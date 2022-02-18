
algorithms chsh-game CHSHGame.csproj
Args = @() },

algorithms oracle-synthesis OracleSynthesis.csproj
Args = @() },

characterization phase-estimation PhaseEstimationSample.csproj
Args = @() },

error-correction bit-flip-code BitFlipCode.csproj
Args = @() },

getting-started measurement Measurement.csproj
Args = @() },

getting-started qrng Qrng.csproj
Args = @() },

getting-started teleportation TeleportationSample.csproj
Args = @() },

numerics custom-mod-add CustomModAdd.csproj
Args = @() },

simulation h2 command-line H2SimulationSampleCmdLine.csproj
Args = @() },

simulation hubbard HubbardSimulationSample.csproj
Args = @() },

algorithms database-search DatabaseSearchSample.csproj
Args = @("Microsoft.Quantum.Samples.DatabaseSearch.RunMultipleQuantumSearch") },

simulation ising IsingSamples.csproj
Args = @("Microsoft.Quantum.Samples.Ising.RunPhaseEstimation") },

algorithms order-finding OrderFinding.csproj
Args = @("--index", "1") },

algorithms repeat-until-success RepeatUntilSuccess.csproj
Args = @("--gate", "simple", "--input-value", "true", "--input-basis", "PauliX", "--limit", "4", "--num-runs", "2") },

algorithms simple-grover SimpleGroverSample.csproj
Args = @("--n-qubits", "8") },

azure-quantum grover Grover.csproj
Args = @("--n-qubits", "3", "--idx-marked", "6") },

azure-quantum hidden-shift HiddenShift.csproj
Args = @("--pattern-int", "6", "--register-size", "4") },

azure-quantum ising-model IsingModel.csproj
Args = @("--n-sites", "5", "--time", "5.0", "--dt", "0.1") },

azure-quantum parallel-qrng ParallelQrng.csproj
Args = @("--n-qubits", "3") },

error-correction syndrome Syndrome.csproj
Args = @("--n-qubits", "5") },

getting-started simple-algorithms SimpleAlgorithms.csproj
Args = @("--n-qubits", "4") },

simulation qaoa QAOA.csproj
Args = @("--num-trials", "20") }
