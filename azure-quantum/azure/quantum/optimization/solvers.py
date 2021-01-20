##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import uuid, io
import azure.quantum

from typing import List, Union, Any, Optional
from enum import Enum
from azure.quantum import Workspace, Job
from azure.quantum._client.models import JobDetails
from azure.quantum.optimization import Problem
from azure.quantum.storage import ContainerClient, create_container_using_client

logger = logging.getLogger(__name__)

__all__ = [
    'Solver',
    'ParallelTempering',
    'SimulatedAnnealing',
    'HardwarePlatform',
    'Tabu',
    'QuantumMonteCarlo'
]

class Solver:

    def __init__(
        self,
        workspace: Workspace,
        provider: str,
        target: str,
        input_data_format: str,
        output_data_format: str,
        nested_params: bool=True,
        force_str_params: bool=False
        ):
        self.workspace = workspace
        self.target = target
        self.provider = provider
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.nested_params = nested_params
        self.force_str_params = force_str_params
        self.params = { "params": {} } if nested_params else {}

    def submit(self, problem: Union[str, Problem]) -> Job:
        """Submits a job to execution to the associated Azure Quantum Workspace.

       :param problem: 
            The Problem to solve. It can be an instance of a Problem, 
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        """
        ## Create a container URL:
        job_id = uuid.uuid1()
        logger.info(f"Submitting job with id: {job_id}")

        container_name = f"job-{job_id}"

        if not self.workspace.storage:
            # No storage account is passed, in this case, get linked account from the service
            container_uri = self.workspace._get_linked_storage_sas_uri(container_name)
            container_client = ContainerClient.from_container_url(container_uri)
            create_container_using_client(container_client)
            container_uri = azure.quantum.storage.remove_sas_token(container_uri)
        else:
            # Storage account is passed, use it to generate a container_uri
            container_uri = azure.quantum.storage.get_container_uri(self.workspace.storage, container_name)
        
        logger.debug(f"Container URI: {container_uri}")

        if isinstance(problem, str):
            name = "Optimization problem"
            problem_uri = problem  
        else:
            name = problem.name
            problem_uri = problem.upload(self.workspace, compress=True, container_name=container_name, blob_name="inputData")
        
        logger.info(f"Submitting problem '{name}'. Using payload from: '{problem_uri}'")

        details = JobDetails(
            id=job_id,
            name=name,
            container_uri=container_uri,
            input_data_format=self.input_data_format,
            output_data_format=self.output_data_format,
            input_data_uri=problem_uri,
            provider_id=self.provider,
            target=self.target,
            input_params=self.params
        )

        logger.debug(f"==> submitting: {details}")
        job = self.workspace.submit_job(Job(self.workspace, details))
        return job

    def optimize(self, problem: Union[str, Problem]):
        """Submits the Problem to the associated Azure Quantum Workspace and get the results. 
        
        :param problem: 
            The Problem to solve. It can be an instance of a Problem, 
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        """
        job = self.submit(problem)
        logger.info(f"Submitted job: '{job.id}'")
        
        return job.get_results()

    def set_one_param(self, name: str, value: Any):
        if value is not None:
            params = self.params["params"] if self.nested_params else self.params
            params[name] = str(value) if self.force_str_params else value

class HardwarePlatform(Enum):
    CPU = 1
    FPGA = 2

class ParallelTempering(Solver):
    def __init__(
        self,
        workspace: Workspace,
        sweeps: Optional[int] = None,
        replicas: Optional[int] = None,
        all_betas: Optional[List[int]] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None):
        """The constructor of a Parallel Tempering solver.

        Multi-core Parallel Tempering solver for binary optimization problems with k-local interactions on an all-to-all 
        graph topology with double precision support for the coupler weights.

        :param sweeps: 
            specifies the number of sweeps.
        :param replicas: 
            specifies the number of replicas.
        :param all_betas: 
            a list of floats specifying the list of inverse temperatures. 
            > Note: this list must be equal in length to the number of replicas.            
        :param timeout: 
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the 
            solver may run longer than the value specified.
        :param seed: 
            specifies a random seed value.
        """
        param_free = (
            sweeps is None and
            replicas is None and
            all_betas is None
        )
        platform = HardwarePlatform.CPU
        if platform == HardwarePlatform.FPGA:
            target = "microsoft.paralleltempering.fpga" 
        else:
            target = "microsoft.paralleltempering-parameterfree.cpu" if param_free  else "microsoft.paralleltempering.cpu"

        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2")

        self.set_one_param("sweeps", sweeps)
        self.set_one_param("replicas", replicas)
        self.set_one_param("all_betas", all_betas)
        self.set_one_param("seed", seed)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)

        # Check parameters:
        if not all_betas is None:
            if replicas is None:
                self.set_one_param("replicas", len(all_betas))
            elif len(all_betas) != replicas:
                raise ValueError("Parameter 'replicas' must equal the length of the 'all_betas' parameters.")


