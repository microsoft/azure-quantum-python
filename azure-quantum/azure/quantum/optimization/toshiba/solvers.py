##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
from typing import Union, Optional
from azure.quantum import Workspace
from azure.quantum.optimization import Problem, Solver
from azure.quantum import Job

logger = logging.getLogger(__name__)
__all__ = ["SimulatedBifurcationMachine"]


class SimulatedBifurcationMachine(Solver):
    def __init__(
        self,
        workspace: Workspace,
        steps: Optional[int] = None,
        loops: Optional[int] = None,
        target: Optional[float] = None,
        maxout: Optional[int] = None,
        timeout: Optional[float] = None,
        dt: Optional[float] = None,
        C: Optional[float] = None,
        algo: Optional[str] = None,
        auto: Optional[bool] = None,
    ):
        """The constructor of Toshiba's simulated bifurcation machine.

        This solver enables users to quickly obtain nearly optimal
        solutions for large combinatorial optimization problems.
        It is developed based on the theory described in the following paper:
        Goto, H., Tatsumura, K., & Dixon, A. R. (2019)
        Combinatorial optimization by simulating adiabatic bifurcations
        in nonlinear Hamiltonian systems, Science Advances,
        5(4), DOI:10.1126/sciadv.aav2372
        :param steps:
           The number of steps in a computation request.
           The default is 0.
           The value 0 means auto step where SBM computation
           service dynamically determines the number of steps.
           The maximum is 100,000,000.
        :param loops:
            The number of loops in SBM computation.
            SBM computation service searches for a better solution
            while repeating loops as many times as is specified.
            The default is 1. If 0 (zero) is specified, computation
            will be repeated until a timeout occurs. The maximum is 10,000,000.
        :param target:
            The end condition of a computation request. When the
            evaluation value reaches this value, the computation will stop.
            If 0 is specified for the parameter loops,
            loops will be repeated either until
            the objective function reaches the value
            specified in the parameter target or until a timeout occurs.
        :param maxout:
            The upper limit of the number of solutions
            to be outputted. The default is 1.
            Until the limit specified by maxout is reached,
            SBM computation service outputs the
            obtained solutions in descending order
            of the value of the objective function.
            The maximum is 1,000.
        :param timeout:
            The maximum computation time (timeout) in seconds.
            The default is 10.
            When the computation time reaches the upper limit before
            completing the computation for steps * loops,
            the computation ends at that point.
            In this case, the execution result will be the
            best solution obtained thus far.
            If 0 is specified for the parameter loops, loops will be repeated
            until the time specified by the parameter timeout expires.
            The maximum is 360.
        :param dt:
            The time per step. The range of the value is greater than
            0.0 and less than or equal to 1.0.
        :param C:
            Corresponds to the constant ξ0,
            appearing in the paper by Goto, Tatsumura,
            & Dixon (2019, p. 2), which is the theoretical basis of SBM.
            Specify the constant as a single-precision floating point
            number, equal to or more than 0.
            If the value is 0, the value C is automatically determined.
        :param algo:
            The type of SBM computation algorithm.
            The default is "2.0". One of "1.5" or "2.0".
            Depending on the type of problem, there may be differences
            in performance between the "1.5" and "2.0" algorithms.
            Try both and decide which yields better performance.
        :param auto:
            The parameter auto tuning flag. The default is "false."
            If the value is "true," SBM computation service searches for
            the values of the parameters automatically to obtain
            the best solution.
            Parameters other than `auto` are treated as follows
            in this case. `algo` and `dt` are ignored and tuned automatically.
            `loops` and `maxout` are ignored.
            `timeout` can be specified as the total computation time (sec).
            Other parameters are treated as defined
        """
        super().__init__(
            workspace=workspace,
            provider="toshiba",
            target="toshiba.sbm.ising",
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            nested_params=False,
            force_str_params=False,
        )
        self.set_one_param("steps", steps)
        self.set_one_param("loops", loops)
        self.set_one_param("target", target)
        self.set_one_param("maxout", maxout)
        self.set_one_param("timeout", timeout)
        self.set_one_param("dt", dt)
        self.set_one_param("C", C)
        self.set_one_param("algo", algo)
        self.set_one_param("auto", auto)

    # We are temporarily disabling the
    # compression of problems for the Toshiba
    # solver to mitigate an issue downloading
    # gzip files using the Blob Storage SDK
    # Issue: https://github.com/Azure/azure-storage-python/issues/548
    def submit(
        self, problem: Union[str, Problem], compress: bool = True
    ) -> Job:
        """Submits a job to execution to
        the associated Azure Quantum Workspace.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :param compress:
            Whether or not to compress the problem when uploading it
            the Blob Storage.
        """
        return super().submit(problem=problem, compress=False)
