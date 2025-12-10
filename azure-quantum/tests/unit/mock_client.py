"""
Mock Azure Quantum REST client used to back a real Workspace
without making network calls. Returns real SDK models and ItemPaged.
"""

from typing import Callable, Iterable, Iterator, List, Optional
from datetime import datetime, UTC

from azure.core.paging import ItemPaged
from azure.quantum._client import ServicesClient
from azure.quantum._client.models import JobDetails, SessionDetails, ItemDetails


def _paged(items: List, page_size: int = 100) -> ItemPaged:
    """Create an ItemPaged that conforms to azure-core's contract.
    - get_next(token) returns a response payload
    - extract_data(response) returns (items_iterable, next_link)
    """

    def get_next(token):
        start = int(token) if token is not None else 0
        end = start + page_size
        page = items[start:end]
        next_link = str(end) if end < len(items) else None
        # Return a dict-like payload as expected by extract_data
        return {"items": page, "next_link": next_link}

    def extract_data(response):
        # Return (iterable, next_link) per azure.core.paging contract
            if response is None:
                return None, []
            items_iter = response.get("items") or []
            next_link = response.get("next_link")
            # azure.core.paging expects (continuation_token, items)
            return next_link, items_iter

    return ItemPaged(get_next, extract_data)


class JobsOperations:
    def __init__(self, store: List[JobDetails]) -> None:
        self._store = store

    def create_or_replace(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        job_id: str,
        job_details: JobDetails,
    ) -> JobDetails:
        # Mark submitted
        job_details.status = "Submitted"
        # Ensure creation_time present
        if not getattr(job_details, "creation_time", None):
            job_details.creation_time = datetime.utcnow()
        # Upsert by id
        for i, jd in enumerate(self._store):
            if jd.id == job_id:
                self._store[i] = job_details
                break
        else:
            self._store.append(job_details)
        return job_details

    def get(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        job_id: str,
    ) -> JobDetails:
        for jd in self._store:
            if jd.id == job_id:
                return jd
        raise KeyError(job_id)

    def list(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        filter: Optional[str] = None,
        orderby: Optional[str] = None,
        top: int = 100,
        skip: int = 0,
    ) -> ItemPaged[JobDetails]:
        items = list(self._store)
        # Only basic orderby support for CreationTime asc/desc
        if orderby:
            try:
                prop, direction = orderby.split()
                if prop == "CreationTime":
                    items.sort(
                        key=lambda j: getattr(j, "creation_time", datetime.now(UTC)),
                        reverse=(direction == "desc"),
                    )
            except Exception:
                pass
        return _paged(items[skip : skip + top], page_size=top)


class SessionsOperations:
    def __init__(
        self, store: List[SessionDetails], jobs_store: List[JobDetails]
    ) -> None:
        self._store = store
        self._jobs_store = jobs_store

    def create_or_replace(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        session_id: str,
        session_details: SessionDetails,
    ) -> SessionDetails:
        session_details.status = "WAITING"
        if not getattr(session_details, "creation_time", None):
            session_details.creation_time = datetime.utcnow()
        for i, sd in enumerate(self._store):
            if sd.id == session_id:
                self._store[i] = session_details
                break
        else:
            self._store.append(session_details)
        return session_details

    def close(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        session_id: str,
    ) -> SessionDetails:
        sd = self.get(subscription_id, resource_group_name, workspace_name, session_id)
        sd.status = "SUCCEEDED"
        return sd

    def get(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        session_id: str,
    ) -> SessionDetails:
        for sd in self._store:
            if sd.id == session_id:
                return sd
        raise KeyError(session_id)

    def list(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        filter: Optional[str] = None,
        orderby: Optional[str] = None,
        skip: int = 0,
        top: int = 100,
    ) -> ItemPaged[SessionDetails]:
        items = list(self._store)
        if orderby:
            try:
                prop, direction = orderby.split()
                if prop == "CreationTime":
                    items.sort(
                        key=lambda s: getattr(s, "creation_time", datetime.now(UTC)),
                        reverse=(direction == "desc"),
                    )
            except Exception:
                pass
        return _paged(items[skip : skip + top], page_size=top)

    def jobs_list(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        session_id: str,
        filter: Optional[str] = None,
        orderby: Optional[str] = None,
        skip: int = 0,
        top: int = 100,
    ) -> ItemPaged[JobDetails]:
        jobs = [
            j for j in self._jobs_store if getattr(j, "session_id", None) == session_id
        ]
        if orderby:
            try:
                prop, direction = orderby.split()
                if prop == "CreationTime":
                    jobs.sort(
                        key=lambda j: getattr(j, "creation_time", datetime.now(UTC)),
                        reverse=(direction == "desc"),
                    )
            except Exception:
                pass
        return _paged(jobs[skip : skip + top], page_size=top)


class TopLevelItemsOperations:
    def __init__(
        self, jobs_store: List[JobDetails], sessions_store: List[SessionDetails]
    ) -> None:
        self._jobs_store = jobs_store
        self._sessions_store = sessions_store

    def list(
        self,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        filter: Optional[str] = None,
        orderby: Optional[str] = None,
        top: int = 100,
        skip: int = 0,
    ) -> ItemPaged[ItemDetails]:
        items: List[ItemDetails] = []
        for j in self._jobs_store:
            items.append(
                ItemDetails.from_dict(
                    {
                        "id": j.id,
                        "itemType": "Job",
                        "name": getattr(j, "name", j.id),
                        "providerId": getattr(j, "provider_id", None),
                        "target": getattr(j, "target", None),
                        "status": getattr(j, "status", None),
                        "creationTime": getattr(j, "creation_time", datetime.utcnow()),
                    }
                )
            )
        for s in self._sessions_store:
            items.append(
                ItemDetails.from_dict(
                    {
                        "id": s.id,
                        "itemType": "Session",
                        "name": getattr(s, "name", s.id),
                        "providerId": getattr(s, "provider_id", None),
                        "target": getattr(s, "target", None),
                        "status": getattr(s, "status", None),
                        "creationTime": getattr(s, "creation_time", datetime.utcnow()),
                    }
                )
            )
        if orderby:
            try:
                prop, direction = orderby.split()
                if prop == "CreationTime":
                    items.sort(
                        key=lambda i: getattr(i, "creation_time", datetime.now(UTC)),
                        reverse=(direction == "desc"),
                    )
            except Exception:
                pass
        return _paged(items[skip : skip + top], page_size=top)


class MockServicesClient(ServicesClient):
    def __init__(self) -> None:
        # in-memory stores
        self._jobs_store: List[JobDetails] = []
        self._sessions_store: List[SessionDetails] = []
        # operations
        self.jobs = JobsOperations(self._jobs_store)
        self.sessions = SessionsOperations(self._sessions_store, self._jobs_store)
        self.top_level_items = TopLevelItemsOperations(
            self._jobs_store, self._sessions_store
        )
