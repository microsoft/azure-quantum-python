##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
"""
Module providing the Paginator class, used to fetch paged items from
an Azure Quantum Workspace.
"""

from typing import Optional

class Paginator:
    """Class representing a pagination iterator"""

    def __init__(
        self,
        fetch_data_function,
        subscription_id: str,
        resource_group_name: str,
        workspace_name: str,
        *,
        filter: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = 100,
        skip: Optional[int] = 0,
        **kwargs):
        """
        Initialize the Paginator.

        Args:
            fetch_data_function (callable): A function to fetch data. 
                                            It must accept `page_number` and `page_size` as arguments.
            page_size (int): Number of items per page. Default is 10.
            **kwargs: Additional arguments to pass to the fetch_data_function.
        """
        self.fetch_data_function = fetch_data_function
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.workspace_name = workspace_name
        self.filter = filter
        self.orderby = orderby
        self.top = top
        self.skip = skip
        self._kwargs = kwargs
        self._current_page_data = []
        self.has_next = True

    def fetch_data(self):
        """
        Fetch the current page of data.
        
        Returns:
            list: Data of the current page.
        """
        if not self._current_page_data:
            print("kwargs:", self._kwargs)

            response = self.fetch_data_function(**self._kwargs, subscription_id=self.subscription_id, resource_group_name=self.resource_group_name, workspace_name=self.workspace_name, filter=self.filter, orderby=self.orderby, top = self.top, skip = self.skip)
            print("response:", response)
            self._current_page_data = response.by_page()
            self.has_next = True if response.next is not None else False
            self.skip = self.skip + self.top
        return self._current_page_data
    