class SimulatedAnnealing(Solver):
    
    def __init__(
        self,
        workspace: Workspace,
        beta_start: Optional[float]=None,
        beta_stop: Optional[float]=None,
        sweeps: Optional[int]=None,
        restarts: Optional[int]=None,
        timeout: Optional[int]=None,
        seed: Optional[int]=None,
        platform: Optional[HardwarePlatform]=HardwarePlatform.CPU
        ):
        """The constructor of an Simulated Annealing solver.
        
        Multi-core Simulated Annealing solver for binary optimization problems 
        with k-local interactions on an all-to-all graph topology with double 
        precision support for the coupler weights. 

        :param beta_start: 
            specifies the starting inverse temperature.
        :param beta_stop: 
            specifies the stopping inverse temperature.
        :param sweeps: 
            specifies the number of sweeps.
        :param restarts: 
            specifies the number of restarts.
        :param timeout: 
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the 
            solver may run longer than the value specified.
        :param seed: 
            specifies a random seed value.
        :platform:
            specifies hardware platform HardwarePlatform.CPU or HardwarePlatform.FPGA.
        """
        param_free = (
            beta_start is None and
            beta_stop is None and 
            sweeps is None and
            restarts is None 
        )

        if platform == HardwarePlatform.FPGA:
            target = "microsoft.simulatedannealing-parameterfree.fpga" if param_free  else "microsoft.simulatedannealing.fpga"
        else:
            target = "microsoft.simulatedannealing-parameterfree.cpu" if param_free  else "microsoft.simulatedannealing.cpu"
        
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2")

        self.set_one_param("beta_start", beta_start)
        self.set_one_param("beta_stop", beta_stop)
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("restarts", restarts)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)


class Tabu(Solver):
    
    def __init__(self, workspace:Workspace, sweeps:Optional[int]=None, tabu_tenure:Optional[int]=None, timeout:Optional[int]=None, seed:Optional[int]=None):
        """The constructor of an Tabu Search solver.
        
        Multi-core Tabu Search solver for binary optimization problems 
        with k-local interactions on an all-to-all graph topology with double 
        precision support for the coupler weights. 

        This solver is CPU only.

        :param sweeps: 
            specifies the number of sweeps.
        :param tabu_tenure: 
            specifies the tabu tenure.
        :param timeout: 
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the 
            solver may run longer than the value specified.
        :param seed: 
            specifies a random seed value.
        """
        param_free = (
            sweeps is None and
            tabu_tenure is None 
        )
        
        target = "microsoft.tabu-parameterfree.cpu" if param_free else "microsoft.tabu.cpu"
        
        super().__init__(
            workspace=workspace, 
            provider="Microsoft", 
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2")
        
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("tabu_tenure", tabu_tenure)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)

class QuantumMonteCarlo(Solver):
    def __init__(
        self, 
        workspace:Workspace, 
        trotter_number:Optional[int]=None, 
        seed:Optional[int]=None,  
        transverse_field_start:Optional[float] = None,
        transverse_field_stop:Optional[float] = None,
        restarts:Optional[int] = None,
        sweeps:Optional[int]=None,
        beta_start:Optional[float]=None):
        """The constructor of Simulated Qunatum Annelaing Search solver.
        
        Simulated Quantum Search solver for binary optimization problems 
        with k-local interactions on an all-to-all graph topology with double 
        precision support for the coupler weights. 

        This solver is CPU only.

        :param trotter_number: 
            specifies the number of trotter time slices i.e. number of copies of each variable.
        :param seed: 
            specifies a random seed value.
        :param sweeps:
            Number of monte carlo sweeps
        :param transverse_field_start:
            starting strength of the external field
        :param transverse_field_end:
            ending strength of the external field
        :param beta_start: 
            Low starting temp i.e. beta start 
        :param restarts:
            Number of simulation runs
        """
        
        target = "microsoft.qmc.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2")
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("trotter_number", trotter_number)
        self.set_one_param("seed", seed)
        self.set_one_param("transverse_field_start",transverse_field_start)
        self.set_one_param("transverse_field_stop",transverse_field_stop)
        self.set_one_param("beta_start",beta_start)
        self.set_one_param("restarts",restarts)

