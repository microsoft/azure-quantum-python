import * as React from "react";
import { createRoot } from 'react-dom/client';
import { SpaceDiagram, TimeDiagram } from "quantum-visualization";

const sample = {
  errorBudget: {
    logical: 0.0003333333333333333,
    rotations: 0.0003333333333333333,
    tstates: 0.0003333333333333333,
  },
  jobParams: {
    errorBudget: 0.001,
    qecScheme: {
      crossingPrefactor: 0.03,
      errorCorrectionThreshold: 0.01,
      logicalCycleTime:
        "(4 * twoQubitGateTime + 2 * oneQubitMeasurementTime) * codeDistance",
      name: "surface_code",
      physicalQubitsPerLogicalQubit: "2 * codeDistance * codeDistance",
    },
    qubitParams: {
      instructionSet: "GateBased",
      name: "qubit_gate_ns_e3",
      oneQubitGateErrorRate: 0.001,
      oneQubitGateTime: "50 ns",
      oneQubitMeasurementErrorRate: 0.001,
      oneQubitMeasurementTime: "100 ns",
      tGateErrorRate: 0.001,
      tGateTime: "50 ns",
      twoQubitGateErrorRate: 0.001,
      twoQubitGateTime: "50 ns",
    },
  },
  logicalCounts: {
    ccixCount: 0,
    cczCount: 0,
    measurementCount: 0,
    numQubits: 16,
    rotationCount: 882,
    rotationDepth: 381,
    tCount: 186,
  },
  logicalQubit: {
    codeDistance: 15,
    logicalCycleTime: 6000.0,
    logicalErrorRate: 3.0000000000000028e-10,
    physicalQubits: 450,
  },
  physicalCounts: {
    breakdown: {
      algorithmicLogicalDepth: 7545,
      algorithmicLogicalQubits: 45,
      cliffordErrorRate: 0.001,
      logicalDepth: 7545,
      numTfactories: 28,
      numTfactoryRuns: 543,
      numTsPerRotation: 17,
      numTstates: 15180,
      physicalQubitsForAlgorithm: 20250,
      physicalQubitsForTfactories: 504000,
      requiredLogicalQubitErrorRate: 9.817637385563164e-10,
      requiredLogicalTstateErrorRate: 2.1958717610891526e-8,
    },
    physicalQubits: 524250,
    runtime: 45270000,
  },
  physicalCountsFormatted: {
    codeDistancePerRound: "5, 13",
    errorBudget: "1.00e-3",
    errorBudgetLogical: "3.33e-4",
    errorBudgetRotations: "3.33e-4",
    errorBudgetTstates: "3.33e-4",
    logicalCycleTime: "6us",
    logicalErrorRate: "3.00e-10",
    numTsPerRotation: "17",
    numUnitsPerRound: "18, 1",
    physicalQubitsForTfactoriesPercentage: "96.14 %",
    physicalQubitsPerRound: "18000, 10478",
    requiredLogicalQubitErrorRate: "9.82e-10",
    requiredLogicalTstateErrorRate: "2.20e-8",
    runtime: "45ms 270us",
    tfactoryRuntime: "83us 200ns",
    tfactoryRuntimePerRound: "26us, 57us 200ns",
    tstateLogicalErrorRate: "2.16e-8",
    unitNamePerRound:
      "15-to-1 space efficient logical, 15-to-1 RM prep logical",
  },
  reportData: {
    assumptions: [
      "_More details on the following lists of assumptions can be found in the paper [Accessing requirements for scaling quantum computers and their applications](https://aka.ms/AQ/RE/Paper)._",
      "**Uniform independent physical noise.** We assume that the noise on physical qubits and physical qubit operations is the standard circuit noise model. In particular we assume error events at different space-time locations are independent and that error rates are uniform across the system in time and space.",
      "**Efficient classical computation.** We assume that classical overhead (compilation, control, feedback, readout, decoding, etc.) does not dominate the overall cost of implementing the full quantum algorithm.",
      "**Extraction circuits for planar quantum ISA.** We assume that stabilizer extraction circuits with similar depth and error correction performance to those for standard surface and Hastings-Haah code patches can be constructed to implement all operations of the planar quantum ISA (instruction set architecture).",
      "**Uniform independent logical noise.** We assume that the error rate of a logical operation is approximately equal to its space-time volume (the number of tiles multiplied by the number of logical time steps) multiplied by the error rate of a logical qubit in a standard one-tile patch in one logical time step.",
      "**Negligible Clifford costs for synthesis.** We assume that the space overhead for synthesis and space and time overhead for transport of magic states within magic state factories and to synthesis qubits are all negligible.",
      "**Smooth magic state consumption rate.** We assume that the rate of T state consumption throughout the compiled algorithm is almost constant, or can be made almost constant without significantly increasing the number of logical time steps for the algorithm.",
    ],
    groups: [
      {
        alwaysVisible: true,
        entries: [
          {
            description: "Number of physical qubits",
            explanation:
              "This value represents the total number of physical qubits, which is the sum of 20250 physical qubits to implement the algorithm logic, and 504000 physical qubits to execute the T factories that are responsible to produce the T states that are consumed by the algorithm.",
            label: "Physical qubits",
            path: "physicalCounts/physicalQubits",
          },
          {
            description: "Total runtime",
            explanation:
              "This is a runtime estimate (in nanosecond precision) for the execution time of the algorithm.  In general, the execution time corresponds to the duration of one logical cycle (6us) multiplied by the 7545 logical cycles to run the algorithm.  If however the duration of a single T factory (here: 83us 200ns) is larger than the algorithm runtime, we extend the number of logical cycles artificially in order to exceed the runtime of a single T factory.",
            label: "Runtime",
            path: "physicalCountsFormatted/runtime",
          },
        ],
        title: "Physical resource estimates",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description:
              "Number of logical qubits for the algorithm after layout",
            explanation:
              "Laying out the logical qubits in the presence of nearest-neighbor constraints requires additional logical qubits.  In particular, to layout the $Q_{\\rm alg} = 16$ logical qubits in the input algorithm, we require in total $2 \\cdot Q_{\\rm alg} + \\lceil \\sqrt{8 \\cdot Q_{\\rm alg}}\\rceil + 1 = 45$ logical qubits.",
            label: "Logical algorithmic qubits",
            path: "physicalCounts/breakdown/algorithmicLogicalQubits",
          },
          {
            description: "Number of logical cycles for the algorithm",
            explanation:
              "To execute the algorithm using _Parallel Synthesis Sequential Pauli Computation_ (PSSPC), operations are scheduled in terms of multi-qubit Pauli measurements, for which assume an execution time of one logical cycle.  Based on the input algorithm, we require one multi-qubit measurement for the 0 single-qubit measurements, the 882 arbitrary single-qubit rotations, and the 186 T gates, three multi-qubit measurements for each of the 0 CCZ and 0 CCiX gates in the input program, as well as 17 multi-qubit measurements for each of the 381 non-Clifford layers in which there is at least one single-qubit rotation with an arbitrary angle rotation.",
            label: "Algorithmic depth",
            path: "physicalCounts/breakdown/algorithmicLogicalDepth",
          },
          {
            description: "Number of logical cycles performed",
            explanation:
              "This number is usually equal to the logical depth of the algorithm, which is 7545.  However, in the case in which a single T factory is slower than the execution time of the algorithm, we adjust the logical cycle depth to exceed the T factory's execution time.",
            label: "Logical depth",
            path: "physicalCounts/breakdown/logicalDepth",
          },
          {
            description: "Number of T states consumed by the algorithm",
            explanation:
              "To execute the algorithm, we require one T state for each of the 186 T gates, four T states for each of the 0 CCZ and 0 CCiX gates, as well as 17 for each of the 882 single-qubit rotation gates with arbitrary angle rotation.",
            label: "Number of T states",
            path: "physicalCounts/breakdown/numTstates",
          },
          {
            description:
              "Number of T factories capable of producing the demanded 15180 T states during the algorithm's runtime",
            explanation:
              "The total number of T factories 28 that are executed in parallel is computed as $\\left\\lceil\\dfrac{15180\\;\\text{T states} \\cdot 83us 200ns\\;\\text{T factory duration}}{1\\;\\text{T states per T factory} \\cdot 45ms 270us\\;\\text{algorithm runtime}}\\right\\rceil$",
            label: "Number of T factories",
            path: "physicalCounts/breakdown/numTfactories",
          },
          {
            description: "Number of times all T factories are invoked",
            explanation:
              "In order to prepare the 15180 T states, the 28 copies of the T factory are repeatedly invoked 543 times.",
            label: "Number of T factory invocations",
            path: "physicalCounts/breakdown/numTfactoryRuns",
          },
          {
            description:
              "Number of physical qubits for the algorithm after layout",
            explanation:
              "The 20250 are the product of the 45 logical qubits after layout and the 450 physical qubits that encode a single logical qubit.",
            label: "Physical algorithmic qubits",
            path: "physicalCounts/breakdown/physicalQubitsForAlgorithm",
          },
          {
            description: "Number of physical qubits for the T factories",
            explanation:
              "Each T factory requires 18000 physical qubits and we run 28 in parallel, therefore we need $504000 = 18000 \\cdot 28$ qubits.",
            label: "Physical T factory qubits",
            path: "physicalCounts/breakdown/physicalQubitsForTfactories",
          },
          {
            description:
              "The minimum logical qubit error rate required to run the algorithm within the error budget",
            explanation:
              "The minimum logical qubit error rate is obtained by dividing the logical error probability 3.33e-4 by the product of 45 logical qubits and the total cycle count 7545.",
            label: "Required logical qubit error rate",
            path: "physicalCountsFormatted/requiredLogicalQubitErrorRate",
          },
          {
            description:
              "The minimum T state error rate required for distilled T states",
            explanation:
              "The minimum T state error rate is obtained by dividing the T distillation error probability 3.33e-4 by the total number of T states 15180.",
            label: "Required logical T state error rate",
            path: "physicalCountsFormatted/requiredLogicalTstateErrorRate",
          },
          {
            description:
              "Number of T states to implement a rotation with an arbitrary angle",
            explanation:
              "The number of T states to implement a rotation with an arbitrary angle is $\\lceil 0.53 \\log_2(882 / 0.0003333333333333333) + 5.3\\rceil$ [[arXiv:2203.10064](https://arxiv.org/abs/2203.10064)].  For simplicity, we use this formula for all single-qubit arbitrary angle rotations, and do not distinguish between best, worst, and average cases.",
            label: "Number of T states per rotation",
            path: "physicalCountsFormatted/numTsPerRotation",
          },
        ],
        title: "Resource estimates breakdown",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description: "Name of QEC scheme",
            explanation:
              "You can load pre-defined QEC schemes by using the name `surface_code` or `floquet_code`. The latter only works with Majorana qubits.",
            label: "QEC scheme",
            path: "jobParams/qecScheme/name",
          },
          {
            description: "Required code distance for error correction",
            explanation:
              "The code distance is the smallest odd integer greater or equal to $\\dfrac{2\\log(0.03 / 0.0000000009817637385563163)}{\\log(0.01/0.001)} - 1$",
            label: "Code distance",
            path: "logicalQubit/codeDistance",
          },
          {
            description: "Number of physical qubits per logical qubit",
            explanation:
              "The number of physical qubits per logical qubit are evaluated using the formula 2 * codeDistance * codeDistance that can be user-specified.",
            label: "Physical qubits",
            path: "logicalQubit/physicalQubits",
          },
          {
            description: "Duration of a logical cycle in nanoseconds",
            explanation:
              "The runtime of one logical cycle in nanoseconds is evaluated using the formula (4 * twoQubitGateTime + 2 * oneQubitMeasurementTime) * codeDistance that can be user-specified.",
            label: "Logical cycle time",
            path: "physicalCountsFormatted/logicalCycleTime",
          },
          {
            description: "Logical qubit error rate",
            explanation:
              "The logical qubit error rate is computed as $0.03 \\cdot \\left(\\dfrac{0.001}{0.01}\\right)^\\frac{15 + 1}{2}$",
            label: "Logical qubit error rate",
            path: "physicalCountsFormatted/logicalErrorRate",
          },
          {
            description: "Crossing prefactor used in QEC scheme",
            explanation:
              "The crossing prefactor is usually extracted numerically from simulations when fitting an exponential curve to model the relationship between logical and physical error rate.",
            label: "Crossing prefactor",
            path: "jobParams/qecScheme/crossingPrefactor",
          },
          {
            description: "Error correction threshold used in QEC scheme",
            explanation:
              "The error correction threshold is the physical error rate below which the error rate of the logical qubit is less than the error rate of the physical qubit that constitute it.  This value is usually extracted numerically from simulations of the logical error rate.",
            label: "Error correction threshold",
            path: "jobParams/qecScheme/errorCorrectionThreshold",
          },
          {
            description:
              "QEC scheme formula used to compute logical cycle time",
            explanation:
              "This is the formula that is used to compute the logical cycle time 6us.",
            label: "Logical cycle time formula",
            path: "jobParams/qecScheme/logicalCycleTime",
          },
          {
            description:
              "QEC scheme formula used to compute number of physical qubits per logical qubit",
            explanation:
              "This is the formula that is used to compute the number of physical qubits per logical qubits 450.",
            label: "Physical qubits formula",
            path: "jobParams/qecScheme/physicalQubitsPerLogicalQubit",
          },
        ],
        title: "Logical qubit parameters",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description: "Number of physical qubits for a single T factory",
            explanation:
              "This corresponds to the maximum number of physical qubits over all rounds of T distillation units in a T factory.  A round of distillation contains of multiple copies of distillation units to achieve the required success probability of producing a T state with the expected logical T state error rate.",
            label: "Physical qubits",
            path: "tfactory/physicalQubits",
          },
          {
            description: "Runtime of a single T factory",
            explanation:
              "The runtime of a single T factory is the accumulated runtime of executing each round in a T factory.",
            label: "Runtime",
            path: "physicalCountsFormatted/tfactoryRuntime",
          },
          {
            description:
              "Number of output T states produced in a single run of T factory",
            explanation:
              "The T factory takes as input 270 noisy physical T states with an error rate of 0.001 and produces 1 T states with an error rate of 2.16e-8.",
            label: "Number of output T states per run",
            path: "tfactory/numTstates",
          },
          {
            description:
              "Number of physical input T states consumed in a single run of a T factory",
            explanation:
              "This value includes the physical input T states of all copies of the distillation unit in the first round.",
            label: "Number of input T states per run",
            path: "tfactory/numInputTstates",
          },
          {
            description: "The number of distillation rounds",
            explanation:
              "This is the number of distillation rounds.  In each round one or multiple copies of some distillation unit is executed.",
            label: "Distillation rounds",
            path: "tfactory/numRounds",
          },
          {
            description: "The number of units in each round of distillation",
            explanation:
              "This is the number of copies for the distillation units per round.",
            label: "Distillation units per round",
            path: "physicalCountsFormatted/numUnitsPerRound",
          },
          {
            description: "The types of distillation units",
            explanation:
              "These are the types of distillation units that are executed in each round.  The units can be either physical or logical, depending on what type of qubit they are operating.  Space-efficient units require fewer qubits for the cost of longer runtime compared to Reed-Muller preparation units.",
            label: "Distillation units",
            path: "physicalCountsFormatted/unitNamePerRound",
          },
          {
            description: "The code distance in each round of distillation",
            explanation:
              "This is the code distance used for the units in each round.  If the code distance is 1, then the distillation unit operates on physical qubits instead of error-corrected logical qubits.",
            label: "Distillation code distances",
            path: "physicalCountsFormatted/codeDistancePerRound",
          },
          {
            description:
              "The number of physical qubits used in each round of distillation",
            explanation:
              "The maximum number of physical qubits over all rounds is the number of physical qubits for the T factory, since qubits are reused by different rounds.",
            label: "Number of physical qubits per round",
            path: "physicalCountsFormatted/physicalQubitsPerRound",
          },
          {
            description: "The runtime of each distillation round",
            explanation:
              "The runtime of the T factory is the sum of the runtimes in all rounds.",
            label: "Runtime per round",
            path: "physicalCountsFormatted/tfactoryRuntimePerRound",
          },
          {
            description: "Logical T state error rate",
            explanation:
              "This is the logical T state error rate achieved by the T factory which is equal or smaller than the required error rate 2.20e-8.",
            label: "Logical T state error rate",
            path: "physicalCountsFormatted/tstateLogicalErrorRate",
          },
        ],
        title: "T factory parameters",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description:
              "Number of logical qubits in the input quantum program",
            explanation:
              "We determine 45 from this number by assuming to align them in a 2D grid.  Auxiliary qubits are added to allow for sufficient space to execute multi-qubit Pauli measurements on all or a subset of the logical qubits.",
            label: "Logical qubits (pre-layout)",
            path: "logicalCounts/numQubits",
          },
          {
            description: "Number of T gates in the input quantum program",
            explanation:
              "This includes all T gates and adjoint T gates, but not T gates used to implement rotation gates with arbitrary angle, CCZ gates, or CCiX gates.",
            label: "T gates",
            path: "logicalCounts/tCount",
          },
          {
            description:
              "Number of rotation gates in the input quantum program",
            explanation:
              "This is the number of all rotation gates. If an angle corresponds to a Pauli, Clifford, or T gate, it is not accounted for in this number.",
            label: "Rotation gates",
            path: "logicalCounts/rotationCount",
          },
          {
            description: "Depth of rotation gates in the input quantum program",
            explanation:
              "This is the number of all non-Clifford layers that include at least one single-qubit rotation gate with an arbitrary angle.",
            label: "Rotation depth",
            path: "logicalCounts/rotationDepth",
          },
          {
            description: "Number of CCZ-gates in the input quantum program",
            explanation: "This is the number of CCZ gates.",
            label: "CCZ gates",
            path: "logicalCounts/cczCount",
          },
          {
            description: "Number of CCiX-gates in the input quantum program",
            explanation:
              "This is the number of CCiX gates, which applies $-iX$ controlled on two control qubits [[1212.5069](https://arxiv.org/abs/1212.5069)].",
            label: "CCiX gates",
            path: "logicalCounts/ccixCount",
          },
          {
            description:
              "Number of single qubit measurements in the input quantum program",
            explanation:
              "This is the number of single qubit measurements in Pauli basis that are used in the input program.  Note that all measurements are counted, however, the measurement result is is determined randomly (with a fixed seed) to be 0 or 1 with a probability of 50%.",
            label: "Measurement operations",
            path: "logicalCounts/measurementCount",
          },
        ],
        title: "Pre-layout logical resources",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description: "Total error budget for the algorithm",
            explanation:
              "The total error budget sets the overall allowed error for the algorithm, i.e., the number of times it is allowed to fail.  Its value must be between 0 and 1 and the default value is 0.001, which corresponds to 0.1%, and means that the algorithm is allowed to fail once in 1000 executions.  This parameter is highly application specific. For example, if one is running Shor's algorithm for factoring integers, a large value for the error budget may be tolerated as one can check that the output are indeed the prime factors of the input.  On the other hand, a much smaller error budget may be needed for an algorithm solving a problem with a solution which cannot be efficiently verified.  This budget $\\epsilon = \\epsilon_{\\log} + \\epsilon_{\\rm dis} + \\epsilon_{\\rm syn}$ is uniformly distributed and applies to errors $\\epsilon_{\\log}$ to implement logical qubits, an error budget $\\epsilon_{\\rm dis}$ to produce T states through distillation, and an error budget $\\epsilon_{\\rm syn}$ to synthesize rotation gates with arbitrary angles.  Note that for distillation and rotation synthesis, the respective error budgets $\\epsilon_{\\rm dis}$ and $\\epsilon_{\\rm syn}$ are uniformly distributed among all T states and all rotation gates, respectively. If there are no rotation gates in the input algorithm, the error budget is uniformly distributed to logical errors and T state errors.",
            label: "Total error budget",
            path: "physicalCountsFormatted/errorBudget",
          },
          {
            description: "Probability of at least one logical error",
            explanation:
              "This is one third of the total error budget 1.00e-3 if the input algorithm contains rotation with gates with arbitrary angles, or one half of it, otherwise.",
            label: "Logical error probability",
            path: "physicalCountsFormatted/errorBudgetLogical",
          },
          {
            description: "Probability of at least one faulty T distillation",
            explanation:
              "This is one third of the total error budget 1.00e-3 if the input algorithm contains rotation with gates with arbitrary angles, or one half of it, otherwise.",
            label: "T distillation error probability",
            path: "physicalCountsFormatted/errorBudgetTstates",
          },
          {
            description:
              "Probability of at least one failed rotation synthesis",
            explanation: "This is one third of the total error budget 1.00e-3.",
            label: "Rotation synthesis error probability",
            path: "physicalCountsFormatted/errorBudgetRotations",
          },
        ],
        title: "Assumed error budget",
      },
      {
        alwaysVisible: false,
        entries: [
          {
            description: "Some descriptive name for the qubit model",
            explanation:
              "You can load pre-defined qubit parameters by using the names `qubit_gate_ns_e3`, `qubit_gate_ns_e4`, `qubit_gate_us_e3`, `qubit_gate_us_e4`, `qubit_maj_ns_e4`, or `qubit_maj_ns_e6`.  The names of these pre-defined qubit parameters indicate the instruction set (gate-based or Majorana), the operation speed (ns or ¬µs regime), as well as the fidelity (e.g., e3 for $10^{-3}$ gate error rates).",
            label: "Qubit name",
            path: "jobParams/qubitParams/name",
          },
          {
            description: "Underlying qubit technology (gate-based or Majorana)",
            explanation:
              "When modeling the physical qubit abstractions, we distinguish between two different physical instruction sets that are used to operate the qubits.  The physical instruction set can be either *gate-based* or *Majorana*.  A gate-based instruction set provides single-qubit measurement, single-qubit gates (incl. T gates), and two-qubit gates.  A Majorana instruction set provides a physical T gate, single-qubit measurement and two-qubit joint measurement operations.",
            label: "Instruction set",
            path: "jobParams/qubitParams/instructionSet",
          },
          {
            description:
              "Operation time for single-qubit measurement (t_meas) in ns",
            explanation:
              "This is the operation time in nanoseconds to perform a single-qubit measurement in the Pauli basis.",
            label: "Single-qubit measurement time",
            path: "jobParams/qubitParams/oneQubitMeasurementTime",
          },
          {
            description: "Operation time for single-qubit gate (t_gate) in ns",
            explanation:
              "This is the operation time in nanoseconds to perform a single-qubit Clifford operation, e.g., Hadamard or Phase gates.",
            label: "Single-qubit gate time",
            path: "jobParams/qubitParams/oneQubitGateTime",
          },
          {
            description: "Operation time for two-qubit gate in ns",
            explanation:
              "This is the operation time in nanoseconds to perform a two-qubit Clifford operation, e.g., a CNOT or CZ gate.",
            label: "Two-qubit gate time",
            path: "jobParams/qubitParams/twoQubitGateTime",
          },
          {
            description: "Operation time for a T gate",
            explanation:
              "This is the operation time in nanoseconds to execute a T gate.",
            label: "T gate time",
            path: "jobParams/qubitParams/tGateTime",
          },
          {
            description: "Error rate for single-qubit measurement",
            explanation:
              "This is the probability in which a single-qubit measurement in the Pauli basis may fail.",
            label: "Single-qubit measurement error rate",
            path: "jobParams/qubitParams/oneQubitMeasurementErrorRate",
          },
          {
            description: "Error rate for single-qubit Clifford gate (p)",
            explanation:
              "This is the probability in which a single-qubit Clifford operation, e.g., Hadamard or Phase gates, may fail.",
            label: "Single-qubit error rate",
            path: "jobParams/qubitParams/oneQubitGateErrorRate",
          },
          {
            description: "Error rate for two-qubit Clifford gate",
            explanation:
              "This is the probability in which a two-qubit Clifford operation, e.g., CNOT or CZ gates, may fail.",
            label: "Two-qubit error rate",
            path: "jobParams/qubitParams/twoQubitGateErrorRate",
          },
          {
            description:
              "Error rate to prepare single-qubit T state or apply a T gate (p_T)",
            explanation:
              "This is the probability in which executing a single T gate may fail.",
            label: "T gate error rate",
            path: "jobParams/qubitParams/tGateErrorRate",
          },
        ],
        title: "Physical qubit parameters",
      },
    ],
  },
  status: "success",
  tfactory: {
    codeDistancePerRound: [5, 13],
    logicalErrorRate: 2.1638392653473639e-8,
    numInputTstates: 270,
    numRounds: 2,
    numTstates: 1,
    numUnitsPerRound: [18, 1],
    physicalQubits: 18000,
    physicalQubitsPerRound: [18000, 10478],
    runtime: 83200.0,
    runtimePerRound: [26000.0, 57200.0],
    unitNamePerRound: [
      "15-to-1 space efficient logical",
      "15-to-1 RM prep logical",
    ],
  },
};

class SpaceDiagramComponent extends HTMLElement {
  connectedCallback() {
    // TODO :we need to genarate a random id
    this.innerHTML = `<div id="space-diagram"> </div>`;
    // const data = this.getAttribute("data");
    var data = JSON.stringify(sample);
    if (data) {
      const root = createRoot(
        document.getElementById('space-diagram')
      );
      root.render(<SpaceDiagram width={1000} height={1000} data={data} />);
    } else {
      console.error("Rendering error: Space Diagram requires data.");
    }
  }
}

class TimeDiagramComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<div id="time-diagram"> </div>`;
    // const data = this.getAttribute("data");
    var data = JSON.stringify(sample);
    if (data) {
      const root = createRoot(
        document.getElementById('time-diagram')
      );
      root.render(<TimeDiagram width={1000} height={1000} data={data} />);
    } else {
      console.error("Rendering error: Time Diagram requires data.");
    }
  }
}

window.customElements.get("re-space-diagram") ||
window.customElements.define("re-space-diagram", SpaceDiagramComponent);

window.customElements.get("re-time-diagram") ||
window.customElements.define("re-time-diagram", TimeDiagramComponent);
