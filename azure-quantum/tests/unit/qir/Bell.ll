; ModuleID = 'Bell circuit'
source_filename = "./module.ll"

%Qubit = type opaque
%Result = type opaque

define void @QuantumApplication__Run__body() #0 {
entry:
  %qr0 = call %Qubit* @__quantum__rt__qubit_allocate()
  %qr1 = call %Qubit* @__quantum__rt__qubit_allocate()
  call void @__quantum__qis__h__body(%Qubit* %qr0)
  call void @__quantum__qis__cnot__body(%Qubit* %qr0, %Qubit* %qr1)
  %qc0 = call %Result* @__quantum__qis__m__body(%Qubit* %qr0)
  %qc1 = call %Result* @__quantum__qis__m__body(%Qubit* %qr1)
  call void @__quantum__rt__qubit_release(%Qubit* %qr1)
  call void @__quantum__rt__qubit_release(%Qubit* %qr0)
  ret void
}

declare void @__quantum__qis__cnot__body(%Qubit*, %Qubit*)

declare void @__quantum__qis__h__body(%Qubit*)

declare %Result* @__quantum__qis__m__body(%Qubit*)

declare %Qubit* @__quantum__rt__qubit_allocate()

declare void @__quantum__rt__qubit_release(%Qubit*)

attributes #0 = { "EntryPoint" }