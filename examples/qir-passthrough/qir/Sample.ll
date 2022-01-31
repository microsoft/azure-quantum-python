
%Range = type { i64, i64, i64 }
%Tuple = type opaque
%String = type opaque
%Array = type opaque
%Qubit = type opaque
%Callable = type opaque
%Result = type opaque

@PauliI = internal constant i2 0
@PauliX = internal constant i2 1
@PauliY = internal constant i2 -1
@PauliZ = internal constant i2 -2
@EmptyRange = internal constant %Range { i64 0, i64 1, i64 -1 }
@0 = internal constant [21 x i8] c"Hello quantum world!\00"
@1 = internal constant [14 x i8] c"Initial state\00"
@2 = internal constant [9 x i8] c"State a:\00"
@3 = internal constant [9 x i8] c"State b:\00"
@4 = internal constant [9 x i8] c"a phase:\00"
@5 = internal constant [9 x i8] c"b phase:\00"
@6 = internal constant [11 x i8] c"After AddI\00"
@7 = internal constant [10 x i8] c"After QFT\00"
@8 = internal constant [10 x i8] c"a result:\00"
@9 = internal constant [10 x i8] c"b result:\00"
@10 = internal constant [2 x i8] c"\22\00"
@11 = internal constant [13 x i8] c"\0A\09Expected:\09\00"
@12 = internal constant [5 x i8] c"true\00"
@13 = internal constant [6 x i8] c"false\00"
@14 = internal constant [11 x i8] c"\0A\09Actual:\09\00"
@15 = internal constant [39 x i8] c"Array must be of the length at least 1\00"
@16 = internal constant [46 x i8] c"`Length(bits)` must be less than 64, but was \00"
@17 = internal constant [2 x i8] c".\00"
@Microsoft__Quantum__Convert__ResultAsBool__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Convert__ResultAsBool__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* null, void (%Tuple*, %Tuple*, %Tuple*)* null, void (%Tuple*, %Tuple*, %Tuple*)* null]
@Microsoft__Quantum__Intrinsic__CNOT__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Intrinsic__CNOT__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Intrinsic__CNOT__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Intrinsic__CNOT__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Intrinsic__CNOT__ctladj__wrapper]
@Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctladj__wrapper]
@18 = internal constant [29 x i8] c"`Length(qs)` must be least 1\00"
@19 = internal constant [48 x i8] c"`a` must be positive and less than `Length(qs)`\00"
@20 = internal constant [53 x i8] c"Input registers must have the same number of qubits.\00"
@21 = internal constant [41 x i8] c"xs must not contain more qubits than ys!\00"
@Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* null, void (%Tuple*, %Tuple*, %Tuple*)* null, void (%Tuple*, %Tuple*, %Tuple*)* null]
@PartialApplication__1__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__1__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__1__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__1__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__1__ctladj__wrapper]
@Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctladj__wrapper]
@MemoryManagement__1__FunctionTable = internal constant [2 x void (%Tuple*, i32)*] [void (%Tuple*, i32)* @MemoryManagement__1__RefCount, void (%Tuple*, i32)* @MemoryManagement__1__AliasCount]
@PartialApplication__2__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__2__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__2__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__2__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__2__ctladj__wrapper]
@PartialApplication__3__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__3__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__3__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__3__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__3__ctladj__wrapper]
@PartialApplication__4__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__4__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__4__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__4__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__4__ctladj__wrapper]
@Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctladj__wrapper]
@Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctladj__wrapper]
@PartialApplication__5__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__5__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__5__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__5__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__5__ctladj__wrapper]
@Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctladj__wrapper]
@MemoryManagement__2__FunctionTable = internal constant [2 x void (%Tuple*, i32)*] [void (%Tuple*, i32)* @MemoryManagement__2__RefCount, void (%Tuple*, i32)* @MemoryManagement__2__AliasCount]
@PartialApplication__6__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__6__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__6__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__6__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__6__ctladj__wrapper]
@PartialApplication__7__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__7__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__7__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__7__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__7__ctladj__wrapper]
@PartialApplication__8__FunctionTable = internal constant [4 x void (%Tuple*, %Tuple*, %Tuple*)*] [void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__8__body__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__8__adj__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__8__ctl__wrapper, void (%Tuple*, %Tuple*, %Tuple*)* @Lifted__PartialApplication__8__ctladj__wrapper]
@22 = internal constant [2 x i8] c"(\00"
@23 = internal constant [3 x i8] c", \00"
@24 = internal constant [2 x i8] c")\00"

define internal { i64, i64 }* @Sample__HelloQ__body() {
entry:
  %0 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([21 x i8], [21 x i8]* @0, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %0)
  %q_a = call %Array* @__quantum__rt__qubit_allocate_array(i64 3)
  call void @__quantum__rt__array_update_alias_count(%Array* %q_a, i32 1)
  %q_b = call %Array* @__quantum__rt__qubit_allocate_array(i64 3)
  call void @__quantum__rt__array_update_alias_count(%Array* %q_b, i32 1)
  %a = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %q_a)
  %1 = getelementptr inbounds { %Array* }, { %Array* }* %a, i32 0, i32 0
  %2 = load %Array*, %Array** %1, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %2, i32 1)
  %3 = bitcast { %Array* }* %a to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %3, i32 1)
  %b = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %q_b)
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %b, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 1)
  %6 = bitcast { %Array* }* %b to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 1)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @1, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %7)
  call void @Microsoft__Quantum__Arithmetic__IncrementByInteger__body(i64 1, { %Array* }* %a)
  call void @Microsoft__Quantum__Arithmetic__IncrementByInteger__body(i64 4, { %Array* }* %b)
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @2, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %8)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_a)
  %9 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @3, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %9)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_b)
  %10 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %a)
  call void @Microsoft__Quantum__Canon__QFT__adj({ %Array* }* %10)
  %11 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %b)
  call void @Microsoft__Quantum__Canon__QFT__adj({ %Array* }* %11)
  %12 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @4, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %12)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_a)
  %13 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @5, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %13)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_b)
  call void @Microsoft__Quantum__Arithmetic__AddI__body({ %Array* }* %a, { %Array* }* %b)
  %14 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @6, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %14)
  %15 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @4, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %15)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_a)
  %16 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @5, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %16)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_b)
  %17 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @7, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %17)
  %18 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %a)
  call void @Microsoft__Quantum__Canon__QFT__body({ %Array* }* %18)
  %19 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %b)
  call void @Microsoft__Quantum__Canon__QFT__body({ %Array* }* %19)
  %20 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @8, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %20)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_a)
  %21 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @9, i32 0, i32 0))
  call void @__quantum__rt__message(%String* %21)
  call void @__quantum__qis__dumpregister__body(i8* null, %Array* %q_b)
  %22 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i64* getelementptr (i64, i64* null, i32 1) to i64), i64 2))
  %23 = bitcast %Tuple* %22 to { i64, i64 }*
  %24 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %23, i32 0, i32 0
  %25 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %23, i32 0, i32 1
  %26 = call i64 @Microsoft__Quantum__Arithmetic__MeasureInteger__body({ %Array* }* %a)
  %27 = call i64 @Microsoft__Quantum__Arithmetic__MeasureInteger__body({ %Array* }* %b)
  store i64 %26, i64* %24, align 4
  store i64 %27, i64* %25, align 4
  %28 = getelementptr inbounds { %Array* }, { %Array* }* %10, i32 0, i32 0
  %29 = load %Array*, %Array** %28, align 8
  %30 = getelementptr inbounds { %Array* }, { %Array* }* %11, i32 0, i32 0
  %31 = load %Array*, %Array** %30, align 8
  %32 = getelementptr inbounds { %Array* }, { %Array* }* %18, i32 0, i32 0
  %33 = load %Array*, %Array** %32, align 8
  %34 = getelementptr inbounds { %Array* }, { %Array* }* %19, i32 0, i32 0
  %35 = load %Array*, %Array** %34, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %q_b, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %2, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %q_a, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %2, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %9, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %29, i32 -1)
  %36 = bitcast { %Array* }* %10 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %36, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %31, i32 -1)
  %37 = bitcast { %Array* }* %11 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %37, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %12, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %13, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %14, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %15, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %16, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %17, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %33, i32 -1)
  %38 = bitcast { %Array* }* %18 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %38, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %35, i32 -1)
  %39 = bitcast { %Array* }* %19 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %39, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %20, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %21, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %0, i32 -1)
  call void @__quantum__rt__qubit_release_array(%Array* %q_b)
  call void @__quantum__rt__qubit_release_array(%Array* %q_a)
  ret { i64, i64 }* %23
}

declare %String* @__quantum__rt__string_create(i8*)

declare void @__quantum__rt__message(%String*)

declare %Qubit* @__quantum__rt__qubit_allocate()

declare %Array* @__quantum__rt__qubit_allocate_array(i64)

declare void @__quantum__rt__qubit_release_array(%Array*)

declare void @__quantum__rt__array_update_alias_count(%Array*, i32)

define internal { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %__Item1__) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 1)
  %0 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  %1 = bitcast %Tuple* %0 to { %Array* }*
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %1, i32 0, i32 0
  store %Array* %__Item1__, %Array** %2, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %__Item1__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 -1)
  ret { %Array* }* %1
}

declare void @__quantum__rt__tuple_update_alias_count(%Tuple*, i32)

define internal void @Microsoft__Quantum__Arithmetic__IncrementByInteger__body(i64 %increment, { %Array* }* %target) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ %Callable*, i64 }* getelementptr ({ %Callable*, i64 }, { %Callable*, i64 }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { %Callable*, i64 }*
  %5 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %4, i32 0, i32 1
  %7 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %7, %Callable** %5, align 8
  store i64 %increment, i64* %6, align 4
  %8 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__1__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__1__FunctionTable, %Tuple* %3)
  call void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__body(%Callable* %8, { %Array* }* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %8, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %8, i32 -1)
  ret void
}

declare void @__quantum__qis__dumpregister__body(i8*, %Array*)

define internal void @Microsoft__Quantum__Canon__QFT__adj({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndianAsLittleEndian__body({ %Array* }* %qs)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__adj({ %Array* }* %3)
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %3, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  %6 = bitcast { %Array* }* %3 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %input) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Array* @Microsoft__Quantum__Arrays___da24003d78a6494a9b43249d80017883_Reversed__body(%Array* %1)
  %4 = call { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndian__body(%Array* %3)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  ret { %Array* }* %4
}

define internal void @Microsoft__Quantum__Arithmetic__AddI__body({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %7 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %8 = icmp eq i64 %6, %7
  br i1 %8, label %then0__1, label %test1__1

then0__1:                                         ; preds = %entry
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__body({ %Array* }* %xs, { %Array* }* %ys)
  br label %continue__1

test1__1:                                         ; preds = %entry
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %11 = icmp sgt i64 %9, %10
  br i1 %11, label %then1__1, label %else__1

then1__1:                                         ; preds = %test1__1
  %12 = sub i64 %9, %10
  %13 = sub i64 %12, 1
  %qs = call %Array* @__quantum__rt__qubit_allocate_array(i64 %13)
  call void @__quantum__rt__array_update_alias_count(%Array* %qs, i32 1)
  %14 = call %Array* @__quantum__rt__array_concatenate(%Array* %1, %Array* %qs)
  %15 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %14)
  %16 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %4)
  %17 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %16)
  %18 = call %Qubit* @Microsoft__Quantum__Arrays___651e5e7f272044f08a0bf7935d1f86ab_Tail__body(%Array* %4)
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__body({ %Array* }* %15, { %Array* }* %17, %Qubit* %18)
  %19 = getelementptr inbounds { %Array* }, { %Array* }* %15, i32 0, i32 0
  %20 = load %Array*, %Array** %19, align 8
  %21 = getelementptr inbounds { %Array* }, { %Array* }* %17, i32 0, i32 0
  %22 = load %Array*, %Array** %21, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %qs, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %14, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %20, i32 -1)
  %23 = bitcast { %Array* }* %15 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %23, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %16, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %22, i32 -1)
  %24 = bitcast { %Array* }* %17 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %24, i32 -1)
  call void @__quantum__rt__qubit_release_array(%Array* %qs)
  br label %continue__1

else__1:                                          ; preds = %test1__1
  %25 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @21, i32 0, i32 0))
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__fail(%String* %25)
  unreachable

continue__1:                                      ; preds = %then1__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFT__body({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndianAsLittleEndian__body({ %Array* }* %qs)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__body({ %Array* }* %3)
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %3, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  %6 = bitcast { %Array* }* %3 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

declare %Tuple* @__quantum__rt__tuple_create(i64)

define internal i64 @Microsoft__Quantum__Arithmetic__MeasureInteger__body({ %Array* }* %target) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Result* @__quantum__rt__result_get_zero()
  %4 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %5 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 %4)
  %6 = sub i64 %4, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %7 = phi i64 [ 0, %entry ], [ %11, %exiting__1 ]
  %8 = icmp sle i64 %7, %6
  br i1 %8, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %9 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %5, i64 %7)
  %10 = bitcast i8* %9 to %Result**
  store %Result* %3, %Result** %10, align 8
  call void @__quantum__rt__result_update_reference_count(%Result* %3, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %11 = add i64 %7, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %results = alloca %Array*, align 8
  store %Array* %5, %Array** %results, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 1)
  %12 = sub i64 %4, 1
  br label %header__2

header__2:                                        ; preds = %exiting__2, %exit__1
  %idx = phi i64 [ 0, %exit__1 ], [ %24, %exiting__2 ]
  %13 = icmp sle i64 %idx, %12
  br i1 %13, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %14 = load %Array*, %Array** %results, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %14, i32 -1)
  %15 = call %Array* @__quantum__rt__array_copy(%Array* %14, i1 false)
  %16 = load %Array*, %Array** %0, align 8
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %16, i64 %idx)
  %18 = bitcast i8* %17 to %Qubit**
  %19 = load %Qubit*, %Qubit** %18, align 8
  %20 = call %Result* @Microsoft__Quantum__Measurement__MResetZ__body(%Qubit* %19)
  %21 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %15, i64 %idx)
  %22 = bitcast i8* %21 to %Result**
  %23 = load %Result*, %Result** %22, align 8
  call void @__quantum__rt__result_update_reference_count(%Result* %23, i32 -1)
  store %Result* %20, %Result** %22, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %15, i32 1)
  store %Array* %15, %Array** %results, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %14, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %24 = add i64 %idx, 1
  br label %header__2

exit__2:                                          ; preds = %header__2
  %25 = load %Array*, %Array** %results, align 8
  %26 = call i64 @Microsoft__Quantum__Convert__ResultArrayAsInt__body(%Array* %25)
  %27 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %27, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %25, i32 -1)
  %28 = call i64 @__quantum__rt__array_get_size_1d(%Array* %25)
  %29 = sub i64 %28, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %30 = phi i64 [ 0, %exit__2 ], [ %35, %exiting__3 ]
  %31 = icmp sle i64 %30, %29
  br i1 %31, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %32 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %25, i64 %30)
  %33 = bitcast i8* %32 to %Result**
  %34 = load %Result*, %Result** %33, align 8
  call void @__quantum__rt__result_update_reference_count(%Result* %34, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %35 = add i64 %30, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  call void @__quantum__rt__array_update_reference_count(%Array* %25, i32 -1)
  ret i64 %26
}

declare void @__quantum__rt__array_update_reference_count(%Array*, i32)

declare void @__quantum__rt__tuple_update_reference_count(%Tuple*, i32)

declare void @__quantum__rt__string_update_reference_count(%String*, i32)

define internal void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %actual, i1 %expected, %String* %message) {
entry:
  %0 = icmp ne i1 %actual, %expected
  br i1 %0, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  call void @Microsoft__Quantum__Diagnostics___100d9c7fc6324d1fa9974674fb5d71c5___QsRef1__FormattedFailure____body(i1 %actual, i1 %expected, %String* %message)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  ret void
}

define internal void @Microsoft__Quantum__Diagnostics___100d9c7fc6324d1fa9974674fb5d71c5___QsRef1__FormattedFailure____body(i1 %actual, i1 %expected, %String* %message) {
entry:
  %0 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @10, i32 0, i32 0))
  %1 = call %String* @__quantum__rt__string_concatenate(%String* %0, %String* %message)
  %2 = call %String* @__quantum__rt__string_concatenate(%String* %1, %String* %0)
  call void @__quantum__rt__string_update_reference_count(%String* %1, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %0, i32 -1)
  %3 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @11, i32 0, i32 0))
  %4 = call %String* @__quantum__rt__string_concatenate(%String* %2, %String* %3)
  call void @__quantum__rt__string_update_reference_count(%String* %2, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %3, i32 -1)
  br i1 %expected, label %condTrue__1, label %condFalse__1

condTrue__1:                                      ; preds = %entry
  %5 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @12, i32 0, i32 0))
  br label %condContinue__1

condFalse__1:                                     ; preds = %entry
  %6 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @13, i32 0, i32 0))
  br label %condContinue__1

condContinue__1:                                  ; preds = %condFalse__1, %condTrue__1
  %7 = phi %String* [ %5, %condTrue__1 ], [ %6, %condFalse__1 ]
  %8 = call %String* @__quantum__rt__string_concatenate(%String* %4, %String* %7)
  call void @__quantum__rt__string_update_reference_count(%String* %4, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  %9 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @14, i32 0, i32 0))
  %10 = call %String* @__quantum__rt__string_concatenate(%String* %8, %String* %9)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %9, i32 -1)
  br i1 %actual, label %condTrue__2, label %condFalse__2

condTrue__2:                                      ; preds = %condContinue__1
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @12, i32 0, i32 0))
  br label %condContinue__2

condFalse__2:                                     ; preds = %condContinue__1
  %12 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @13, i32 0, i32 0))
  br label %condContinue__2

condContinue__2:                                  ; preds = %condFalse__2, %condTrue__2
  %13 = phi %String* [ %11, %condTrue__2 ], [ %12, %condFalse__2 ]
  %14 = call %String* @__quantum__rt__string_concatenate(%String* %10, %String* %13)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %13, i32 -1)
  call void @__quantum__rt__fail(%String* %14)
  unreachable
}

define internal void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %actual, i64 %expected, %String* %message) {
entry:
  %0 = icmp ne i64 %actual, %expected
  br i1 %0, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  call void @Microsoft__Quantum__Diagnostics___fe8f6431b5f34ae7a9cfe3ccd7ea40f4___QsRef1__FormattedFailure____body(i64 %actual, i64 %expected, %String* %message)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  ret void
}

define internal void @Microsoft__Quantum__Diagnostics___fe8f6431b5f34ae7a9cfe3ccd7ea40f4___QsRef1__FormattedFailure____body(i64 %actual, i64 %expected, %String* %message) {
entry:
  %0 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @10, i32 0, i32 0))
  %1 = call %String* @__quantum__rt__string_concatenate(%String* %0, %String* %message)
  %2 = call %String* @__quantum__rt__string_concatenate(%String* %1, %String* %0)
  call void @__quantum__rt__string_update_reference_count(%String* %1, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %0, i32 -1)
  %3 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @11, i32 0, i32 0))
  %4 = call %String* @__quantum__rt__string_concatenate(%String* %2, %String* %3)
  call void @__quantum__rt__string_update_reference_count(%String* %2, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %3, i32 -1)
  %5 = call %String* @__quantum__rt__int_to_string(i64 %expected)
  %6 = call %String* @__quantum__rt__string_concatenate(%String* %4, %String* %5)
  call void @__quantum__rt__string_update_reference_count(%String* %4, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %5, i32 -1)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @14, i32 0, i32 0))
  %8 = call %String* @__quantum__rt__string_concatenate(%String* %6, %String* %7)
  call void @__quantum__rt__string_update_reference_count(%String* %6, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  %9 = call %String* @__quantum__rt__int_to_string(i64 %actual)
  %10 = call %String* @__quantum__rt__string_concatenate(%String* %8, %String* %9)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %9, i32 -1)
  call void @__quantum__rt__fail(%String* %10)
  unreachable
}

define internal void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %actual, %String* %message) {
entry:
  %0 = xor i1 %actual, true
  br i1 %0, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  call void @__quantum__rt__string_update_reference_count(%String* %message, i32 1)
  call void @__quantum__rt__fail(%String* %message)
  unreachable

continue__1:                                      ; preds = %entry
  ret void
}

declare void @__quantum__rt__fail(%String*)

declare %String* @__quantum__rt__string_concatenate(%String*, %String*)

declare %String* @__quantum__rt__int_to_string(i64)

define internal %Range @Microsoft__Quantum__Arrays___8b62ee2f8c734139a0a79ea89d6b17c1_IndexRange__body(%Array* %array) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = sub i64 %0, 1
  %2 = load %Range, %Range* @EmptyRange, align 4
  %3 = insertvalue %Range %2, i64 0, 0
  %4 = insertvalue %Range %3, i64 1, 1
  %5 = insertvalue %Range %4, i64 %1, 2
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  ret %Range %5
}

declare i64 @__quantum__rt__array_get_size_1d(%Array*)

define internal %Range @Microsoft__Quantum__Arrays___25a41074dac049fdba7e12ae3b973296_IndexRange__body(%Array* %array) {
entry:
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = sub i64 %0, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %2 = phi i64 [ 0, %entry ], [ %8, %exiting__1 ]
  %3 = icmp sle i64 %2, %1
  br i1 %3, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %4 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %array, i64 %2)
  %5 = bitcast i8* %4 to { %Qubit*, %Qubit* }**
  %6 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %5, align 8
  %7 = bitcast { %Qubit*, %Qubit* }* %6 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %7, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %8 = add i64 %2, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %9 = sub i64 %0, 1
  %10 = load %Range, %Range* @EmptyRange, align 4
  %11 = insertvalue %Range %10, i64 0, 0
  %12 = insertvalue %Range %11, i64 1, 1
  %13 = insertvalue %Range %12, i64 %9, 2
  %14 = sub i64 %0, 1
  br label %header__2

header__2:                                        ; preds = %exiting__2, %exit__1
  %15 = phi i64 [ 0, %exit__1 ], [ %21, %exiting__2 ]
  %16 = icmp sle i64 %15, %14
  br i1 %16, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %array, i64 %15)
  %18 = bitcast i8* %17 to { %Qubit*, %Qubit* }**
  %19 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %18, align 8
  %20 = bitcast { %Qubit*, %Qubit* }* %19 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %20, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %21 = add i64 %15, 1
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  ret %Range %13
}

declare i8* @__quantum__rt__array_get_element_ptr_1d(%Array*, i64)

define internal %Array* @Microsoft__Quantum__Arrays___b04b37c15ebd4965af7d2fde57ded96d_Mapped__body(%Callable* %mapper, %Array* %array) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %mapper, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %mapper, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = call %Array* @__quantum__rt__array_create_1d(i32 1, i64 %0)
  %2 = sub i64 %0, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %3 = phi i64 [ 0, %entry ], [ %7, %exiting__1 ]
  %4 = icmp sle i64 %3, %2
  br i1 %4, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %5 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 %3)
  %6 = bitcast i8* %5 to i1*
  store i1 false, i1* %6, align 1
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %7 = add i64 %3, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %resultArray = alloca %Array*, align 8
  store %Array* %1, %Array** %resultArray, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %8 = call %Range @Microsoft__Quantum__Arrays___8b62ee2f8c734139a0a79ea89d6b17c1_IndexRange__body(%Array* %array)
  %9 = extractvalue %Range %8, 0
  %10 = extractvalue %Range %8, 1
  %11 = extractvalue %Range %8, 2
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  %12 = icmp sgt i64 %10, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %idxElement = phi i64 [ %9, %preheader__1 ], [ %31, %exiting__2 ]
  %13 = icmp sle i64 %idxElement, %11
  %14 = icmp sge i64 %idxElement, %11
  %15 = select i1 %12, i1 %13, i1 %14
  br i1 %15, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %16 = load %Array*, %Array** %resultArray, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %16, i32 -1)
  %17 = call %Array* @__quantum__rt__array_copy(%Array* %16, i1 false)
  %18 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %array, i64 %idxElement)
  %19 = bitcast i8* %18 to %Result**
  %20 = load %Result*, %Result** %19, align 8
  %21 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  %22 = bitcast %Tuple* %21 to { %Result* }*
  %23 = getelementptr inbounds { %Result* }, { %Result* }* %22, i32 0, i32 0
  store %Result* %20, %Result** %23, align 8
  %24 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1* getelementptr (i1, i1* null, i32 1) to i64))
  call void @__quantum__rt__callable_invoke(%Callable* %mapper, %Tuple* %21, %Tuple* %24)
  %25 = bitcast %Tuple* %24 to { i1 }*
  %26 = getelementptr inbounds { i1 }, { i1 }* %25, i32 0, i32 0
  %27 = load i1, i1* %26, align 1
  %28 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %17, i64 %idxElement)
  %29 = bitcast i8* %28 to i1*
  %30 = load i1, i1* %29, align 1
  store i1 %27, i1* %29, align 1
  call void @__quantum__rt__array_update_alias_count(%Array* %17, i32 1)
  store %Array* %17, %Array** %resultArray, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %16, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %21, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %24, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %31 = add i64 %idxElement, %10
  br label %header__2

exit__2:                                          ; preds = %header__2
  %32 = load %Array*, %Array** %resultArray, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %mapper, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %mapper, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %32, i32 -1)
  ret %Array* %32
}

declare void @__quantum__rt__capture_update_alias_count(%Callable*, i32)

declare void @__quantum__rt__callable_update_alias_count(%Callable*, i32)

declare %Array* @__quantum__rt__array_create_1d(i32, i64)

declare %Array* @__quantum__rt__array_copy(%Array*, i1)

declare void @__quantum__rt__callable_invoke(%Callable*, %Tuple*, %Tuple*)

define internal %Array* @Microsoft__Quantum__Arrays___da24003d78a6494a9b43249d80017883_Reversed__body(%Array* %array) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %nElements = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %0 = sub i64 %nElements, 1
  %1 = load %Range, %Range* @EmptyRange, align 4
  %2 = insertvalue %Range %1, i64 %0, 0
  %3 = insertvalue %Range %2, i64 -1, 1
  %4 = insertvalue %Range %3, i64 0, 2
  %5 = call %Array* @__quantum__rt__array_slice_1d(%Array* %array, %Range %4, i1 true)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  ret %Array* %5
}

declare %Array* @__quantum__rt__array_slice_1d(%Array*, %Range, i1)

define internal %Qubit* @Microsoft__Quantum__Arrays___651e5e7f272044f08a0bf7935d1f86ab_Tail__body(%Array* %array) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = icmp sgt i64 %0, 0
  %2 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([39 x i8], [39 x i8]* @15, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %1, i1 true, %String* %2)
  %3 = sub i64 %0, 1
  %4 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %array, i64 %3)
  %5 = bitcast i8* %4 to %Qubit**
  %6 = load %Qubit*, %Qubit** %5, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %2, i32 -1)
  ret %Qubit* %6
}

define internal %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %array) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = sub i64 %0, 2
  %2 = load %Range, %Range* @EmptyRange, align 4
  %3 = insertvalue %Range %2, i64 0, 0
  %4 = insertvalue %Range %3, i64 1, 1
  %5 = insertvalue %Range %4, i64 %1, 2
  %6 = call %Array* @__quantum__rt__array_slice_1d(%Array* %array, %Range %5, i1 true)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  ret %Array* %6
}

define internal %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %array) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %array)
  %1 = sub i64 %0, 1
  %2 = load %Range, %Range* @EmptyRange, align 4
  %3 = insertvalue %Range %2, i64 1, 0
  %4 = insertvalue %Range %3, i64 1, 1
  %5 = insertvalue %Range %4, i64 %1, 2
  %6 = call %Array* @__quantum__rt__array_slice_1d(%Array* %array, %Range %5, i1 true)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %array, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  ret %Array* %6
}

define internal %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %left, %Array* %right) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %left, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %right, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %left)
  %1 = call i64 @__quantum__rt__array_get_size_1d(%Array* %right)
  %2 = icmp slt i64 %0, %1
  br i1 %2, label %condTrue__1, label %condFalse__1

condTrue__1:                                      ; preds = %entry
  br label %condContinue__1

condFalse__1:                                     ; preds = %entry
  br label %condContinue__1

condContinue__1:                                  ; preds = %condFalse__1, %condTrue__1
  %nElements = phi i64 [ %0, %condTrue__1 ], [ %1, %condFalse__1 ]
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Qubit*, %Qubit* }*
  %5 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 1
  store %Qubit* null, %Qubit** %5, align 8
  store %Qubit* null, %Qubit** %6, align 8
  %7 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 %nElements)
  %8 = sub i64 %nElements, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %condContinue__1
  %9 = phi i64 [ 0, %condContinue__1 ], [ %13, %exiting__1 ]
  %10 = icmp sle i64 %9, %8
  br i1 %10, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %11 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 %9)
  %12 = bitcast i8* %11 to { %Qubit*, %Qubit* }**
  store { %Qubit*, %Qubit* }* %4, { %Qubit*, %Qubit* }** %12, align 8
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %13 = add i64 %9, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %output = alloca %Array*, align 8
  store %Array* %7, %Array** %output, align 8
  %14 = sub i64 %nElements, 1
  br label %header__2

header__2:                                        ; preds = %exiting__2, %exit__1
  %15 = phi i64 [ 0, %exit__1 ], [ %21, %exiting__2 ]
  %16 = icmp sle i64 %15, %14
  br i1 %16, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 %15)
  %18 = bitcast i8* %17 to { %Qubit*, %Qubit* }**
  %19 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %18, align 8
  %20 = bitcast { %Qubit*, %Qubit* }* %19 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %20, i32 1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %21 = add i64 %15, 1
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %22 = sub i64 %nElements, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %idxElement = phi i64 [ 0, %exit__2 ], [ %40, %exiting__3 ]
  %23 = icmp sle i64 %idxElement, %22
  br i1 %23, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %24 = load %Array*, %Array** %output, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %24, i32 -1)
  %25 = call %Array* @__quantum__rt__array_copy(%Array* %24, i1 false)
  %26 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %27 = bitcast %Tuple* %26 to { %Qubit*, %Qubit* }*
  %28 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %27, i32 0, i32 0
  %29 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %27, i32 0, i32 1
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %left, i64 %idxElement)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  %33 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %right, i64 %idxElement)
  %34 = bitcast i8* %33 to %Qubit**
  %35 = load %Qubit*, %Qubit** %34, align 8
  store %Qubit* %32, %Qubit** %28, align 8
  store %Qubit* %35, %Qubit** %29, align 8
  %36 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %25, i64 %idxElement)
  %37 = bitcast i8* %36 to { %Qubit*, %Qubit* }**
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %26, i32 1)
  %38 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %37, align 8
  %39 = bitcast { %Qubit*, %Qubit* }* %38 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %39, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %39, i32 -1)
  store { %Qubit*, %Qubit* }* %27, { %Qubit*, %Qubit* }** %37, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %25, i32 1)
  store %Array* %25, %Array** %output, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %24, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %40 = add i64 %idxElement, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  %41 = load %Array*, %Array** %output, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %left, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %right, i32 -1)
  %42 = call i64 @__quantum__rt__array_get_size_1d(%Array* %41)
  %43 = sub i64 %42, 1
  br label %header__4

header__4:                                        ; preds = %exiting__4, %exit__3
  %44 = phi i64 [ 0, %exit__3 ], [ %50, %exiting__4 ]
  %45 = icmp sle i64 %44, %43
  br i1 %45, label %body__4, label %exit__4

body__4:                                          ; preds = %header__4
  %46 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %41, i64 %44)
  %47 = bitcast i8* %46 to { %Qubit*, %Qubit* }**
  %48 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %47, align 8
  %49 = bitcast { %Qubit*, %Qubit* }* %48 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %49, i32 -1)
  br label %exiting__4

exiting__4:                                       ; preds = %body__4
  %50 = add i64 %44, 1
  br label %header__4

exit__4:                                          ; preds = %header__4
  call void @__quantum__rt__array_update_alias_count(%Array* %41, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret %Array* %41
}

define internal i64 @Microsoft__Quantum__Convert__BoolArrayAsInt__body(%Array* %bits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %bits, i32 1)
  %nBits = call i64 @__quantum__rt__array_get_size_1d(%Array* %bits)
  %0 = icmp slt i64 %nBits, 64
  %1 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([46 x i8], [46 x i8]* @16, i32 0, i32 0))
  %2 = call %String* @__quantum__rt__int_to_string(i64 %nBits)
  %3 = call %String* @__quantum__rt__string_concatenate(%String* %1, %String* %2)
  call void @__quantum__rt__string_update_reference_count(%String* %1, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %2, i32 -1)
  %4 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @17, i32 0, i32 0))
  %5 = call %String* @__quantum__rt__string_concatenate(%String* %3, %String* %4)
  call void @__quantum__rt__string_update_reference_count(%String* %3, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %4, i32 -1)
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %0, %String* %5)
  %number = alloca i64, align 8
  store i64 0, i64* %number, align 4
  %6 = sub i64 %nBits, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %idxBit = phi i64 [ 0, %entry ], [ %16, %exiting__1 ]
  %7 = icmp sle i64 %idxBit, %6
  br i1 %7, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %8 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %bits, i64 %idxBit)
  %9 = bitcast i8* %8 to i1*
  %10 = load i1, i1* %9, align 1
  br i1 %10, label %then0__1, label %continue__1

then0__1:                                         ; preds = %body__1
  %11 = load i64, i64* %number, align 4
  %12 = trunc i64 %idxBit to i32
  %13 = call double @llvm.powi.f64(double 2.000000e+00, i32 %12)
  %14 = fptosi double %13 to i64
  %15 = add i64 %11, %14
  store i64 %15, i64* %number, align 4
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %body__1
  br label %exiting__1

exiting__1:                                       ; preds = %continue__1
  %16 = add i64 %idxBit, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %17 = load i64, i64* %number, align 4
  call void @__quantum__rt__array_update_alias_count(%Array* %bits, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %5, i32 -1)
  ret i64 %17
}

; Function Attrs: nounwind readnone speculatable willreturn
declare double @llvm.powi.f64(double, i32) #0

define internal %Array* @Microsoft__Quantum__Convert__ResultArrayAsBoolArray__body(%Array* %input) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %input, i32 1)
  %0 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Convert__ResultAsBool__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %1 = call %Array* @Microsoft__Quantum__Arrays___b04b37c15ebd4965af7d2fde57ded96d_Mapped__body(%Callable* %0, %Array* %input)
  call void @__quantum__rt__array_update_alias_count(%Array* %input, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %0, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %0, i32 -1)
  ret %Array* %1
}

define internal void @Microsoft__Quantum__Convert__ResultAsBool__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Result* }*
  %1 = getelementptr inbounds { %Result* }, { %Result* }* %0, i32 0, i32 0
  %2 = load %Result*, %Result** %1, align 8
  %3 = call i1 @Microsoft__Quantum__Convert__ResultAsBool__body(%Result* %2)
  %4 = bitcast %Tuple* %result-tuple to { i1 }*
  %5 = getelementptr inbounds { i1 }, { i1 }* %4, i32 0, i32 0
  store i1 %3, i1* %5, align 1
  ret void
}

declare %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]*, [2 x void (%Tuple*, i32)*]*, %Tuple*)

declare void @__quantum__rt__capture_update_reference_count(%Callable*, i32)

declare void @__quantum__rt__callable_update_reference_count(%Callable*, i32)

define internal i1 @Microsoft__Quantum__Convert__ResultAsBool__body(%Result* %input) {
entry:
  %0 = call %Result* @__quantum__rt__result_get_zero()
  %1 = call i1 @__quantum__rt__result_equal(%Result* %input, %Result* %0)
  %2 = select i1 %1, i1 false, i1 true
  ret i1 %2
}

define internal i64 @Microsoft__Quantum__Convert__ResultArrayAsInt__body(%Array* %results) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %results, i32 1)
  %0 = call %Array* @Microsoft__Quantum__Convert__ResultArrayAsBoolArray__body(%Array* %results)
  %1 = call i64 @Microsoft__Quantum__Convert__BoolArrayAsInt__body(%Array* %0)
  call void @__quantum__rt__array_update_alias_count(%Array* %results, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %0, i32 -1)
  ret i64 %1
}

declare %Result* @__quantum__rt__result_get_zero()

declare i1 @__quantum__rt__result_equal(%Result*, %Result*)

define internal double @Microsoft__Quantum__Math__PI__body() {
entry:
  ret double 0x400921FB54442D18
}

define internal void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %control1, %Qubit* %control2, %Qubit* %target) {
entry:
  %__controlQubits__ = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 2)
  %0 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %__controlQubits__, i64 0)
  %1 = bitcast i8* %0 to %Qubit**
  %2 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %__controlQubits__, i64 1)
  %3 = bitcast i8* %2 to %Qubit**
  store %Qubit* %control1, %Qubit** %1, align 8
  store %Qubit* %control2, %Qubit** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__, %Qubit* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

declare void @__quantum__qis__x__ctl(%Array*, %Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %control1, %Qubit* %control2, %Qubit* %target) {
entry:
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %control1, %Qubit* %control2, %Qubit* %target)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CCNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %control1 = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %control2 = load %Qubit*, %Qubit** %2, align 8
  %3 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 2
  %target = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 2)
  %5 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %6 = bitcast i8* %5 to %Qubit**
  %7 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 1)
  %8 = bitcast i8* %7 to %Qubit**
  store %Qubit* %control1, %Qubit** %6, align 8
  store %Qubit* %control2, %Qubit** %8, align 8
  %__controlQubits__1 = call %Array* @__quantum__rt__array_concatenate(%Array* %__controlQubits__, %Array* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__1, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__1, %Qubit* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__1, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__1, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

declare %Array* @__quantum__rt__array_concatenate(%Array*, %Array*)

define internal void @Microsoft__Quantum__Intrinsic__CCNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %control1 = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %control2 = load %Qubit*, %Qubit** %2, align 8
  %3 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %0, i32 0, i32 2
  %target = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %5 = bitcast %Tuple* %4 to { %Qubit*, %Qubit*, %Qubit* }*
  %6 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %5, i32 0, i32 0
  %7 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %5, i32 0, i32 1
  %8 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %5, i32 0, i32 2
  store %Qubit* %control1, %Qubit** %6, align 8
  store %Qubit* %control2, %Qubit** %7, align 8
  store %Qubit* %target, %Qubit** %8, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit*, %Qubit* }* %5)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %control, %Qubit* %target) {
entry:
  %__controlQubits__ = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %0 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %__controlQubits__, i64 0)
  %1 = bitcast i8* %0 to %Qubit**
  store %Qubit* %control, %Qubit** %1, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__, %Qubit* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %control, %Qubit* %target) {
entry:
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %control, %Qubit* %target)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %control = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %target = load %Qubit*, %Qubit** %2, align 8
  %3 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %4 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %5 = bitcast i8* %4 to %Qubit**
  store %Qubit* %control, %Qubit** %5, align 8
  %__controlQubits__1 = call %Array* @__quantum__rt__array_concatenate(%Array* %__controlQubits__, %Array* %3)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__1, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__1, %Qubit* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__1, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__1, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %control = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %target = load %Qubit*, %Qubit** %2, align 8
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Qubit*, %Qubit* }*
  %5 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 1
  store %Qubit* %control, %Qubit** %5, align 8
  store %Qubit* %target, %Qubit** %6, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__H__body(%Qubit* %qubit) {
entry:
  call void @__quantum__qis__h__body(%Qubit* %qubit)
  ret void
}

declare void @__quantum__qis__h__body(%Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__H__adj(%Qubit* %qubit) {
entry:
  call void @__quantum__qis__h__body(%Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__H__ctl(%Array* %__controlQubits__, %Qubit* %qubit) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__h__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

declare void @__quantum__qis__h__ctl(%Array*, %Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__H__ctladj(%Array* %__controlQubits__, %Qubit* %qubit) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__h__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal %Result* @Microsoft__Quantum__Intrinsic__M__body(%Qubit* %qubit) {
entry:
  %bases = call %Array* @__quantum__rt__array_create_1d(i32 1, i64 1)
  %0 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %bases, i64 0)
  %1 = bitcast i8* %0 to i2*
  %2 = load i2, i2* @PauliZ, align 1
  store i2 %2, i2* %1, align 1
  call void @__quantum__rt__array_update_alias_count(%Array* %bases, i32 1)
  %qubits = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %3 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %qubits, i64 0)
  %4 = bitcast i8* %3 to %Qubit**
  store %Qubit* %qubit, %Qubit** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %5 = call %Result* @__quantum__qis__measure__body(%Array* %bases, %Array* %qubits)
  call void @__quantum__rt__array_update_alias_count(%Array* %bases, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %bases, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %qubits, i32 -1)
  ret %Result* %5
}

declare %Result* @__quantum__qis__measure__body(%Array*, %Array*)

define internal %Result* @Microsoft__Quantum__Intrinsic__Measure__body(%Array* %bases, %Array* %qubits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %bases, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %0 = call %Result* @__quantum__qis__measure__body(%Array* %bases, %Array* %qubits)
  call void @__quantum__rt__array_update_alias_count(%Array* %bases, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  ret %Result* %0
}

define internal void @Microsoft__Quantum__Intrinsic__R__body(i2 %pauli, double %theta, %Qubit* %qubit) {
entry:
  call void @__quantum__qis__r__body(i2 %pauli, double %theta, %Qubit* %qubit)
  ret void
}

declare void @__quantum__qis__r__body(i2, double, %Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__R__adj(i2 %pauli, double %theta, %Qubit* %qubit) {
entry:
  call void @__quantum__qis__r__adj(i2 %pauli, double %theta, %Qubit* %qubit)
  ret void
}

declare void @__quantum__qis__r__adj(i2, double, %Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__R__ctl(%Array* %__controlQubits__, { i2, double, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 0
  %pauli = load i2, i2* %1, align 1
  %2 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 1
  %theta = load double, double* %2, align 8
  %3 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 2
  %qubit = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, double, %Qubit* }* getelementptr ({ i2, double, %Qubit* }, { i2, double, %Qubit* }* null, i32 1) to i64))
  %5 = bitcast %Tuple* %4 to { i2, double, %Qubit* }*
  %6 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 0
  %7 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 1
  %8 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 2
  store i2 %pauli, i2* %6, align 1
  store double %theta, double* %7, align 8
  store %Qubit* %qubit, %Qubit** %8, align 8
  call void @__quantum__qis__r__ctl(%Array* %__controlQubits__, { i2, double, %Qubit* }* %5)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  ret void
}

declare void @__quantum__qis__r__ctl(%Array*, { i2, double, %Qubit* }*)

define internal void @Microsoft__Quantum__Intrinsic__R__ctladj(%Array* %__controlQubits__, { i2, double, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 0
  %pauli = load i2, i2* %1, align 1
  %2 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 1
  %theta = load double, double* %2, align 8
  %3 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %0, i32 0, i32 2
  %qubit = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, double, %Qubit* }* getelementptr ({ i2, double, %Qubit* }, { i2, double, %Qubit* }* null, i32 1) to i64))
  %5 = bitcast %Tuple* %4 to { i2, double, %Qubit* }*
  %6 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 0
  %7 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 1
  %8 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %5, i32 0, i32 2
  store i2 %pauli, i2* %6, align 1
  store double %theta, double* %7, align 8
  store %Qubit* %qubit, %Qubit** %8, align 8
  call void @__quantum__qis__r__ctladj(%Array* %__controlQubits__, { i2, double, %Qubit* }* %5)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  ret void
}

declare void @__quantum__qis__r__ctladj(%Array*, { i2, double, %Qubit* }*)

define internal void @Microsoft__Quantum__Intrinsic__R1Frac__body(i64 %numerator, i64 %power, %Qubit* %qubit) {
entry:
  %0 = load i2, i2* @PauliZ, align 1
  %1 = sub i64 0, %numerator
  %2 = add i64 %power, 1
  call void @Microsoft__Quantum__Intrinsic__RFrac__body(i2 %0, i64 %1, i64 %2, %Qubit* %qubit)
  %3 = load i2, i2* @PauliI, align 1
  %4 = add i64 %power, 1
  call void @Microsoft__Quantum__Intrinsic__RFrac__body(i2 %3, i64 %numerator, i64 %4, %Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__RFrac__body(i2 %pauli, i64 %numerator, i64 %power, %Qubit* %qubit) {
entry:
  %0 = call double @Microsoft__Quantum__Math__PI__body()
  %1 = fmul double -2.000000e+00, %0
  %2 = sitofp i64 %numerator to double
  %3 = fmul double %1, %2
  %4 = sitofp i64 %power to double
  %5 = call double @llvm.pow.f64(double 2.000000e+00, double %4)
  %angle = fdiv double %3, %5
  call void @__quantum__qis__r__body(i2 %pauli, double %angle, %Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__R1Frac__adj(i64 %numerator, i64 %power, %Qubit* %qubit) {
entry:
  %0 = load i2, i2* @PauliI, align 1
  %1 = add i64 %power, 1
  call void @Microsoft__Quantum__Intrinsic__RFrac__adj(i2 %0, i64 %numerator, i64 %1, %Qubit* %qubit)
  %2 = load i2, i2* @PauliZ, align 1
  %3 = sub i64 0, %numerator
  %4 = add i64 %power, 1
  call void @Microsoft__Quantum__Intrinsic__RFrac__adj(i2 %2, i64 %3, i64 %4, %Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__RFrac__adj(i2 %pauli, i64 %numerator, i64 %power, %Qubit* %qubit) {
entry:
  %0 = call double @Microsoft__Quantum__Math__PI__body()
  %1 = fmul double -2.000000e+00, %0
  %2 = sitofp i64 %numerator to double
  %3 = fmul double %1, %2
  %4 = sitofp i64 %power to double
  %5 = call double @llvm.pow.f64(double 2.000000e+00, double %4)
  %__qsVar0__angle__ = fdiv double %3, %5
  call void @__quantum__qis__r__adj(i2 %pauli, double %__qsVar0__angle__, %Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__R1Frac__ctl(%Array* %__controlQubits__, { i64, i64, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 0
  %numerator = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 1
  %power = load i64, i64* %2, align 4
  %3 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 2
  %qubit = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, i64, i64, %Qubit* }* getelementptr ({ i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* null, i32 1) to i64))
  %5 = bitcast %Tuple* %4 to { i2, i64, i64, %Qubit* }*
  %6 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 0
  %7 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 1
  %8 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 2
  %9 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 3
  %10 = load i2, i2* @PauliZ, align 1
  %11 = sub i64 0, %numerator
  %12 = add i64 %power, 1
  store i2 %10, i2* %6, align 1
  store i64 %11, i64* %7, align 4
  store i64 %12, i64* %8, align 4
  store %Qubit* %qubit, %Qubit** %9, align 8
  call void @Microsoft__Quantum__Intrinsic__RFrac__ctl(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %5)
  %13 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, i64, i64, %Qubit* }* getelementptr ({ i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* null, i32 1) to i64))
  %14 = bitcast %Tuple* %13 to { i2, i64, i64, %Qubit* }*
  %15 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %14, i32 0, i32 0
  %16 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %14, i32 0, i32 1
  %17 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %14, i32 0, i32 2
  %18 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %14, i32 0, i32 3
  %19 = load i2, i2* @PauliI, align 1
  %20 = add i64 %power, 1
  store i2 %19, i2* %15, align 1
  store i64 %numerator, i64* %16, align 4
  store i64 %20, i64* %17, align 4
  store %Qubit* %qubit, %Qubit** %18, align 8
  call void @Microsoft__Quantum__Intrinsic__RFrac__ctl(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %14)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__RFrac__ctl(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 0
  %pauli = load i2, i2* %1, align 1
  %2 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 1
  %numerator = load i64, i64* %2, align 4
  %3 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 2
  %power = load i64, i64* %3, align 4
  %4 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 3
  %qubit = load %Qubit*, %Qubit** %4, align 8
  %5 = call double @Microsoft__Quantum__Math__PI__body()
  %6 = fmul double -2.000000e+00, %5
  %7 = sitofp i64 %numerator to double
  %8 = fmul double %6, %7
  %9 = sitofp i64 %power to double
  %10 = call double @llvm.pow.f64(double 2.000000e+00, double %9)
  %angle = fdiv double %8, %10
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %11 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, double, %Qubit* }* getelementptr ({ i2, double, %Qubit* }, { i2, double, %Qubit* }* null, i32 1) to i64))
  %12 = bitcast %Tuple* %11 to { i2, double, %Qubit* }*
  %13 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 0
  %14 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 1
  %15 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 2
  store i2 %pauli, i2* %13, align 1
  store double %angle, double* %14, align 8
  store %Qubit* %qubit, %Qubit** %15, align 8
  call void @__quantum__qis__r__ctl(%Array* %__controlQubits__, { i2, double, %Qubit* }* %12)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %11, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__R1Frac__ctladj(%Array* %__controlQubits__, { i64, i64, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 0
  %numerator = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 1
  %power = load i64, i64* %2, align 4
  %3 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %0, i32 0, i32 2
  %qubit = load %Qubit*, %Qubit** %3, align 8
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, i64, i64, %Qubit* }* getelementptr ({ i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* null, i32 1) to i64))
  %5 = bitcast %Tuple* %4 to { i2, i64, i64, %Qubit* }*
  %6 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 0
  %7 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 1
  %8 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 2
  %9 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %5, i32 0, i32 3
  %10 = load i2, i2* @PauliI, align 1
  %11 = add i64 %power, 1
  store i2 %10, i2* %6, align 1
  store i64 %numerator, i64* %7, align 4
  store i64 %11, i64* %8, align 4
  store %Qubit* %qubit, %Qubit** %9, align 8
  call void @Microsoft__Quantum__Intrinsic__RFrac__ctladj(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %5)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, i64, i64, %Qubit* }* getelementptr ({ i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* null, i32 1) to i64))
  %13 = bitcast %Tuple* %12 to { i2, i64, i64, %Qubit* }*
  %14 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %13, i32 0, i32 2
  %17 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %13, i32 0, i32 3
  %18 = load i2, i2* @PauliZ, align 1
  %19 = sub i64 0, %numerator
  %20 = add i64 %power, 1
  store i2 %18, i2* %14, align 1
  store i64 %19, i64* %15, align 4
  store i64 %20, i64* %16, align 4
  store %Qubit* %qubit, %Qubit** %17, align 8
  call void @Microsoft__Quantum__Intrinsic__RFrac__ctladj(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %13)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__RFrac__ctladj(%Array* %__controlQubits__, { i2, i64, i64, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 0
  %pauli = load i2, i2* %1, align 1
  %2 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 1
  %numerator = load i64, i64* %2, align 4
  %3 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 2
  %power = load i64, i64* %3, align 4
  %4 = getelementptr inbounds { i2, i64, i64, %Qubit* }, { i2, i64, i64, %Qubit* }* %0, i32 0, i32 3
  %qubit = load %Qubit*, %Qubit** %4, align 8
  %5 = call double @Microsoft__Quantum__Math__PI__body()
  %6 = fmul double -2.000000e+00, %5
  %7 = sitofp i64 %numerator to double
  %8 = fmul double %6, %7
  %9 = sitofp i64 %power to double
  %10 = call double @llvm.pow.f64(double 2.000000e+00, double %9)
  %__qsVar0__angle__ = fdiv double %8, %10
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %11 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i2, double, %Qubit* }* getelementptr ({ i2, double, %Qubit* }, { i2, double, %Qubit* }* null, i32 1) to i64))
  %12 = bitcast %Tuple* %11 to { i2, double, %Qubit* }*
  %13 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 0
  %14 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 1
  %15 = getelementptr inbounds { i2, double, %Qubit* }, { i2, double, %Qubit* }* %12, i32 0, i32 2
  store i2 %pauli, i2* %13, align 1
  store double %__qsVar0__angle__, double* %14, align 8
  store %Qubit* %qubit, %Qubit** %15, align 8
  call void @__quantum__qis__r__ctladj(%Array* %__controlQubits__, { i2, double, %Qubit* }* %12)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %11, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

; Function Attrs: nounwind readnone speculatable willreturn
declare double @llvm.pow.f64(double, double) #0

define internal void @Microsoft__Quantum__Intrinsic__SWAP__body(%Qubit* %qubit1, %Qubit* %qubit2) {
entry:
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %qubit1, %Qubit* %qubit2)
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %qubit2, %Qubit* %qubit1)
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %qubit1, %Qubit* %qubit2)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__SWAP__adj(%Qubit* %qubit1, %Qubit* %qubit2) {
entry:
  call void @Microsoft__Quantum__Intrinsic__SWAP__body(%Qubit* %qubit1, %Qubit* %qubit2)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__SWAP__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %qubit1 = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %qubit2 = load %Qubit*, %Qubit** %2, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %qubit1, %Qubit* %qubit2)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Qubit*, %Qubit* }*
  %5 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 1
  store %Qubit* %qubit2, %Qubit** %5, align 8
  store %Qubit* %qubit1, %Qubit** %6, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %4)
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %qubit1, %Qubit* %qubit2)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__SWAP__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %qubit1 = load %Qubit*, %Qubit** %1, align 8
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %qubit2 = load %Qubit*, %Qubit** %2, align 8
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Qubit*, %Qubit* }*
  %5 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %4, i32 0, i32 1
  store %Qubit* %qubit1, %Qubit** %5, align 8
  store %Qubit* %qubit2, %Qubit** %6, align 8
  call void @Microsoft__Quantum__Intrinsic__SWAP__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__X__body(%Qubit* %qubit) {
entry:
  call void @__quantum__qis__x__body(%Qubit* %qubit)
  ret void
}

declare void @__quantum__qis__x__body(%Qubit*)

define internal void @Microsoft__Quantum__Intrinsic__X__adj(%Qubit* %qubit) {
entry:
  call void @__quantum__qis__x__body(%Qubit* %qubit)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__X__ctl(%Array* %__controlQubits__, %Qubit* %qubit) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__X__ctladj(%Array* %__controlQubits__, %Qubit* %qubit) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__qis__x__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____body({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  call void @Microsoft__Quantum__Canon__ApproximateQFT__body(i64 %3, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApproximateQFT__body(i64 %a, { %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %3 = icmp sgt i64 %nQubits, 0
  %4 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @18, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %3, %String* %4)
  %5 = icmp sgt i64 %a, 0
  br i1 %5, label %condTrue__1, label %condContinue__1

condTrue__1:                                      ; preds = %entry
  %6 = icmp sle i64 %a, %nQubits
  br label %condContinue__1

condContinue__1:                                  ; preds = %condTrue__1, %entry
  %7 = phi i1 [ %6, %condTrue__1 ], [ %5, %entry ]
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @19, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %7, %String* %8)
  %9 = sub i64 %nQubits, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %condContinue__1
  %i = phi i64 [ 0, %condContinue__1 ], [ %12, %exiting__1 ]
  %10 = icmp sle i64 %i, %9
  br i1 %10, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %11 = sub i64 %i, 1
  br label %header__2

exiting__1:                                       ; preds = %exit__2
  %12 = add i64 %i, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %13 = load %Array*, %Array** %0, align 8
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__body(%Array* %13)
  call void @__quantum__rt__array_update_alias_count(%Array* %13, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %4, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  ret void

header__2:                                        ; preds = %exiting__2, %body__1
  %j = phi i64 [ 0, %body__1 ], [ %33, %exiting__2 ]
  %14 = icmp sle i64 %j, %11
  br i1 %14, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %15 = sub i64 %i, %j
  %16 = icmp slt i64 %15, %a
  br i1 %16, label %then0__1, label %continue__1

then0__1:                                         ; preds = %body__2
  %17 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %18 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %17, i64 0)
  %19 = bitcast i8* %18 to %Qubit**
  %20 = load %Array*, %Array** %0, align 8
  %21 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %20, i64 %i)
  %22 = bitcast i8* %21 to %Qubit**
  %23 = load %Qubit*, %Qubit** %22, align 8
  store %Qubit* %23, %Qubit** %19, align 8
  %24 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %25 = bitcast %Tuple* %24 to { i64, i64, %Qubit* }*
  %26 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %25, i32 0, i32 0
  %27 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %25, i32 0, i32 1
  %28 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %25, i32 0, i32 2
  %29 = sub i64 %i, %j
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %20, i64 %j)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  store i64 1, i64* %26, align 4
  store i64 %29, i64* %27, align 4
  store %Qubit* %32, %Qubit** %28, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctl(%Array* %17, { i64, i64, %Qubit* }* %25)
  call void @__quantum__rt__array_update_reference_count(%Array* %17, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %24, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %body__2
  br label %exiting__2

exiting__2:                                       ; preds = %continue__1
  %33 = add i64 %j, 1
  br label %header__2

exit__2:                                          ; preds = %header__2
  %34 = load %Array*, %Array** %0, align 8
  %35 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %34, i64 %i)
  %36 = bitcast i8* %35 to %Qubit**
  %qubit = load %Qubit*, %Qubit** %36, align 8
  call void @__quantum__qis__h__body(%Qubit* %qubit)
  br label %exiting__1
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____adj({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  call void @Microsoft__Quantum__Canon__ApproximateQFT__adj(i64 %3, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApproximateQFT__adj(i64 %a, { %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %3 = icmp sgt i64 %__qsVar0__nQubits__, 0
  %4 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @18, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %3, %String* %4)
  %5 = icmp sgt i64 %a, 0
  br i1 %5, label %condTrue__1, label %condContinue__1

condTrue__1:                                      ; preds = %entry
  %6 = icmp sle i64 %a, %__qsVar0__nQubits__
  br label %condContinue__1

condContinue__1:                                  ; preds = %condTrue__1, %entry
  %7 = phi i1 [ %6, %condTrue__1 ], [ %5, %entry ]
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @19, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %7, %String* %8)
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__adj(%Array* %1)
  %9 = sub i64 %__qsVar0__nQubits__, 1
  %10 = sub i64 %9, 0
  %11 = sdiv i64 %10, 1
  %12 = mul i64 1, %11
  %13 = add i64 0, %12
  %14 = load %Range, %Range* @EmptyRange, align 4
  %15 = insertvalue %Range %14, i64 %13, 0
  %16 = insertvalue %Range %15, i64 -1, 1
  %17 = insertvalue %Range %16, i64 0, 2
  %18 = extractvalue %Range %17, 0
  %19 = extractvalue %Range %17, 1
  %20 = extractvalue %Range %17, 2
  br label %preheader__1

preheader__1:                                     ; preds = %condContinue__1
  %21 = icmp sgt i64 %19, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar1__i__ = phi i64 [ %18, %preheader__1 ], [ %40, %exiting__1 ]
  %22 = icmp sle i64 %__qsVar1__i__, %20
  %23 = icmp sge i64 %__qsVar1__i__, %20
  %24 = select i1 %21, i1 %22, i1 %23
  br i1 %24, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %25 = load %Array*, %Array** %0, align 8
  %26 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %25, i64 %__qsVar1__i__)
  %27 = bitcast i8* %26 to %Qubit**
  %qubit = load %Qubit*, %Qubit** %27, align 8
  call void @__quantum__qis__h__body(%Qubit* %qubit)
  %28 = sub i64 %__qsVar1__i__, 1
  %29 = sub i64 %28, 0
  %30 = sdiv i64 %29, 1
  %31 = mul i64 1, %30
  %32 = add i64 0, %31
  %33 = load %Range, %Range* @EmptyRange, align 4
  %34 = insertvalue %Range %33, i64 %32, 0
  %35 = insertvalue %Range %34, i64 -1, 1
  %36 = insertvalue %Range %35, i64 0, 2
  %37 = extractvalue %Range %36, 0
  %38 = extractvalue %Range %36, 1
  %39 = extractvalue %Range %36, 2
  br label %preheader__2

exiting__1:                                       ; preds = %exit__2
  %40 = add i64 %__qsVar1__i__, %19
  br label %header__1

exit__1:                                          ; preds = %header__1
  %41 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %41, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %4, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  ret void

preheader__2:                                     ; preds = %body__1
  %42 = icmp sgt i64 %38, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__2
  %__qsVar2__j__ = phi i64 [ %37, %preheader__2 ], [ %64, %exiting__2 ]
  %43 = icmp sle i64 %__qsVar2__j__, %39
  %44 = icmp sge i64 %__qsVar2__j__, %39
  %45 = select i1 %42, i1 %43, i1 %44
  br i1 %45, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %46 = sub i64 %__qsVar1__i__, %__qsVar2__j__
  %47 = icmp slt i64 %46, %a
  br i1 %47, label %then0__1, label %continue__1

then0__1:                                         ; preds = %body__2
  %48 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %49 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %48, i64 0)
  %50 = bitcast i8* %49 to %Qubit**
  %51 = load %Array*, %Array** %0, align 8
  %52 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %51, i64 %__qsVar1__i__)
  %53 = bitcast i8* %52 to %Qubit**
  %54 = load %Qubit*, %Qubit** %53, align 8
  store %Qubit* %54, %Qubit** %50, align 8
  %55 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %56 = bitcast %Tuple* %55 to { i64, i64, %Qubit* }*
  %57 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %56, i32 0, i32 0
  %58 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %56, i32 0, i32 1
  %59 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %56, i32 0, i32 2
  %60 = sub i64 %__qsVar1__i__, %__qsVar2__j__
  %61 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %51, i64 %__qsVar2__j__)
  %62 = bitcast i8* %61 to %Qubit**
  %63 = load %Qubit*, %Qubit** %62, align 8
  store i64 1, i64* %57, align 4
  store i64 %60, i64* %58, align 4
  store %Qubit* %63, %Qubit** %59, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctladj(%Array* %48, { i64, i64, %Qubit* }* %56)
  call void @__quantum__rt__array_update_reference_count(%Array* %48, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %55, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %body__2
  br label %exiting__2

exiting__2:                                       ; preds = %continue__1
  %64 = add i64 %__qsVar2__j__, %38
  br label %header__2

exit__2:                                          ; preds = %header__2
  br label %exiting__1
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctl(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  %7 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  store i64 %7, i64* %5, align 4
  store { %Array* }* %qs, { %Array* }** %6, align 8
  call void @Microsoft__Quantum__Canon__ApproximateQFT__ctl(%Array* %__controlQubits__, { i64, { %Array* }* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApproximateQFT__ctl(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %a = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %qs = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %6 = icmp sgt i64 %nQubits, 0
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @18, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %6, %String* %7)
  %8 = icmp sgt i64 %a, 0
  br i1 %8, label %condTrue__1, label %condContinue__1

condTrue__1:                                      ; preds = %entry
  %9 = icmp sle i64 %a, %nQubits
  br label %condContinue__1

condContinue__1:                                  ; preds = %condTrue__1, %entry
  %10 = phi i1 [ %9, %condTrue__1 ], [ %8, %entry ]
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @19, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %10, %String* %11)
  %12 = sub i64 %nQubits, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %condContinue__1
  %i = phi i64 [ 0, %condContinue__1 ], [ %15, %exiting__1 ]
  %13 = icmp sle i64 %i, %12
  br i1 %13, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %14 = sub i64 %i, 1
  br label %header__2

exiting__1:                                       ; preds = %exit__2
  %15 = add i64 %i, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %16 = load %Array*, %Array** %3, align 8
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__ctl(%Array* %__controlQubits__, %Array* %16)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %16, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  ret void

header__2:                                        ; preds = %exiting__2, %body__1
  %j = phi i64 [ 0, %body__1 ], [ %37, %exiting__2 ]
  %17 = icmp sle i64 %j, %14
  br i1 %17, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %18 = sub i64 %i, %j
  %19 = icmp slt i64 %18, %a
  br i1 %19, label %then0__1, label %continue__1

then0__1:                                         ; preds = %body__2
  %20 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %21 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %20, i64 0)
  %22 = bitcast i8* %21 to %Qubit**
  %23 = load %Array*, %Array** %3, align 8
  %24 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %23, i64 %i)
  %25 = bitcast i8* %24 to %Qubit**
  %26 = load %Qubit*, %Qubit** %25, align 8
  store %Qubit* %26, %Qubit** %22, align 8
  %27 = call %Array* @__quantum__rt__array_concatenate(%Array* %__controlQubits__, %Array* %20)
  %28 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %29 = bitcast %Tuple* %28 to { i64, i64, %Qubit* }*
  %30 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %29, i32 0, i32 0
  %31 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %29, i32 0, i32 1
  %32 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %29, i32 0, i32 2
  %33 = sub i64 %i, %j
  %34 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %23, i64 %j)
  %35 = bitcast i8* %34 to %Qubit**
  %36 = load %Qubit*, %Qubit** %35, align 8
  store i64 1, i64* %30, align 4
  store i64 %33, i64* %31, align 4
  store %Qubit* %36, %Qubit** %32, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctl(%Array* %27, { i64, i64, %Qubit* }* %29)
  call void @__quantum__rt__array_update_reference_count(%Array* %20, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %27, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %28, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %body__2
  br label %exiting__2

exiting__2:                                       ; preds = %continue__1
  %37 = add i64 %j, 1
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %38 = load %Array*, %Array** %3, align 8
  %39 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %38, i64 %i)
  %40 = bitcast i8* %39 to %Qubit**
  %qubit = load %Qubit*, %Qubit** %40, align 8
  call void @__quantum__qis__h__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  br label %exiting__1
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctladj(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  %7 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  store i64 %7, i64* %5, align 4
  store { %Array* }* %qs, { %Array* }** %6, align 8
  call void @Microsoft__Quantum__Canon__ApproximateQFT__ctladj(%Array* %__controlQubits__, { i64, { %Array* }* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApproximateQFT__ctladj(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %a = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %qs = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %6 = icmp sgt i64 %__qsVar0__nQubits__, 0
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @18, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %6, %String* %7)
  %8 = icmp sgt i64 %a, 0
  br i1 %8, label %condTrue__1, label %condContinue__1

condTrue__1:                                      ; preds = %entry
  %9 = icmp sle i64 %a, %__qsVar0__nQubits__
  br label %condContinue__1

condContinue__1:                                  ; preds = %condTrue__1, %entry
  %10 = phi i1 [ %9, %condTrue__1 ], [ %8, %entry ]
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([48 x i8], [48 x i8]* @19, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__Fact__body(i1 %10, %String* %11)
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__ctladj(%Array* %__controlQubits__, %Array* %4)
  %12 = sub i64 %__qsVar0__nQubits__, 1
  %13 = sub i64 %12, 0
  %14 = sdiv i64 %13, 1
  %15 = mul i64 1, %14
  %16 = add i64 0, %15
  %17 = load %Range, %Range* @EmptyRange, align 4
  %18 = insertvalue %Range %17, i64 %16, 0
  %19 = insertvalue %Range %18, i64 -1, 1
  %20 = insertvalue %Range %19, i64 0, 2
  %21 = extractvalue %Range %20, 0
  %22 = extractvalue %Range %20, 1
  %23 = extractvalue %Range %20, 2
  br label %preheader__1

preheader__1:                                     ; preds = %condContinue__1
  %24 = icmp sgt i64 %22, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar1__i__ = phi i64 [ %21, %preheader__1 ], [ %43, %exiting__1 ]
  %25 = icmp sle i64 %__qsVar1__i__, %23
  %26 = icmp sge i64 %__qsVar1__i__, %23
  %27 = select i1 %24, i1 %25, i1 %26
  br i1 %27, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %28 = load %Array*, %Array** %3, align 8
  %29 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %28, i64 %__qsVar1__i__)
  %30 = bitcast i8* %29 to %Qubit**
  %qubit = load %Qubit*, %Qubit** %30, align 8
  call void @__quantum__qis__h__ctl(%Array* %__controlQubits__, %Qubit* %qubit)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  %31 = sub i64 %__qsVar1__i__, 1
  %32 = sub i64 %31, 0
  %33 = sdiv i64 %32, 1
  %34 = mul i64 1, %33
  %35 = add i64 0, %34
  %36 = load %Range, %Range* @EmptyRange, align 4
  %37 = insertvalue %Range %36, i64 %35, 0
  %38 = insertvalue %Range %37, i64 -1, 1
  %39 = insertvalue %Range %38, i64 0, 2
  %40 = extractvalue %Range %39, 0
  %41 = extractvalue %Range %39, 1
  %42 = extractvalue %Range %39, 2
  br label %preheader__2

exiting__1:                                       ; preds = %exit__2
  %43 = add i64 %__qsVar1__i__, %22
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  %44 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %44, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  ret void

preheader__2:                                     ; preds = %body__1
  %45 = icmp sgt i64 %41, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__2
  %__qsVar2__j__ = phi i64 [ %40, %preheader__2 ], [ %68, %exiting__2 ]
  %46 = icmp sle i64 %__qsVar2__j__, %42
  %47 = icmp sge i64 %__qsVar2__j__, %42
  %48 = select i1 %45, i1 %46, i1 %47
  br i1 %48, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %49 = sub i64 %__qsVar1__i__, %__qsVar2__j__
  %50 = icmp slt i64 %49, %a
  br i1 %50, label %then0__1, label %continue__1

then0__1:                                         ; preds = %body__2
  %51 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 1)
  %52 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %51, i64 0)
  %53 = bitcast i8* %52 to %Qubit**
  %54 = load %Array*, %Array** %3, align 8
  %55 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %54, i64 %__qsVar1__i__)
  %56 = bitcast i8* %55 to %Qubit**
  %57 = load %Qubit*, %Qubit** %56, align 8
  store %Qubit* %57, %Qubit** %53, align 8
  %58 = call %Array* @__quantum__rt__array_concatenate(%Array* %__controlQubits__, %Array* %51)
  %59 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %60 = bitcast %Tuple* %59 to { i64, i64, %Qubit* }*
  %61 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %60, i32 0, i32 0
  %62 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %60, i32 0, i32 1
  %63 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %60, i32 0, i32 2
  %64 = sub i64 %__qsVar1__i__, %__qsVar2__j__
  %65 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %54, i64 %__qsVar2__j__)
  %66 = bitcast i8* %65 to %Qubit**
  %67 = load %Qubit*, %Qubit** %66, align 8
  store i64 1, i64* %61, align 4
  store i64 %64, i64* %62, align 4
  store %Qubit* %67, %Qubit** %63, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctladj(%Array* %58, { i64, i64, %Qubit* }* %60)
  call void @__quantum__rt__array_update_reference_count(%Array* %51, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %58, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %59, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %body__2
  br label %exiting__2

exiting__2:                                       ; preds = %continue__1
  %68 = add i64 %__qsVar2__j__, %41
  br label %header__2

exit__2:                                          ; preds = %header__2
  br label %exiting__1
}

define internal void @Microsoft__Quantum__Canon__ApplyCNOTChain__body(%Array* %qubits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %0 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %1 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %qubits)
  %2 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %qubits)
  %3 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %1, %Array* %2)
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__body(%Callable* %0, %Array* %3)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %0, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %0, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %2, i32 -1)
  %4 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %5 = sub i64 %4, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %6 = phi i64 [ 0, %entry ], [ %12, %exiting__1 ]
  %7 = icmp sle i64 %6, %5
  br i1 %7, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %8 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 %6)
  %9 = bitcast i8* %8 to { %Qubit*, %Qubit* }**
  %10 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %9, align 8
  %11 = bitcast { %Qubit*, %Qubit* }* %10 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %11, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %12 = add i64 %6, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__body(%Callable* %singleElementOperation, %Array* %register) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %1 = sub i64 %0, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %2 = phi i64 [ 0, %entry ], [ %8, %exiting__1 ]
  %3 = icmp sle i64 %2, %1
  br i1 %3, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %4 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %2)
  %5 = bitcast i8* %4 to { %Qubit*, %Qubit* }**
  %6 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %5, align 8
  %7 = bitcast { %Qubit*, %Qubit* }* %6 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %7, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %8 = add i64 %2, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %9 = call %Range @Microsoft__Quantum__Arrays___25a41074dac049fdba7e12ae3b973296_IndexRange__body(%Array* %register)
  %10 = extractvalue %Range %9, 0
  %11 = extractvalue %Range %9, 1
  %12 = extractvalue %Range %9, 2
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  %13 = icmp sgt i64 %11, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %idxQubit = phi i64 [ %10, %preheader__1 ], [ %21, %exiting__2 ]
  %14 = icmp sle i64 %idxQubit, %12
  %15 = icmp sge i64 %idxQubit, %12
  %16 = select i1 %13, i1 %14, i1 %15
  br i1 %16, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %idxQubit)
  %18 = bitcast i8* %17 to { %Qubit*, %Qubit* }**
  %19 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %18, align 8
  %20 = bitcast { %Qubit*, %Qubit* }* %19 to %Tuple*
  call void @__quantum__rt__callable_invoke(%Callable* %singleElementOperation, %Tuple* %20, %Tuple* null)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %21 = add i64 %idxQubit, %11
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  %22 = sub i64 %0, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %23 = phi i64 [ 0, %exit__2 ], [ %29, %exiting__3 ]
  %24 = icmp sle i64 %23, %22
  br i1 %24, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %25 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %23)
  %26 = bitcast i8* %25 to { %Qubit*, %Qubit* }**
  %27 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %26, align 8
  %28 = bitcast { %Qubit*, %Qubit* }* %27 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %28, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %29 = add i64 %23, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Qubit*, %Qubit* }*
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %3 = load %Qubit*, %Qubit** %1, align 8
  %4 = load %Qubit*, %Qubit** %2, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %3, %Qubit* %4)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Qubit*, %Qubit* }*
  %1 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %0, i32 0, i32 1
  %3 = load %Qubit*, %Qubit** %1, align 8
  %4 = load %Qubit*, %Qubit** %2, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %3, %Qubit* %4)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Qubit*, %Qubit* }* }*
  %1 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %2, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %3, { %Qubit*, %Qubit* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Intrinsic__CNOT__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Qubit*, %Qubit* }* }*
  %1 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %2, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %3, { %Qubit*, %Qubit* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyCNOTChain__adj(%Array* %qubits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %0 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %1 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %qubits)
  %2 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %qubits)
  %3 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %1, %Array* %2)
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__adj(%Callable* %0, %Array* %3)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %0, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %0, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %2, i32 -1)
  %4 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %5 = sub i64 %4, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %6 = phi i64 [ 0, %entry ], [ %12, %exiting__1 ]
  %7 = icmp sle i64 %6, %5
  br i1 %7, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %8 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 %6)
  %9 = bitcast i8* %8 to { %Qubit*, %Qubit* }**
  %10 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %9, align 8
  %11 = bitcast { %Qubit*, %Qubit* }* %10 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %11, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %12 = add i64 %6, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__adj(%Callable* %singleElementOperation, %Array* %register) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 1)
  %0 = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %1 = sub i64 %0, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %2 = phi i64 [ 0, %entry ], [ %8, %exiting__1 ]
  %3 = icmp sle i64 %2, %1
  br i1 %3, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %4 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %2)
  %5 = bitcast i8* %4 to { %Qubit*, %Qubit* }**
  %6 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %5, align 8
  %7 = bitcast { %Qubit*, %Qubit* }* %6 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %7, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %8 = add i64 %2, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %9 = call %Range @Microsoft__Quantum__Arrays___25a41074dac049fdba7e12ae3b973296_IndexRange__body(%Array* %register)
  %10 = extractvalue %Range %9, 0
  %11 = extractvalue %Range %9, 1
  %12 = extractvalue %Range %9, 2
  %13 = sub i64 %12, %10
  %14 = sdiv i64 %13, %11
  %15 = mul i64 %11, %14
  %16 = add i64 %10, %15
  %17 = sub i64 0, %11
  %18 = load %Range, %Range* @EmptyRange, align 4
  %19 = insertvalue %Range %18, i64 %16, 0
  %20 = insertvalue %Range %19, i64 %17, 1
  %21 = insertvalue %Range %20, i64 %10, 2
  %22 = extractvalue %Range %21, 0
  %23 = extractvalue %Range %21, 1
  %24 = extractvalue %Range %21, 2
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  %25 = icmp sgt i64 %23, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %__qsVar0__idxQubit__ = phi i64 [ %22, %preheader__1 ], [ %34, %exiting__2 ]
  %26 = icmp sle i64 %__qsVar0__idxQubit__, %24
  %27 = icmp sge i64 %__qsVar0__idxQubit__, %24
  %28 = select i1 %25, i1 %26, i1 %27
  br i1 %28, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %29 = call %Callable* @__quantum__rt__callable_copy(%Callable* %singleElementOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %29, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %29)
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %__qsVar0__idxQubit__)
  %31 = bitcast i8* %30 to { %Qubit*, %Qubit* }**
  %32 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %31, align 8
  %33 = bitcast { %Qubit*, %Qubit* }* %32 to %Tuple*
  call void @__quantum__rt__callable_invoke(%Callable* %29, %Tuple* %33, %Tuple* null)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %29, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %29, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %34 = add i64 %__qsVar0__idxQubit__, %23
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  %35 = sub i64 %0, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %36 = phi i64 [ 0, %exit__2 ], [ %42, %exiting__3 ]
  %37 = icmp sle i64 %36, %35
  br i1 %37, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %38 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %36)
  %39 = bitcast i8* %38 to { %Qubit*, %Qubit* }**
  %40 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %39, align 8
  %41 = bitcast { %Qubit*, %Qubit* }* %40 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %41, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %42 = add i64 %36, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyCNOTChain__ctl(%Array* %__controlQubits__, %Array* %qubits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %0 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %1 = bitcast %Tuple* %0 to { %Callable*, %Array* }*
  %2 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %1, i32 0, i32 0
  %3 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %1, i32 0, i32 1
  %4 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %5 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %qubits)
  %6 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %qubits)
  %7 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %5, %Array* %6)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  store %Callable* %4, %Callable** %2, align 8
  store %Array* %7, %Array** %3, align 8
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctl(%Array* %__controlQubits__, { %Callable*, %Array* }* %1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %4, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %4, i32 -1)
  %8 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %9 = sub i64 %8, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %10 = phi i64 [ 0, %entry ], [ %16, %exiting__1 ]
  %11 = icmp sle i64 %10, %9
  br i1 %11, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %12 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 %10)
  %13 = bitcast i8* %12 to { %Qubit*, %Qubit* }**
  %14 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %13, align 8
  %15 = bitcast { %Qubit*, %Qubit* }* %14 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %15, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %16 = add i64 %10, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %0, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctl(%Array* %__controlQubits__, { %Callable*, %Array* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %0, i32 0, i32 0
  %singleElementOperation = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %0, i32 0, i32 1
  %register = load %Array*, %Array** %2, align 8
  %3 = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %4 = sub i64 %3, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %5 = phi i64 [ 0, %entry ], [ %11, %exiting__1 ]
  %6 = icmp sle i64 %5, %4
  br i1 %6, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %7 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %5)
  %8 = bitcast i8* %7 to { %Qubit*, %Qubit* }**
  %9 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %8, align 8
  %10 = bitcast { %Qubit*, %Qubit* }* %9 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %11 = add i64 %5, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %12 = call %Range @Microsoft__Quantum__Arrays___25a41074dac049fdba7e12ae3b973296_IndexRange__body(%Array* %register)
  %13 = extractvalue %Range %12, 0
  %14 = extractvalue %Range %12, 1
  %15 = extractvalue %Range %12, 2
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  %16 = icmp sgt i64 %14, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %idxQubit = phi i64 [ %13, %preheader__1 ], [ %29, %exiting__2 ]
  %17 = icmp sle i64 %idxQubit, %15
  %18 = icmp sge i64 %idxQubit, %15
  %19 = select i1 %16, i1 %17, i1 %18
  br i1 %19, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %20 = call %Callable* @__quantum__rt__callable_copy(%Callable* %singleElementOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %20, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %20)
  %21 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %22 = bitcast %Tuple* %21 to { %Array*, { %Qubit*, %Qubit* }* }*
  %23 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %22, i32 0, i32 0
  %24 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %22, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  %25 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %idxQubit)
  %26 = bitcast i8* %25 to { %Qubit*, %Qubit* }**
  %27 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %26, align 8
  %28 = bitcast { %Qubit*, %Qubit* }* %27 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %28, i32 1)
  store %Array* %__controlQubits__, %Array** %23, align 8
  store { %Qubit*, %Qubit* }* %27, { %Qubit*, %Qubit* }** %24, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %20, %Tuple* %21, %Tuple* null)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %20, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %20, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %28, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %21, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %29 = add i64 %idxQubit, %14
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  %30 = sub i64 %3, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %31 = phi i64 [ 0, %exit__2 ], [ %37, %exiting__3 ]
  %32 = icmp sle i64 %31, %30
  br i1 %32, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %33 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %31)
  %34 = bitcast i8* %33 to { %Qubit*, %Qubit* }**
  %35 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %34, align 8
  %36 = bitcast { %Qubit*, %Qubit* }* %35 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %36, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %37 = add i64 %31, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyCNOTChain__ctladj(%Array* %__controlQubits__, %Array* %qubits) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 1)
  %0 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %1 = bitcast %Tuple* %0 to { %Callable*, %Array* }*
  %2 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %1, i32 0, i32 0
  %3 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %1, i32 0, i32 1
  %4 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %5 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %qubits)
  %6 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %qubits)
  %7 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %5, %Array* %6)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  store %Callable* %4, %Callable** %2, align 8
  store %Array* %7, %Array** %3, align 8
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Array* }* %1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %qubits, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %4, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %4, i32 -1)
  %8 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %9 = sub i64 %8, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %10 = phi i64 [ 0, %entry ], [ %16, %exiting__1 ]
  %11 = icmp sle i64 %10, %9
  br i1 %11, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %12 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 %10)
  %13 = bitcast i8* %12 to { %Qubit*, %Qubit* }**
  %14 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %13, align 8
  %15 = bitcast { %Qubit*, %Qubit* }* %14 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %15, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %16 = add i64 %10, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %0, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Array* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %0, i32 0, i32 0
  %singleElementOperation = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %0, i32 0, i32 1
  %register = load %Array*, %Array** %2, align 8
  %3 = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %4 = sub i64 %3, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %5 = phi i64 [ 0, %entry ], [ %11, %exiting__1 ]
  %6 = icmp sle i64 %5, %4
  br i1 %6, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %7 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %5)
  %8 = bitcast i8* %7 to { %Qubit*, %Qubit* }**
  %9 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %8, align 8
  %10 = bitcast { %Qubit*, %Qubit* }* %9 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %11 = add i64 %5, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %12 = call %Range @Microsoft__Quantum__Arrays___25a41074dac049fdba7e12ae3b973296_IndexRange__body(%Array* %register)
  %13 = extractvalue %Range %12, 0
  %14 = extractvalue %Range %12, 1
  %15 = extractvalue %Range %12, 2
  %16 = sub i64 %15, %13
  %17 = sdiv i64 %16, %14
  %18 = mul i64 %14, %17
  %19 = add i64 %13, %18
  %20 = sub i64 0, %14
  %21 = load %Range, %Range* @EmptyRange, align 4
  %22 = insertvalue %Range %21, i64 %19, 0
  %23 = insertvalue %Range %22, i64 %20, 1
  %24 = insertvalue %Range %23, i64 %13, 2
  %25 = extractvalue %Range %24, 0
  %26 = extractvalue %Range %24, 1
  %27 = extractvalue %Range %24, 2
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  %28 = icmp sgt i64 %26, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %__qsVar0__idxQubit__ = phi i64 [ %25, %preheader__1 ], [ %41, %exiting__2 ]
  %29 = icmp sle i64 %__qsVar0__idxQubit__, %27
  %30 = icmp sge i64 %__qsVar0__idxQubit__, %27
  %31 = select i1 %28, i1 %29, i1 %30
  br i1 %31, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %32 = call %Callable* @__quantum__rt__callable_copy(%Callable* %singleElementOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %32, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %32)
  call void @__quantum__rt__callable_make_controlled(%Callable* %32)
  %33 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %34 = bitcast %Tuple* %33 to { %Array*, { %Qubit*, %Qubit* }* }*
  %35 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %34, i32 0, i32 0
  %36 = getelementptr inbounds { %Array*, { %Qubit*, %Qubit* }* }, { %Array*, { %Qubit*, %Qubit* }* }* %34, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  %37 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %__qsVar0__idxQubit__)
  %38 = bitcast i8* %37 to { %Qubit*, %Qubit* }**
  %39 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %38, align 8
  %40 = bitcast { %Qubit*, %Qubit* }* %39 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %40, i32 1)
  store %Array* %__controlQubits__, %Array** %35, align 8
  store { %Qubit*, %Qubit* }* %39, { %Qubit*, %Qubit* }** %36, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %32, %Tuple* %33, %Tuple* null)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %32, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %32, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %40, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %33, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %41 = add i64 %__qsVar0__idxQubit__, %26
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %singleElementOperation, i32 -1)
  %42 = sub i64 %3, 1
  br label %header__3

header__3:                                        ; preds = %exiting__3, %exit__2
  %43 = phi i64 [ 0, %exit__2 ], [ %49, %exiting__3 ]
  %44 = icmp sle i64 %43, %42
  br i1 %44, label %body__3, label %exit__3

body__3:                                          ; preds = %header__3
  %45 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %43)
  %46 = bitcast i8* %45 to { %Qubit*, %Qubit* }**
  %47 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %46, align 8
  %48 = bitcast { %Qubit*, %Qubit* }* %47 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %48, i32 -1)
  br label %exiting__3

exiting__3:                                       ; preds = %body__3
  %49 = add i64 %43, 1
  br label %header__3

exit__3:                                          ; preds = %header__3
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__body({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__body(%Callable* %3, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__body(%Callable* %op, { %Array* }* %register) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %register, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %register to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__body(%Callable* %3, %Callable* %op, { %Array* }* %register)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array* }*
  call void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____body({ %Array* }* %0)
  ret void
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array* }*
  call void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____adj({ %Array* }* %0)
  ret void
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctl(%Array* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____ctladj(%Array* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__adj({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__adj(%Callable* %3, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__adj(%Callable* %op, { %Array* }* %register) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %register, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %register to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__adj(%Callable* %3, %Callable* %op, { %Array* }* %register)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctl(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Callable*, { %Array* }* }*
  %5 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %4, i32 0, i32 1
  %7 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  store %Callable* %7, %Callable** %5, align 8
  store { %Array* }* %qs, { %Array* }** %6, align 8
  call void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__ctl(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__ctl(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %op = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %2 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %register = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %register, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %register to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %7 = bitcast %Tuple* %6 to { %Callable*, %Callable*, { %Array* }* }*
  %8 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 0
  %9 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 1
  %10 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 2
  %11 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %op, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store %Callable* %11, %Callable** %8, align 8
  store %Callable* %op, %Callable** %9, align 8
  store { %Array* }* %register, { %Array* }** %10, align 8
  call void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__ctl(%Array* %__controlQubits__, { %Callable*, %Callable*, { %Array* }* }* %7)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctladj(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %4 = bitcast %Tuple* %3 to { %Callable*, { %Array* }* }*
  %5 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %4, i32 0, i32 1
  %7 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Canon____QsRef1__ApplyQuantumFourierTransformBE____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  store %Callable* %7, %Callable** %5, align 8
  store { %Array* }* %qs, { %Array* }** %6, align 8
  call void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__ctladj(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %4)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyReversedOpBECA__ctladj(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %op = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %2 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %register = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %register, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %register to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %7 = bitcast %Tuple* %6 to { %Callable*, %Callable*, { %Array* }* }*
  %8 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 0
  %9 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 1
  %10 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %7, i32 0, i32 2
  %11 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %op, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store %Callable* %11, %Callable** %8, align 8
  store %Callable* %op, %Callable** %9, align 8
  store { %Array* }* %register, { %Array* }** %10, align 8
  call void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Callable*, { %Array* }* }* %7)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__SwapReverseRegister__body(%Array* %register) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %totalQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %halfTotal = sdiv i64 %totalQubits, 2
  %0 = sub i64 %halfTotal, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %i = phi i64 [ 0, %entry ], [ %10, %exiting__1 ]
  %1 = icmp sle i64 %i, %0
  br i1 %1, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %2 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %i)
  %3 = bitcast i8* %2 to %Qubit**
  %4 = load %Qubit*, %Qubit** %3, align 8
  %5 = sub i64 %totalQubits, %i
  %6 = sub i64 %5, 1
  %7 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %6)
  %8 = bitcast i8* %7 to %Qubit**
  %9 = load %Qubit*, %Qubit** %8, align 8
  call void @Microsoft__Quantum__Intrinsic__SWAP__body(%Qubit* %4, %Qubit* %9)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %10 = add i64 %i, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__SwapReverseRegister__adj(%Array* %register) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__body(%Array* %register)
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__SwapReverseRegister__ctl(%Array* %__controlQubits__, %Array* %register) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  %totalQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %register)
  %halfTotal = sdiv i64 %totalQubits, 2
  %0 = sub i64 %halfTotal, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %i = phi i64 [ 0, %entry ], [ %14, %exiting__1 ]
  %1 = icmp sle i64 %i, %0
  br i1 %1, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %2 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %3 = bitcast %Tuple* %2 to { %Qubit*, %Qubit* }*
  %4 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %3, i32 0, i32 0
  %5 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %3, i32 0, i32 1
  %6 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %i)
  %7 = bitcast i8* %6 to %Qubit**
  %8 = load %Qubit*, %Qubit** %7, align 8
  %9 = sub i64 %totalQubits, %i
  %10 = sub i64 %9, 1
  %11 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %register, i64 %10)
  %12 = bitcast i8* %11 to %Qubit**
  %13 = load %Qubit*, %Qubit** %12, align 8
  store %Qubit* %8, %Qubit** %4, align 8
  store %Qubit* %13, %Qubit** %5, align 8
  call void @Microsoft__Quantum__Intrinsic__SWAP__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %3)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %14 = add i64 %i, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__SwapReverseRegister__ctladj(%Array* %__controlQubits__, %Array* %register) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 1)
  call void @Microsoft__Quantum__Canon__SwapReverseRegister__ctl(%Array* %__controlQubits__, %Array* %register)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %register, i32 -1)
  ret void
}

define internal { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndianAsLittleEndian__body({ %Array* }* %input) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Array* @Microsoft__Quantum__Arrays___da24003d78a6494a9b43249d80017883_Reversed__body(%Array* %1)
  %4 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %3)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  ret { %Array* }* %4
}

define internal void @Microsoft__Quantum__Canon__QFT__ctl(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndianAsLittleEndian__body({ %Array* }* %qs)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctl(%Array* %__controlQubits__, { %Array* }* %3)
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %3, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  %6 = bitcast { %Array* }* %3 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFT__ctladj(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndianAsLittleEndian__body({ %Array* }* %qs)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctladj(%Array* %__controlQubits__, { %Array* }* %3)
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %3, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %5, i32 -1)
  %6 = bitcast { %Array* }* %3 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFTLE__body({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__body({ %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFTLE__adj({ %Array* }* %qs) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__adj({ %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFTLE__ctl(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctl(%Array* %__controlQubits__, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon__QFTLE__ctladj(%Array* %__controlQubits__, { %Array* }* %qs) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %qs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %qs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__ApplyQuantumFourierTransform__ctladj(%Array* %__controlQubits__, { %Array* }* %qs)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__body(%Callable* %fn, %Callable* %op, { %Array* }* %input) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  call void @__quantum__rt__callable_invoke(%Callable* %fn, %Tuple* %2, %Tuple* %3)
  %4 = bitcast %Tuple* %3 to { { %Array* }* }*
  %5 = getelementptr inbounds { { %Array* }* }, { { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = bitcast { %Array* }* %6 to %Tuple*
  call void @__quantum__rt__callable_invoke(%Callable* %op, %Tuple* %7, %Tuple* null)
  %8 = getelementptr inbounds { %Array* }, { %Array* }* %6, i32 0, i32 0
  %9 = load %Array*, %Array** %8, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %9, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__adj(%Callable* %fn, %Callable* %op, { %Array* }* %input) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %3)
  %4 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  call void @__quantum__rt__callable_invoke(%Callable* %fn, %Tuple* %2, %Tuple* %4)
  %5 = bitcast %Tuple* %4 to { { %Array* }* }*
  %6 = getelementptr inbounds { { %Array* }* }, { { %Array* }* }* %5, i32 0, i32 0
  %7 = load { %Array* }*, { %Array* }** %6, align 8
  %8 = bitcast { %Array* }* %7 to %Tuple*
  call void @__quantum__rt__callable_invoke(%Callable* %3, %Tuple* %8, %Tuple* null)
  %9 = getelementptr inbounds { %Array* }, { %Array* }* %7, i32 0, i32 0
  %10 = load %Array*, %Array** %9, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %3, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %10, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  ret void
}

declare %Callable* @__quantum__rt__callable_copy(%Callable*, i1)

declare void @__quantum__rt__callable_make_adjoint(%Callable*)

define internal void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__ctl(%Array* %__controlQubits__, { %Callable*, %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %fn = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %op = load %Callable*, %Callable** %2, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %3 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 2
  %input = load { %Array* }*, { %Array* }** %3, align 8
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 1)
  %6 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 1)
  %7 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %7)
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %9 = bitcast %Tuple* %8 to { %Array*, { %Array* }* }*
  %10 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %9, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  call void @__quantum__rt__callable_invoke(%Callable* %fn, %Tuple* %6, %Tuple* %12)
  %13 = bitcast %Tuple* %12 to { { %Array* }* }*
  %14 = getelementptr inbounds { { %Array* }* }, { { %Array* }* }* %13, i32 0, i32 0
  %15 = load { %Array* }*, { %Array* }** %14, align 8
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  store %Array* %__controlQubits__, %Array** %10, align 8
  store { %Array* }* %15, { %Array* }** %11, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %7, %Tuple* %8, %Tuple* null)
  %16 = getelementptr inbounds { %Array* }, { %Array* }* %15, i32 0, i32 0
  %17 = load %Array*, %Array** %16, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %17, i32 -1)
  %18 = bitcast { %Array* }* %15 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %18, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

declare void @__quantum__rt__callable_make_controlled(%Callable*)

define internal void @Microsoft__Quantum__Canon___0a765c3d835f4d919918e800ea143796_ApplyWithInputTransformationCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %fn = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %op = load %Callable*, %Callable** %2, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %3 = getelementptr inbounds { %Callable*, %Callable*, { %Array* }* }, { %Callable*, %Callable*, { %Array* }* }* %0, i32 0, i32 2
  %input = load { %Array* }*, { %Array* }** %3, align 8
  %4 = getelementptr inbounds { %Array* }, { %Array* }* %input, i32 0, i32 0
  %5 = load %Array*, %Array** %4, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 1)
  %6 = bitcast { %Array* }* %input to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 1)
  %7 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %7)
  call void @__quantum__rt__callable_make_controlled(%Callable* %7)
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %9 = bitcast %Tuple* %8 to { %Array*, { %Array* }* }*
  %10 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %9, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  call void @__quantum__rt__callable_invoke(%Callable* %fn, %Tuple* %6, %Tuple* %12)
  %13 = bitcast %Tuple* %12 to { { %Array* }* }*
  %14 = getelementptr inbounds { { %Array* }* }, { { %Array* }* }* %13, i32 0, i32 0
  %15 = load { %Array* }*, { %Array* }** %14, align 8
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  store %Array* %__controlQubits__, %Array** %10, align 8
  store { %Array* }* %15, { %Array* }** %11, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %7, %Tuple* %8, %Tuple* null)
  %16 = getelementptr inbounds { %Array* }, { %Array* }* %15, i32 0, i32 0
  %17 = load %Array*, %Array** %16, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %fn, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %5, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %6, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %7, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %17, i32 -1)
  %18 = bitcast { %Array* }* %15 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %18, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__body(%Callable* %outerOperation, %Callable* %innerOperation, { { %Array* }*, { %Array* }* }* %target) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 1)
  %0 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 0
  %1 = load { %Array* }*, { %Array* }** %0, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %1, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %1 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 1
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { %Array* }, { %Array* }* %6, i32 0, i32 0
  %8 = load %Array*, %Array** %7, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %8, i32 1)
  %9 = bitcast { %Array* }* %6 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %9, i32 1)
  %10 = bitcast { { %Array* }*, { %Array* }* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 1)
  call void @__quantum__rt__callable_invoke(%Callable* %outerOperation, %Tuple* %10, %Tuple* null)
  call void @__quantum__rt__callable_invoke(%Callable* %innerOperation, %Tuple* %10, %Tuple* null)
  %11 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %11)
  call void @__quantum__rt__callable_invoke(%Callable* %11, %Tuple* %10, %Tuple* null)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %8, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %9, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %11, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__adj(%Callable* %outerOperation, %Callable* %innerOperation, { { %Array* }*, { %Array* }* }* %target) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 1)
  %0 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 0
  %1 = load { %Array* }*, { %Array* }** %0, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %1, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %1 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 1
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { %Array* }, { %Array* }* %6, i32 0, i32 0
  %8 = load %Array*, %Array** %7, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %8, i32 1)
  %9 = bitcast { %Array* }* %6 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %9, i32 1)
  %10 = bitcast { { %Array* }*, { %Array* }* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 1)
  %11 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %11)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %11)
  call void @__quantum__rt__callable_invoke(%Callable* %11, %Tuple* %10, %Tuple* null)
  %12 = call %Callable* @__quantum__rt__callable_copy(%Callable* %innerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %12, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %12)
  call void @__quantum__rt__callable_invoke(%Callable* %12, %Tuple* %10, %Tuple* null)
  %13 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %13, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %13)
  call void @__quantum__rt__callable_invoke(%Callable* %13, %Tuple* %10, %Tuple* null)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %8, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %9, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %10, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %12, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %13, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %13, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctl(%Array* %controlRegister, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controlRegister, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %outerOperation = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %innerOperation = load %Callable*, %Callable** %2, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 1)
  %3 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 2
  %target = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %3, align 8
  %4 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 0
  %5 = load { %Array* }*, { %Array* }** %4, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %5, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %5 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 1
  %10 = load { %Array* }*, { %Array* }** %9, align 8
  %11 = getelementptr inbounds { %Array* }, { %Array* }* %10, i32 0, i32 0
  %12 = load %Array*, %Array** %11, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %12, i32 1)
  %13 = bitcast { %Array* }* %10 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %13, i32 1)
  %14 = bitcast { { %Array* }*, { %Array* }* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %14, i32 1)
  call void @__quantum__rt__callable_invoke(%Callable* %outerOperation, %Tuple* %14, %Tuple* null)
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %innerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %15)
  %16 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %17 = bitcast %Tuple* %16 to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %18 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %17, i32 0, i32 0
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %17, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %controlRegister, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %14, i32 1)
  store %Array* %controlRegister, %Array** %18, align 8
  store { { %Array* }*, { %Array* }* }* %target, { { %Array* }*, { %Array* }* }** %19, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %16, %Tuple* null)
  %20 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %20, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %20)
  call void @__quantum__rt__callable_invoke(%Callable* %20, %Tuple* %14, %Tuple* null)
  call void @__quantum__rt__array_update_alias_count(%Array* %controlRegister, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %12, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %13, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %14, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %controlRegister, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %14, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %16, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %20, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %20, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctladj(%Array* %controlRegister, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controlRegister, i32 1)
  %1 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %outerOperation = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 1)
  %2 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %innerOperation = load %Callable*, %Callable** %2, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 1)
  %3 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 2
  %target = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %3, align 8
  %4 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 0
  %5 = load { %Array* }*, { %Array* }** %4, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %5, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %5 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %target, i32 0, i32 1
  %10 = load { %Array* }*, { %Array* }** %9, align 8
  %11 = getelementptr inbounds { %Array* }, { %Array* }* %10, i32 0, i32 0
  %12 = load %Array*, %Array** %11, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %12, i32 1)
  %13 = bitcast { %Array* }* %10 to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %13, i32 1)
  %14 = bitcast { { %Array* }*, { %Array* }* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %14, i32 1)
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %14, %Tuple* null)
  %16 = call %Callable* @__quantum__rt__callable_copy(%Callable* %innerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %16, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %16)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %16)
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %18, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %controlRegister, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %14, i32 1)
  store %Array* %controlRegister, %Array** %19, align 8
  store { { %Array* }*, { %Array* }* }* %target, { { %Array* }*, { %Array* }* }** %20, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %16, %Tuple* %17, %Tuple* null)
  %21 = call %Callable* @__quantum__rt__callable_copy(%Callable* %outerOperation, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %21, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %21)
  call void @__quantum__rt__callable_invoke(%Callable* %21, %Tuple* %14, %Tuple* null)
  call void @__quantum__rt__array_update_alias_count(%Array* %controlRegister, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %outerOperation, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %innerOperation, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %12, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %13, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %14, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %16, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %16, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %controlRegister, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %14, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %21, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %21, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____body({ %Array* }* %xs, { %Array* }* %ys, %Qubit* %carry) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 0)
  %7 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %8 = bitcast %Tuple* %7 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 0
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 1
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 2
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %9, align 8
  store { %Array* }* %ys, { %Array* }** %10, align 8
  store %Qubit* %carry, %Qubit** %11, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctl(%Array* %6, { { %Array* }*, { %Array* }*, %Qubit* }* %8)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctl(%Array* %controls, { { %Array* }*, { %Array* }*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %carry = load %Qubit*, %Qubit** %9, align 8
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %10, %String* %11)
  %12 = sub i64 %nQubits, 2
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %idx = phi i64 [ 0, %entry ], [ %26, %exiting__1 ]
  %13 = icmp sle i64 %idx, %12
  br i1 %13, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %14 = load %Array*, %Array** %2, align 8
  %15 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %14, i64 %idx)
  %16 = bitcast i8* %15 to %Qubit**
  %17 = load %Qubit*, %Qubit** %16, align 8
  %18 = load %Array*, %Array** %6, align 8
  %19 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %18, i64 %idx)
  %20 = bitcast i8* %19 to %Qubit**
  %21 = load %Qubit*, %Qubit** %20, align 8
  %22 = add i64 %idx, 1
  %23 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %14, i64 %22)
  %24 = bitcast i8* %23 to %Qubit**
  %25 = load %Qubit*, %Qubit** %24, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %17, %Qubit* %21, %Qubit* %25)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %26 = add i64 %idx, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %27 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %28 = bitcast %Tuple* %27 to { %Qubit*, %Qubit*, %Qubit* }*
  %29 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %28, i32 0, i32 0
  %30 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %28, i32 0, i32 1
  %31 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %28, i32 0, i32 2
  %32 = load %Array*, %Array** %2, align 8
  %33 = sub i64 %nQubits, 1
  %34 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %32, i64 %33)
  %35 = bitcast i8* %34 to %Qubit**
  %36 = load %Qubit*, %Qubit** %35, align 8
  %37 = load %Array*, %Array** %6, align 8
  %38 = sub i64 %nQubits, 1
  %39 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %37, i64 %38)
  %40 = bitcast i8* %39 to %Qubit**
  %41 = load %Qubit*, %Qubit** %40, align 8
  store %Qubit* %36, %Qubit** %29, align 8
  store %Qubit* %41, %Qubit** %30, align 8
  store %Qubit* %carry, %Qubit** %31, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__ctl(%Array* %controls, { %Qubit*, %Qubit*, %Qubit* }* %28)
  %42 = sub i64 %nQubits, 1
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %idx__1 = phi i64 [ %42, %preheader__1 ], [ %69, %exiting__2 ]
  %43 = icmp sle i64 %idx__1, 1
  %44 = icmp sge i64 %idx__1, 1
  %45 = select i1 false, i1 %43, i1 %44
  br i1 %45, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %46 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %47 = bitcast %Tuple* %46 to { %Qubit*, %Qubit* }*
  %48 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %47, i32 0, i32 0
  %49 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %47, i32 0, i32 1
  %50 = load %Array*, %Array** %2, align 8
  %51 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %50, i64 %idx__1)
  %52 = bitcast i8* %51 to %Qubit**
  %53 = load %Qubit*, %Qubit** %52, align 8
  %54 = load %Array*, %Array** %6, align 8
  %55 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %54, i64 %idx__1)
  %56 = bitcast i8* %55 to %Qubit**
  %57 = load %Qubit*, %Qubit** %56, align 8
  store %Qubit* %53, %Qubit** %48, align 8
  store %Qubit* %57, %Qubit** %49, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %controls, { %Qubit*, %Qubit* }* %47)
  %58 = sub i64 %idx__1, 1
  %59 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %50, i64 %58)
  %60 = bitcast i8* %59 to %Qubit**
  %61 = load %Qubit*, %Qubit** %60, align 8
  %62 = sub i64 %idx__1, 1
  %63 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %54, i64 %62)
  %64 = bitcast i8* %63 to %Qubit**
  %65 = load %Qubit*, %Qubit** %64, align 8
  %66 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %50, i64 %idx__1)
  %67 = bitcast i8* %66 to %Qubit**
  %68 = load %Qubit*, %Qubit** %67, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %61, %Qubit* %65, %Qubit* %68)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %46, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %69 = add i64 %idx__1, -1
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 -1)
  %70 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %70, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  %71 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %71, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %27, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____adj({ %Array* }* %xs, { %Array* }* %ys, %Qubit* %carry) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 0)
  %7 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %8 = bitcast %Tuple* %7 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 0
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 1
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %8, i32 0, i32 2
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %9, align 8
  store { %Array* }* %ys, { %Array* }** %10, align 8
  store %Qubit* %carry, %Qubit** %11, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctladj(%Array* %6, { { %Array* }*, { %Array* }*, %Qubit* }* %8)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctladj(%Array* %controls, { { %Array* }*, { %Array* }*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %carry = load %Qubit*, %Qubit** %9, align 8
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %10, %String* %11)
  %12 = sub i64 %__qsVar0__nQubits__, 1
  %13 = sub i64 1, %12
  %14 = sdiv i64 %13, -1
  %15 = mul i64 -1, %14
  %16 = add i64 %12, %15
  %17 = load %Range, %Range* @EmptyRange, align 4
  %18 = insertvalue %Range %17, i64 %16, 0
  %19 = insertvalue %Range %18, i64 1, 1
  %20 = insertvalue %Range %19, i64 %12, 2
  %21 = extractvalue %Range %20, 0
  %22 = extractvalue %Range %20, 1
  %23 = extractvalue %Range %20, 2
  br label %preheader__1

preheader__1:                                     ; preds = %entry
  %24 = icmp sgt i64 %22, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar2__idx__ = phi i64 [ %21, %preheader__1 ], [ %51, %exiting__1 ]
  %25 = icmp sle i64 %__qsVar2__idx__, %23
  %26 = icmp sge i64 %__qsVar2__idx__, %23
  %27 = select i1 %24, i1 %25, i1 %26
  br i1 %27, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %28 = load %Array*, %Array** %2, align 8
  %29 = sub i64 %__qsVar2__idx__, 1
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %28, i64 %29)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  %33 = load %Array*, %Array** %6, align 8
  %34 = sub i64 %__qsVar2__idx__, 1
  %35 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %33, i64 %34)
  %36 = bitcast i8* %35 to %Qubit**
  %37 = load %Qubit*, %Qubit** %36, align 8
  %38 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %28, i64 %__qsVar2__idx__)
  %39 = bitcast i8* %38 to %Qubit**
  %40 = load %Qubit*, %Qubit** %39, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %32, %Qubit* %37, %Qubit* %40)
  %41 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %42 = bitcast %Tuple* %41 to { %Qubit*, %Qubit* }*
  %43 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %42, i32 0, i32 0
  %44 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %42, i32 0, i32 1
  %45 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %28, i64 %__qsVar2__idx__)
  %46 = bitcast i8* %45 to %Qubit**
  %47 = load %Qubit*, %Qubit** %46, align 8
  %48 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %33, i64 %__qsVar2__idx__)
  %49 = bitcast i8* %48 to %Qubit**
  %50 = load %Qubit*, %Qubit** %49, align 8
  store %Qubit* %47, %Qubit** %43, align 8
  store %Qubit* %50, %Qubit** %44, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %controls, { %Qubit*, %Qubit* }* %42)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %41, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %51 = add i64 %__qsVar2__idx__, %22
  br label %header__1

exit__1:                                          ; preds = %header__1
  %52 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %53 = bitcast %Tuple* %52 to { %Qubit*, %Qubit*, %Qubit* }*
  %54 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %53, i32 0, i32 0
  %55 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %53, i32 0, i32 1
  %56 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %53, i32 0, i32 2
  %57 = load %Array*, %Array** %2, align 8
  %58 = sub i64 %__qsVar0__nQubits__, 1
  %59 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %57, i64 %58)
  %60 = bitcast i8* %59 to %Qubit**
  %61 = load %Qubit*, %Qubit** %60, align 8
  %62 = load %Array*, %Array** %6, align 8
  %63 = sub i64 %__qsVar0__nQubits__, 1
  %64 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %62, i64 %63)
  %65 = bitcast i8* %64 to %Qubit**
  %66 = load %Qubit*, %Qubit** %65, align 8
  store %Qubit* %61, %Qubit** %54, align 8
  store %Qubit* %66, %Qubit** %55, align 8
  store %Qubit* %carry, %Qubit** %56, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__ctladj(%Array* %controls, { %Qubit*, %Qubit*, %Qubit* }* %53)
  %67 = sub i64 %__qsVar0__nQubits__, 2
  %68 = sub i64 %67, 0
  %69 = sdiv i64 %68, 1
  %70 = mul i64 1, %69
  %71 = add i64 0, %70
  %72 = load %Range, %Range* @EmptyRange, align 4
  %73 = insertvalue %Range %72, i64 %71, 0
  %74 = insertvalue %Range %73, i64 -1, 1
  %75 = insertvalue %Range %74, i64 0, 2
  %76 = extractvalue %Range %75, 0
  %77 = extractvalue %Range %75, 1
  %78 = extractvalue %Range %75, 2
  br label %preheader__2

preheader__2:                                     ; preds = %exit__1
  %79 = icmp sgt i64 %77, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__2
  %__qsVar1__idx__ = phi i64 [ %76, %preheader__2 ], [ %95, %exiting__2 ]
  %80 = icmp sle i64 %__qsVar1__idx__, %78
  %81 = icmp sge i64 %__qsVar1__idx__, %78
  %82 = select i1 %79, i1 %80, i1 %81
  br i1 %82, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %83 = load %Array*, %Array** %2, align 8
  %84 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %83, i64 %__qsVar1__idx__)
  %85 = bitcast i8* %84 to %Qubit**
  %86 = load %Qubit*, %Qubit** %85, align 8
  %87 = load %Array*, %Array** %6, align 8
  %88 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %87, i64 %__qsVar1__idx__)
  %89 = bitcast i8* %88 to %Qubit**
  %90 = load %Qubit*, %Qubit** %89, align 8
  %91 = add i64 %__qsVar1__idx__, 1
  %92 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %83, i64 %91)
  %93 = bitcast i8* %92 to %Qubit**
  %94 = load %Qubit*, %Qubit** %93, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %86, %Qubit* %90, %Qubit* %94)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %95 = add i64 %__qsVar1__idx__, %77
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 -1)
  %96 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %96, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  %97 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %97, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %52, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____body({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 0)
  %7 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %8 = bitcast %Tuple* %7 to { { %Array* }*, { %Array* }* }*
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %8, i32 0, i32 0
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %8, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %9, align 8
  store { %Array* }* %ys, { %Array* }** %10, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctl(%Array* %6, { { %Array* }*, { %Array* }* }* %8)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctl(%Array* %controls, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %9, %String* %10)
  %11 = sub i64 %nQubits, 2
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %idx = phi i64 [ 0, %entry ], [ %25, %exiting__1 ]
  %12 = icmp sle i64 %idx, %11
  br i1 %12, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %13 = load %Array*, %Array** %2, align 8
  %14 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %13, i64 %idx)
  %15 = bitcast i8* %14 to %Qubit**
  %16 = load %Qubit*, %Qubit** %15, align 8
  %17 = load %Array*, %Array** %6, align 8
  %18 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %17, i64 %idx)
  %19 = bitcast i8* %18 to %Qubit**
  %20 = load %Qubit*, %Qubit** %19, align 8
  %21 = add i64 %idx, 1
  %22 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %13, i64 %21)
  %23 = bitcast i8* %22 to %Qubit**
  %24 = load %Qubit*, %Qubit** %23, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %16, %Qubit* %20, %Qubit* %24)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %25 = add i64 %idx, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %26 = sub i64 %nQubits, 1
  br label %preheader__1

preheader__1:                                     ; preds = %exit__1
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__1
  %idx__1 = phi i64 [ %26, %preheader__1 ], [ %53, %exiting__2 ]
  %27 = icmp sle i64 %idx__1, 1
  %28 = icmp sge i64 %idx__1, 1
  %29 = select i1 false, i1 %27, i1 %28
  br i1 %29, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %30 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %31 = bitcast %Tuple* %30 to { %Qubit*, %Qubit* }*
  %32 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %31, i32 0, i32 0
  %33 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %31, i32 0, i32 1
  %34 = load %Array*, %Array** %2, align 8
  %35 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %34, i64 %idx__1)
  %36 = bitcast i8* %35 to %Qubit**
  %37 = load %Qubit*, %Qubit** %36, align 8
  %38 = load %Array*, %Array** %6, align 8
  %39 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %38, i64 %idx__1)
  %40 = bitcast i8* %39 to %Qubit**
  %41 = load %Qubit*, %Qubit** %40, align 8
  store %Qubit* %37, %Qubit** %32, align 8
  store %Qubit* %41, %Qubit** %33, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %controls, { %Qubit*, %Qubit* }* %31)
  %42 = sub i64 %idx__1, 1
  %43 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %34, i64 %42)
  %44 = bitcast i8* %43 to %Qubit**
  %45 = load %Qubit*, %Qubit** %44, align 8
  %46 = sub i64 %idx__1, 1
  %47 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %38, i64 %46)
  %48 = bitcast i8* %47 to %Qubit**
  %49 = load %Qubit*, %Qubit** %48, align 8
  %50 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %34, i64 %idx__1)
  %51 = bitcast i8* %50 to %Qubit**
  %52 = load %Qubit*, %Qubit** %51, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %45, %Qubit* %49, %Qubit* %52)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %30, i32 -1)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %53 = add i64 %idx__1, -1
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 -1)
  %54 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %54, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  %55 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %55, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____adj({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Array* @__quantum__rt__array_create_1d(i32 8, i64 0)
  %7 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %8 = bitcast %Tuple* %7 to { { %Array* }*, { %Array* }* }*
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %8, i32 0, i32 0
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %8, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %9, align 8
  store { %Array* }* %ys, { %Array* }** %10, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctladj(%Array* %6, { { %Array* }*, { %Array* }* }* %8)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %6, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctladj(%Array* %controls, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %9, %String* %10)
  %11 = sub i64 %__qsVar0__nQubits__, 1
  %12 = sub i64 1, %11
  %13 = sdiv i64 %12, -1
  %14 = mul i64 -1, %13
  %15 = add i64 %11, %14
  %16 = load %Range, %Range* @EmptyRange, align 4
  %17 = insertvalue %Range %16, i64 %15, 0
  %18 = insertvalue %Range %17, i64 1, 1
  %19 = insertvalue %Range %18, i64 %11, 2
  %20 = extractvalue %Range %19, 0
  %21 = extractvalue %Range %19, 1
  %22 = extractvalue %Range %19, 2
  br label %preheader__1

preheader__1:                                     ; preds = %entry
  %23 = icmp sgt i64 %21, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar2__idx__ = phi i64 [ %20, %preheader__1 ], [ %50, %exiting__1 ]
  %24 = icmp sle i64 %__qsVar2__idx__, %22
  %25 = icmp sge i64 %__qsVar2__idx__, %22
  %26 = select i1 %23, i1 %24, i1 %25
  br i1 %26, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %27 = load %Array*, %Array** %2, align 8
  %28 = sub i64 %__qsVar2__idx__, 1
  %29 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %27, i64 %28)
  %30 = bitcast i8* %29 to %Qubit**
  %31 = load %Qubit*, %Qubit** %30, align 8
  %32 = load %Array*, %Array** %6, align 8
  %33 = sub i64 %__qsVar2__idx__, 1
  %34 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %32, i64 %33)
  %35 = bitcast i8* %34 to %Qubit**
  %36 = load %Qubit*, %Qubit** %35, align 8
  %37 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %27, i64 %__qsVar2__idx__)
  %38 = bitcast i8* %37 to %Qubit**
  %39 = load %Qubit*, %Qubit** %38, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %31, %Qubit* %36, %Qubit* %39)
  %40 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %41 = bitcast %Tuple* %40 to { %Qubit*, %Qubit* }*
  %42 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %41, i32 0, i32 0
  %43 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %41, i32 0, i32 1
  %44 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %27, i64 %__qsVar2__idx__)
  %45 = bitcast i8* %44 to %Qubit**
  %46 = load %Qubit*, %Qubit** %45, align 8
  %47 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %32, i64 %__qsVar2__idx__)
  %48 = bitcast i8* %47 to %Qubit**
  %49 = load %Qubit*, %Qubit** %48, align 8
  store %Qubit* %46, %Qubit** %42, align 8
  store %Qubit* %49, %Qubit** %43, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %controls, { %Qubit*, %Qubit* }* %41)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %40, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %50 = add i64 %__qsVar2__idx__, %21
  br label %header__1

exit__1:                                          ; preds = %header__1
  %51 = sub i64 %__qsVar0__nQubits__, 2
  %52 = sub i64 %51, 0
  %53 = sdiv i64 %52, 1
  %54 = mul i64 1, %53
  %55 = add i64 0, %54
  %56 = load %Range, %Range* @EmptyRange, align 4
  %57 = insertvalue %Range %56, i64 %55, 0
  %58 = insertvalue %Range %57, i64 -1, 1
  %59 = insertvalue %Range %58, i64 0, 2
  %60 = extractvalue %Range %59, 0
  %61 = extractvalue %Range %59, 1
  %62 = extractvalue %Range %59, 2
  br label %preheader__2

preheader__2:                                     ; preds = %exit__1
  %63 = icmp sgt i64 %61, 0
  br label %header__2

header__2:                                        ; preds = %exiting__2, %preheader__2
  %__qsVar1__idx__ = phi i64 [ %60, %preheader__2 ], [ %79, %exiting__2 ]
  %64 = icmp sle i64 %__qsVar1__idx__, %62
  %65 = icmp sge i64 %__qsVar1__idx__, %62
  %66 = select i1 %63, i1 %64, i1 %65
  br i1 %66, label %body__2, label %exit__2

body__2:                                          ; preds = %header__2
  %67 = load %Array*, %Array** %2, align 8
  %68 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %67, i64 %__qsVar1__idx__)
  %69 = bitcast i8* %68 to %Qubit**
  %70 = load %Qubit*, %Qubit** %69, align 8
  %71 = load %Array*, %Array** %6, align 8
  %72 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %71, i64 %__qsVar1__idx__)
  %73 = bitcast i8* %72 to %Qubit**
  %74 = load %Qubit*, %Qubit** %73, align 8
  %75 = add i64 %__qsVar1__idx__, 1
  %76 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %67, i64 %75)
  %77 = bitcast i8* %76 to %Qubit**
  %78 = load %Qubit*, %Qubit** %77, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %70, %Qubit* %74, %Qubit* %78)
  br label %exiting__2

exiting__2:                                       ; preds = %body__2
  %79 = add i64 %__qsVar1__idx__, %61
  br label %header__2

exit__2:                                          ; preds = %header__2
  call void @__quantum__rt__array_update_alias_count(%Array* %controls, i32 -1)
  %80 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %80, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  %81 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %81, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____body({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %6, %String* %7)
  %8 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %9 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %1)
  %10 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %4)
  %11 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %9, %Array* %10)
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__body(%Callable* %8, %Array* %11)
  %12 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %1)
  call void @Microsoft__Quantum__Canon__ApplyCNOTChain__adj(%Array* %12)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %8, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %8, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %9, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %10, i32 -1)
  %13 = call i64 @__quantum__rt__array_get_size_1d(%Array* %11)
  %14 = sub i64 %13, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %15 = phi i64 [ 0, %entry ], [ %21, %exiting__1 ]
  %16 = icmp sle i64 %15, %14
  br i1 %16, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %11, i64 %15)
  %18 = bitcast i8* %17 to { %Qubit*, %Qubit* }**
  %19 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %18, align 8
  %20 = bitcast { %Qubit*, %Qubit* }* %19 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %20, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %21 = add i64 %15, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %11, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____adj({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %6, %String* %7)
  %8 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %1)
  call void @Microsoft__Quantum__Canon__ApplyCNOTChain__body(%Array* %8)
  %9 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %10 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %1)
  %11 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %4)
  %12 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %10, %Array* %11)
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__adj(%Callable* %9, %Array* %12)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %10, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %11, i32 -1)
  %13 = call i64 @__quantum__rt__array_get_size_1d(%Array* %12)
  %14 = sub i64 %13, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %15 = phi i64 [ 0, %entry ], [ %21, %exiting__1 ]
  %16 = icmp sle i64 %15, %14
  br i1 %16, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %17 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %12, i64 %15)
  %18 = bitcast i8* %17 to { %Qubit*, %Qubit* }**
  %19 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %18, align 8
  %20 = bitcast { %Qubit*, %Qubit* }* %19 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %20, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %21 = add i64 %15, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %9, %String* %10)
  %11 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %12 = bitcast %Tuple* %11 to { %Callable*, %Array* }*
  %13 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %12, i32 0, i32 0
  %14 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %12, i32 0, i32 1
  %15 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %16 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %3)
  %17 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %7)
  %18 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %16, %Array* %17)
  call void @__quantum__rt__array_update_reference_count(%Array* %16, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %17, i32 -1)
  store %Callable* %15, %Callable** %13, align 8
  store %Array* %18, %Array** %14, align 8
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctl(%Array* %__controlQubits__, { %Callable*, %Array* }* %12)
  %19 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %3)
  call void @Microsoft__Quantum__Canon__ApplyCNOTChain__ctladj(%Array* %__controlQubits__, %Array* %19)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  %20 = call i64 @__quantum__rt__array_get_size_1d(%Array* %18)
  %21 = sub i64 %20, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %22 = phi i64 [ 0, %entry ], [ %28, %exiting__1 ]
  %23 = icmp sle i64 %22, %21
  br i1 %23, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %24 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %18, i64 %22)
  %25 = bitcast i8* %24 to { %Qubit*, %Qubit* }**
  %26 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %25, align 8
  %27 = bitcast { %Qubit*, %Qubit* }* %26 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %27, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %28 = add i64 %22, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %18, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %11, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %19, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %9, %String* %10)
  %11 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %3)
  call void @Microsoft__Quantum__Canon__ApplyCNOTChain__ctl(%Array* %__controlQubits__, %Array* %11)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Callable*, %Array* }*
  %14 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Callable*, %Array* }, { %Callable*, %Array* }* %13, i32 0, i32 1
  %16 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Intrinsic__CNOT__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %17 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %3)
  %18 = call %Array* @Microsoft__Quantum__Arrays___ca7ee916220f487e9e4fd3c5f291ea3b_Rest__body(%Array* %7)
  %19 = call %Array* @Microsoft__Quantum__Arrays___d1028568f5b64018af3baa7e25c137c1_Zipped__body(%Array* %17, %Array* %18)
  call void @__quantum__rt__array_update_reference_count(%Array* %17, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %18, i32 -1)
  store %Callable* %16, %Callable** %14, align 8
  store %Array* %19, %Array** %15, align 8
  call void @Microsoft__Quantum__Canon___71b76e8d558d4207b32c5dd013e30daa_ApplyToEachCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Array* }* %13)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %11, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %16, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %16, i32 -1)
  %20 = call i64 @__quantum__rt__array_get_size_1d(%Array* %19)
  %21 = sub i64 %20, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %22 = phi i64 [ 0, %entry ], [ %28, %exiting__1 ]
  %23 = icmp sle i64 %22, %21
  br i1 %23, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %24 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %19, i64 %22)
  %25 = bitcast i8* %24 to { %Qubit*, %Qubit* }**
  %26 = load { %Qubit*, %Qubit* }*, { %Qubit*, %Qubit* }** %25, align 8
  %27 = bitcast { %Qubit*, %Qubit* }* %26 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %27, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %28 = add i64 %22, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_reference_count(%Array* %19, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__body({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = icmp eq i64 %nQubits, %6
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %7, i1 true, %String* %8)
  %9 = icmp sgt i64 %nQubits, 1
  br i1 %9, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  %10 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %11 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %14, align 8
  store { %Array* }* %ys, { %Array* }** %15, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__body(%Callable* %10, %Callable* %11, { { %Array* }*, { %Array* }* }* %13)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %11, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  %16 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %17 = bitcast i8* %16 to %Qubit**
  %18 = load %Qubit*, %Qubit** %17, align 8
  %19 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %20 = bitcast i8* %19 to %Qubit**
  %21 = load %Qubit*, %Qubit** %20, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %18, %Qubit* %21)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__body({ %Array* }* %xs, { %Array* }* %ys, %Qubit* %carry) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %6, %String* %7)
  %8 = icmp sgt i64 %nQubits, 1
  br i1 %8, label %then0__1, label %else__1

then0__1:                                         ; preds = %entry
  %9 = sub i64 %nQubits, 1
  %10 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 %9)
  %11 = bitcast i8* %10 to %Qubit**
  %12 = load %Qubit*, %Qubit** %11, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %12, %Qubit* %carry)
  %13 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %14 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %15 = bitcast %Tuple* %14 to { %Callable*, %Qubit* }*
  %16 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %15, i32 0, i32 0
  %17 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %15, i32 0, i32 1
  %18 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %18, %Callable** %16, align 8
  store %Qubit* %carry, %Qubit** %17, align 8
  %19 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__5__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__2__FunctionTable, %Tuple* %14)
  %20 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %21 = bitcast %Tuple* %20 to { { %Array* }*, { %Array* }* }*
  %22 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %21, i32 0, i32 0
  %23 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %21, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %22, align 8
  store { %Array* }* %ys, { %Array* }** %23, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__body(%Callable* %13, %Callable* %19, { { %Array* }*, { %Array* }* }* %21)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %13, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %13, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %19, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %19, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %20, i32 -1)
  br label %continue__1

else__1:                                          ; preds = %entry
  %24 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %25 = bitcast i8* %24 to %Qubit**
  %26 = load %Qubit*, %Qubit** %25, align 8
  %27 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %28 = bitcast i8* %27 to %Qubit**
  %29 = load %Qubit*, %Qubit** %28, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__body(%Qubit* %26, %Qubit* %29, %Qubit* %carry)
  br label %continue__1

continue__1:                                      ; preds = %else__1, %then0__1
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  %33 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %34 = bitcast i8* %33 to %Qubit**
  %35 = load %Qubit*, %Qubit** %34, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__body(%Qubit* %32, %Qubit* %35)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__AddI__adj({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %7 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %8 = icmp eq i64 %6, %7
  br i1 %8, label %then0__1, label %test1__1

then0__1:                                         ; preds = %entry
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__adj({ %Array* }* %xs, { %Array* }* %ys)
  br label %continue__1

test1__1:                                         ; preds = %entry
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %11 = icmp sgt i64 %9, %10
  br i1 %11, label %then1__1, label %else__1

then1__1:                                         ; preds = %test1__1
  %12 = sub i64 %9, %10
  %13 = sub i64 %12, 1
  %__qsVar0__qs__ = call %Array* @__quantum__rt__qubit_allocate_array(i64 %13)
  call void @__quantum__rt__array_update_alias_count(%Array* %__qsVar0__qs__, i32 1)
  %14 = call %Array* @__quantum__rt__array_concatenate(%Array* %1, %Array* %__qsVar0__qs__)
  %15 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %14)
  %16 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %4)
  %17 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %16)
  %18 = call %Qubit* @Microsoft__Quantum__Arrays___651e5e7f272044f08a0bf7935d1f86ab_Tail__body(%Array* %4)
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__adj({ %Array* }* %15, { %Array* }* %17, %Qubit* %18)
  %19 = getelementptr inbounds { %Array* }, { %Array* }* %15, i32 0, i32 0
  %20 = load %Array*, %Array** %19, align 8
  %21 = getelementptr inbounds { %Array* }, { %Array* }* %17, i32 0, i32 0
  %22 = load %Array*, %Array** %21, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__qsVar0__qs__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %14, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %20, i32 -1)
  %23 = bitcast { %Array* }* %15 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %23, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %16, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %22, i32 -1)
  %24 = bitcast { %Array* }* %17 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %24, i32 -1)
  call void @__quantum__rt__qubit_release_array(%Array* %__qsVar0__qs__)
  br label %continue__1

else__1:                                          ; preds = %test1__1
  %25 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @21, i32 0, i32 0))
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__fail(%String* %25)
  unreachable

continue__1:                                      ; preds = %then1__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__adj({ %Array* }* %xs, { %Array* }* %ys) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = icmp eq i64 %__qsVar0__nQubits__, %6
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %7, i1 true, %String* %8)
  %9 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %10 = bitcast i8* %9 to %Qubit**
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %13 = bitcast i8* %12 to %Qubit**
  %14 = load %Qubit*, %Qubit** %13, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %11, %Qubit* %14)
  %15 = icmp sgt i64 %__qsVar0__nQubits__, 1
  br i1 %15, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  %16 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %17 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %18 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %19 = bitcast %Tuple* %18 to { { %Array* }*, { %Array* }* }*
  %20 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %19, i32 0, i32 0
  %21 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %19, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %20, align 8
  store { %Array* }* %ys, { %Array* }** %21, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__adj(%Callable* %16, %Callable* %17, { { %Array* }*, { %Array* }* }* %19)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %16, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %16, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %17, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %17, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %18, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__adj({ %Array* }* %xs, { %Array* }* %ys, %Qubit* %carry) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %6 = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %7 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %6, %String* %7)
  %8 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %9 = bitcast i8* %8 to %Qubit**
  %10 = load %Qubit*, %Qubit** %9, align 8
  %11 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %12 = bitcast i8* %11 to %Qubit**
  %13 = load %Qubit*, %Qubit** %12, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %10, %Qubit* %13)
  %14 = icmp sgt i64 %__qsVar0__nQubits__, 1
  br i1 %14, label %then0__1, label %else__1

then0__1:                                         ; preds = %entry
  %15 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %16 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %17 = bitcast %Tuple* %16 to { %Callable*, %Qubit* }*
  %18 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %17, i32 0, i32 0
  %19 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %17, i32 0, i32 1
  %20 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %20, %Callable** %18, align 8
  store %Qubit* %carry, %Qubit** %19, align 8
  %21 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__6__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__2__FunctionTable, %Tuple* %16)
  %22 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %23 = bitcast %Tuple* %22 to { { %Array* }*, { %Array* }* }*
  %24 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %23, i32 0, i32 0
  %25 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %23, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store { %Array* }* %xs, { %Array* }** %24, align 8
  store { %Array* }* %ys, { %Array* }** %25, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__adj(%Callable* %15, %Callable* %21, { { %Array* }*, { %Array* }* }* %23)
  %26 = sub i64 %__qsVar0__nQubits__, 1
  %27 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 %26)
  %28 = bitcast i8* %27 to %Qubit**
  %29 = load %Qubit*, %Qubit** %28, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__adj(%Qubit* %29, %Qubit* %carry)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %21, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %21, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %22, i32 -1)
  br label %continue__1

else__1:                                          ; preds = %entry
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %1, i64 0)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  %33 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %4, i64 0)
  %34 = bitcast i8* %33 to %Qubit**
  %35 = load %Qubit*, %Qubit** %34, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__adj(%Qubit* %32, %Qubit* %35, %Qubit* %carry)
  br label %continue__1

continue__1:                                      ; preds = %else__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__AddI__ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = icmp eq i64 %9, %10
  br i1 %11, label %then0__1, label %test1__1

then0__1:                                         ; preds = %entry
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %14, align 8
  store { %Array* }* %ys, { %Array* }** %15, align 8
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %13)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  br label %continue__1

test1__1:                                         ; preds = %entry
  %16 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %17 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %18 = icmp sgt i64 %16, %17
  br i1 %18, label %then1__1, label %else__1

then1__1:                                         ; preds = %test1__1
  %19 = sub i64 %16, %17
  %20 = sub i64 %19, 1
  %qs = call %Array* @__quantum__rt__qubit_allocate_array(i64 %20)
  call void @__quantum__rt__array_update_alias_count(%Array* %qs, i32 1)
  %21 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %22 = bitcast %Tuple* %21 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %23 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 0
  %24 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 1
  %25 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 2
  %26 = call %Array* @__quantum__rt__array_concatenate(%Array* %3, %Array* %qs)
  %27 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %26)
  call void @__quantum__rt__array_update_reference_count(%Array* %26, i32 -1)
  %28 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %7)
  %29 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %28)
  call void @__quantum__rt__array_update_reference_count(%Array* %28, i32 -1)
  %30 = call %Qubit* @Microsoft__Quantum__Arrays___651e5e7f272044f08a0bf7935d1f86ab_Tail__body(%Array* %7)
  store { %Array* }* %27, { %Array* }** %23, align 8
  store { %Array* }* %29, { %Array* }** %24, align 8
  store %Qubit* %30, %Qubit** %25, align 8
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }*, %Qubit* }* %22)
  %31 = getelementptr inbounds { %Array* }, { %Array* }* %27, i32 0, i32 0
  %32 = load %Array*, %Array** %31, align 8
  %33 = getelementptr inbounds { %Array* }, { %Array* }* %29, i32 0, i32 0
  %34 = load %Array*, %Array** %33, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %qs, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %32, i32 -1)
  %35 = bitcast { %Array* }* %27 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %35, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %34, i32 -1)
  %36 = bitcast { %Array* }* %29 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %36, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %21, i32 -1)
  call void @__quantum__rt__qubit_release_array(%Array* %qs)
  br label %continue__1

else__1:                                          ; preds = %test1__1
  %37 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @21, i32 0, i32 0))
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__fail(%String* %37)
  unreachable

continue__1:                                      ; preds = %then1__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = icmp eq i64 %nQubits, %9
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %10, i1 true, %String* %11)
  %12 = icmp sgt i64 %nQubits, 1
  br i1 %12, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  %13 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %14 = bitcast %Tuple* %13 to { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }*
  %15 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %14, i32 0, i32 0
  %16 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %14, i32 0, i32 1
  %17 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %14, i32 0, i32 2
  %18 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %19 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %20 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %21 = bitcast %Tuple* %20 to { { %Array* }*, { %Array* }* }*
  %22 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %21, i32 0, i32 0
  %23 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %21, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %22, align 8
  store { %Array* }* %ys, { %Array* }** %23, align 8
  store %Callable* %18, %Callable** %15, align 8
  store %Callable* %19, %Callable** %16, align 8
  store { { %Array* }*, { %Array* }* }* %21, { { %Array* }*, { %Array* }* }** %17, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctl(%Array* %__controlQubits__, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %14)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %19, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %19, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %20, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  %24 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %25 = bitcast %Tuple* %24 to { %Qubit*, %Qubit* }*
  %26 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %25, i32 0, i32 0
  %27 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %25, i32 0, i32 1
  %28 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %29 = bitcast i8* %28 to %Qubit**
  %30 = load %Qubit*, %Qubit** %29, align 8
  %31 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %32 = bitcast i8* %31 to %Qubit**
  %33 = load %Qubit*, %Qubit** %32, align 8
  store %Qubit* %30, %Qubit** %26, align 8
  store %Qubit* %33, %Qubit** %27, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %25)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %24, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__ctl(%Array* %__controlQubits__, { { %Array* }*, { %Array* }*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %carry = load %Qubit*, %Qubit** %9, align 8
  %nQubits = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %nQubits, i64 %10, %String* %11)
  %12 = icmp sgt i64 %nQubits, 1
  br i1 %12, label %then0__1, label %else__1

then0__1:                                         ; preds = %entry
  %13 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %14 = bitcast %Tuple* %13 to { %Qubit*, %Qubit* }*
  %15 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %14, i32 0, i32 0
  %16 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %14, i32 0, i32 1
  %17 = sub i64 %nQubits, 1
  %18 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 %17)
  %19 = bitcast i8* %18 to %Qubit**
  %20 = load %Qubit*, %Qubit** %19, align 8
  store %Qubit* %20, %Qubit** %15, align 8
  store %Qubit* %carry, %Qubit** %16, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %14)
  %21 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %22 = bitcast %Tuple* %21 to { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }*
  %23 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %22, i32 0, i32 0
  %24 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %22, i32 0, i32 1
  %25 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %22, i32 0, i32 2
  %26 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %27 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %28 = bitcast %Tuple* %27 to { %Callable*, %Qubit* }*
  %29 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %28, i32 0, i32 0
  %30 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %28, i32 0, i32 1
  %31 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %31, %Callable** %29, align 8
  store %Qubit* %carry, %Qubit** %30, align 8
  %32 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__7__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__2__FunctionTable, %Tuple* %27)
  %33 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %34 = bitcast %Tuple* %33 to { { %Array* }*, { %Array* }* }*
  %35 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %34, i32 0, i32 0
  %36 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %34, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %35, align 8
  store { %Array* }* %ys, { %Array* }** %36, align 8
  store %Callable* %26, %Callable** %23, align 8
  store %Callable* %32, %Callable** %24, align 8
  store { { %Array* }*, { %Array* }* }* %34, { { %Array* }*, { %Array* }* }** %25, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctl(%Array* %__controlQubits__, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %22)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %13, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %26, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %26, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %32, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %32, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %33, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %21, i32 -1)
  br label %continue__1

else__1:                                          ; preds = %entry
  %37 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %38 = bitcast %Tuple* %37 to { %Qubit*, %Qubit*, %Qubit* }*
  %39 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %38, i32 0, i32 0
  %40 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %38, i32 0, i32 1
  %41 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %38, i32 0, i32 2
  %42 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %43 = bitcast i8* %42 to %Qubit**
  %44 = load %Qubit*, %Qubit** %43, align 8
  %45 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %46 = bitcast i8* %45 to %Qubit**
  %47 = load %Qubit*, %Qubit** %46, align 8
  store %Qubit* %44, %Qubit** %39, align 8
  store %Qubit* %47, %Qubit** %40, align 8
  store %Qubit* %carry, %Qubit** %41, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit*, %Qubit* }* %38)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %37, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %else__1, %then0__1
  %48 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %49 = bitcast %Tuple* %48 to { %Qubit*, %Qubit* }*
  %50 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %49, i32 0, i32 0
  %51 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %49, i32 0, i32 1
  %52 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %53 = bitcast i8* %52 to %Qubit**
  %54 = load %Qubit*, %Qubit** %53, align 8
  %55 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %56 = bitcast i8* %55 to %Qubit**
  %57 = load %Qubit*, %Qubit** %56, align 8
  store %Qubit* %54, %Qubit** %50, align 8
  store %Qubit* %57, %Qubit** %51, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctl(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %49)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %48, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__AddI__ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = icmp eq i64 %9, %10
  br i1 %11, label %then0__1, label %test1__1

then0__1:                                         ; preds = %entry
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %13, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %14, align 8
  store { %Array* }* %ys, { %Array* }** %15, align 8
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %13)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  br label %continue__1

test1__1:                                         ; preds = %entry
  %16 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %17 = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %18 = icmp sgt i64 %16, %17
  br i1 %18, label %then1__1, label %else__1

then1__1:                                         ; preds = %test1__1
  %19 = sub i64 %16, %17
  %20 = sub i64 %19, 1
  %__qsVar0__qs__ = call %Array* @__quantum__rt__qubit_allocate_array(i64 %20)
  call void @__quantum__rt__array_update_alias_count(%Array* %__qsVar0__qs__, i32 1)
  %21 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %22 = bitcast %Tuple* %21 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %23 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 0
  %24 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 1
  %25 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %22, i32 0, i32 2
  %26 = call %Array* @__quantum__rt__array_concatenate(%Array* %3, %Array* %__qsVar0__qs__)
  %27 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %26)
  call void @__quantum__rt__array_update_reference_count(%Array* %26, i32 -1)
  %28 = call %Array* @Microsoft__Quantum__Arrays___8a833c914a8f4f95b4a7f8dcc7072f54_Most__body(%Array* %7)
  %29 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndian__body(%Array* %28)
  call void @__quantum__rt__array_update_reference_count(%Array* %28, i32 -1)
  %30 = call %Qubit* @Microsoft__Quantum__Arrays___651e5e7f272044f08a0bf7935d1f86ab_Tail__body(%Array* %7)
  store { %Array* }* %27, { %Array* }** %23, align 8
  store { %Array* }* %29, { %Array* }** %24, align 8
  store %Qubit* %30, %Qubit** %25, align 8
  call void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }*, %Qubit* }* %22)
  %31 = getelementptr inbounds { %Array* }, { %Array* }* %27, i32 0, i32 0
  %32 = load %Array*, %Array** %31, align 8
  %33 = getelementptr inbounds { %Array* }, { %Array* }* %29, i32 0, i32 0
  %34 = load %Array*, %Array** %33, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %__qsVar0__qs__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %32, i32 -1)
  %35 = bitcast { %Array* }* %27 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %35, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %34, i32 -1)
  %36 = bitcast { %Array* }* %29 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %36, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %21, i32 -1)
  call void @__quantum__rt__qubit_release_array(%Array* %__qsVar0__qs__)
  br label %continue__1

else__1:                                          ; preds = %test1__1
  %37 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @21, i32 0, i32 0))
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__fail(%String* %37)
  unreachable

continue__1:                                      ; preds = %then1__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderNoCarryTTK__ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %9 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %10 = icmp eq i64 %__qsVar0__nQubits__, %9
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactB__body(i1 %10, i1 true, %String* %11)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Qubit*, %Qubit* }*
  %14 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %13, i32 0, i32 1
  %16 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %17 = bitcast i8* %16 to %Qubit**
  %18 = load %Qubit*, %Qubit** %17, align 8
  %19 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %20 = bitcast i8* %19 to %Qubit**
  %21 = load %Qubit*, %Qubit** %20, align 8
  store %Qubit* %18, %Qubit** %14, align 8
  store %Qubit* %21, %Qubit** %15, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %13)
  %22 = icmp sgt i64 %__qsVar0__nQubits__, 1
  br i1 %22, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  %23 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %24 = bitcast %Tuple* %23 to { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }*
  %25 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 0
  %26 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 1
  %27 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 2
  %28 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %29 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %30 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %31 = bitcast %Tuple* %30 to { { %Array* }*, { %Array* }* }*
  %32 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %31, i32 0, i32 0
  %33 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %31, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %32, align 8
  store { %Array* }* %ys, { %Array* }** %33, align 8
  store %Callable* %28, %Callable** %25, align 8
  store %Callable* %29, %Callable** %26, align 8
  store { { %Array* }*, { %Array* }* }* %31, { { %Array* }*, { %Array* }* }** %27, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %28, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %28, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %29, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %29, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %30, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %23, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__RippleCarryAdderTTK__ctladj(%Array* %__controlQubits__, { { %Array* }*, { %Array* }*, %Qubit* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %xs = load { %Array* }*, { %Array* }** %1, align 8
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %xs, i32 0, i32 0
  %3 = load %Array*, %Array** %2, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 1)
  %4 = bitcast { %Array* }* %xs to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 1)
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %ys = load { %Array* }*, { %Array* }** %5, align 8
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %ys, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %ys to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %carry = load %Qubit*, %Qubit** %9, align 8
  %__qsVar0__nQubits__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %3)
  %10 = call i64 @__quantum__rt__array_get_size_1d(%Array* %7)
  %11 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([53 x i8], [53 x i8]* @20, i32 0, i32 0))
  call void @Microsoft__Quantum__Diagnostics__EqualityFactI__body(i64 %__qsVar0__nQubits__, i64 %10, %String* %11)
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Qubit*, %Qubit* }*
  %14 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %13, i32 0, i32 1
  %16 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %17 = bitcast i8* %16 to %Qubit**
  %18 = load %Qubit*, %Qubit** %17, align 8
  %19 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %20 = bitcast i8* %19 to %Qubit**
  %21 = load %Qubit*, %Qubit** %20, align 8
  store %Qubit* %18, %Qubit** %14, align 8
  store %Qubit* %21, %Qubit** %15, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %13)
  %22 = icmp sgt i64 %__qsVar0__nQubits__, 1
  br i1 %22, label %then0__1, label %else__1

then0__1:                                         ; preds = %entry
  %23 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %24 = bitcast %Tuple* %23 to { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }*
  %25 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 0
  %26 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 1
  %27 = getelementptr inbounds { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24, i32 0, i32 2
  %28 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  %29 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %30 = bitcast %Tuple* %29 to { %Callable*, %Qubit* }*
  %31 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %30, i32 0, i32 0
  %32 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %30, i32 0, i32 1
  %33 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %33, %Callable** %31, align 8
  store %Qubit* %carry, %Qubit** %32, align 8
  %34 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__8__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__2__FunctionTable, %Tuple* %29)
  %35 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %36 = bitcast %Tuple* %35 to { { %Array* }*, { %Array* }* }*
  %37 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %36, i32 0, i32 0
  %38 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %36, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store { %Array* }* %xs, { %Array* }** %37, align 8
  store { %Array* }* %ys, { %Array* }** %38, align 8
  store %Callable* %28, %Callable** %25, align 8
  store %Callable* %34, %Callable** %26, align 8
  store { { %Array* }*, { %Array* }* }* %36, { { %Array* }*, { %Array* }* }** %27, align 8
  call void @Microsoft__Quantum__Canon___66800af3157a4599af2ef7f18a41f3af_ApplyWithCA__ctladj(%Array* %__controlQubits__, { %Callable*, %Callable*, { { %Array* }*, { %Array* }* }* }* %24)
  %39 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %40 = bitcast %Tuple* %39 to { %Qubit*, %Qubit* }*
  %41 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %40, i32 0, i32 0
  %42 = getelementptr inbounds { %Qubit*, %Qubit* }, { %Qubit*, %Qubit* }* %40, i32 0, i32 1
  %43 = sub i64 %__qsVar0__nQubits__, 1
  %44 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 %43)
  %45 = bitcast i8* %44 to %Qubit**
  %46 = load %Qubit*, %Qubit** %45, align 8
  store %Qubit* %46, %Qubit** %41, align 8
  store %Qubit* %carry, %Qubit** %42, align 8
  call void @Microsoft__Quantum__Intrinsic__CNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit* }* %40)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %28, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %28, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %34, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %34, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %35, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %23, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %39, i32 -1)
  br label %continue__1

else__1:                                          ; preds = %entry
  %47 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %48 = bitcast %Tuple* %47 to { %Qubit*, %Qubit*, %Qubit* }*
  %49 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %48, i32 0, i32 0
  %50 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %48, i32 0, i32 1
  %51 = getelementptr inbounds { %Qubit*, %Qubit*, %Qubit* }, { %Qubit*, %Qubit*, %Qubit* }* %48, i32 0, i32 2
  %52 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %3, i64 0)
  %53 = bitcast i8* %52 to %Qubit**
  %54 = load %Qubit*, %Qubit** %53, align 8
  %55 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 0)
  %56 = bitcast i8* %55 to %Qubit**
  %57 = load %Qubit*, %Qubit** %56, align 8
  store %Qubit* %54, %Qubit** %49, align 8
  store %Qubit* %57, %Qubit** %50, align 8
  store %Qubit* %carry, %Qubit** %51, align 8
  call void @Microsoft__Quantum__Intrinsic__CCNOT__ctladj(%Array* %__controlQubits__, { %Qubit*, %Qubit*, %Qubit* }* %48)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %47, i32 -1)
  br label %continue__1

continue__1:                                      ; preds = %else__1, %then0__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %3, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %4, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__body(%Callable* %op, { %Array* }* %target) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__QFTLE__body({ %Array* }* %target)
  %__qsVar0__phaseLE__ = call { %Array* }* @Microsoft__Quantum__Arithmetic__PhaseLittleEndian__body(%Array* %1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %__qsVar0__phaseLE__, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %__qsVar0__phaseLE__ to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  call void @__quantum__rt__callable_invoke(%Callable* %op, %Tuple* %5, %Tuple* null)
  call void @Microsoft__Quantum__Canon__QFTLE__adj({ %Array* }* %target)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  ret void
}

define internal { %Array* }* @Microsoft__Quantum__Arithmetic__PhaseLittleEndian__body(%Array* %__Item1__) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 1)
  %0 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  %1 = bitcast %Tuple* %0 to { %Array* }*
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %1, i32 0, i32 0
  store %Array* %__Item1__, %Array** %2, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %__Item1__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 -1)
  ret { %Array* }* %1
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__adj(%Callable* %op, { %Array* }* %target) {
entry:
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  call void @Microsoft__Quantum__Canon__QFTLE__body({ %Array* }* %target)
  %__qsVar0____qsVar0__phaseLE____ = call { %Array* }* @Microsoft__Quantum__Arithmetic__PhaseLittleEndian__body(%Array* %1)
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %__qsVar0____qsVar0__phaseLE____, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %__qsVar0____qsVar0__phaseLE____ to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %6, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %6)
  call void @__quantum__rt__callable_invoke(%Callable* %6, %Tuple* %5, %Tuple* null)
  call void @Microsoft__Quantum__Canon__QFTLE__adj({ %Array* }* %target)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %6, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %6, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__ctl(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %op = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %2 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  call void @Microsoft__Quantum__Canon__QFTLE__body({ %Array* }* %target)
  %__qsVar0__phaseLE__ = call { %Array* }* @Microsoft__Quantum__Arithmetic__PhaseLittleEndian__body(%Array* %4)
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %__qsVar0__phaseLE__, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %__qsVar0__phaseLE__ to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %9, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %9)
  %10 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %11 = bitcast %Tuple* %10 to { %Array*, { %Array* }* }*
  %12 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %11, i32 0, i32 0
  %13 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %11, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store %Array* %__controlQubits__, %Array** %12, align 8
  store { %Array* }* %__qsVar0__phaseLE__, { %Array* }** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %10, %Tuple* null)
  call void @Microsoft__Quantum__Canon__QFTLE__adj({ %Array* }* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %10, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__ctladj(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 0
  %op = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 1)
  %2 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  call void @Microsoft__Quantum__Canon__QFTLE__body({ %Array* }* %target)
  %__qsVar0____qsVar0__phaseLE____ = call { %Array* }* @Microsoft__Quantum__Arithmetic__PhaseLittleEndian__body(%Array* %4)
  %6 = getelementptr inbounds { %Array* }, { %Array* }* %__qsVar0____qsVar0__phaseLE____, i32 0, i32 0
  %7 = load %Array*, %Array** %6, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 1)
  %8 = bitcast { %Array* }* %__qsVar0____qsVar0__phaseLE____ to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 1)
  %9 = call %Callable* @__quantum__rt__callable_copy(%Callable* %op, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %9, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %9)
  call void @__quantum__rt__callable_make_controlled(%Callable* %9)
  %10 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %11 = bitcast %Tuple* %10 to { %Array*, { %Array* }* }*
  %12 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %11, i32 0, i32 0
  %13 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %11, i32 0, i32 1
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 1)
  store %Array* %__controlQubits__, %Array** %12, align 8
  store { %Array* }* %__qsVar0____qsVar0__phaseLE____, { %Array* }** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %10, %Tuple* null)
  call void @Microsoft__Quantum__Canon__QFTLE__adj({ %Array* }* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__capture_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %op, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %9, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %7, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %10, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array* }*
  %1 = call { %Array* }* @Microsoft__Quantum__Arithmetic__LittleEndianAsBigEndian__body({ %Array* }* %0)
  %2 = bitcast %Tuple* %result-tuple to { { %Array* }* }*
  %3 = getelementptr inbounds { { %Array* }* }, { { %Array* }* }* %2, i32 0, i32 0
  store { %Array* }* %1, { %Array* }** %3, align 8
  ret void
}

define internal { %Array* }* @Microsoft__Quantum__Arithmetic__BigEndian__body(%Array* %__Item1__) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 1)
  %0 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64))
  %1 = bitcast %Tuple* %0 to { %Array* }*
  %2 = getelementptr inbounds { %Array* }, { %Array* }* %1, i32 0, i32 0
  store %Array* %__Item1__, %Array** %2, align 8
  call void @__quantum__rt__array_update_reference_count(%Array* %__Item1__, i32 1)
  call void @__quantum__rt__array_update_alias_count(%Array* %__Item1__, i32 -1)
  ret { %Array* }* %1
}

define internal void @Lifted__PartialApplication__1__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__1__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  %10 = call %Callable* @__quantum__rt__callable_copy(%Callable* %9, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %10)
  call void @__quantum__rt__callable_invoke(%Callable* %10, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %10, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__1__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__1__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %18)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { i64, { %Array* }* }*
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %3 = load i64, i64* %1, align 4
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__body(i64 %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { i64, { %Array* }* }*
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %3 = load i64, i64* %1, align 4
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__adj(i64 %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { i64, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { i64, { %Array* }* }*, { i64, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctl(%Array* %3, { i64, { %Array* }* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { i64, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { i64, { %Array* }* }*, { i64, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctladj(%Array* %3, { i64, { %Array* }* }* %4)
  ret void
}

define internal void @MemoryManagement__1__RefCount(%Tuple* %capture-tuple, i32 %count-change) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %2 = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_reference_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %capture-tuple, i32 %count-change)
  ret void
}

define internal void @MemoryManagement__1__AliasCount(%Tuple* %capture-tuple, i32 %count-change) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %2 = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %capture-tuple, i32 %count-change)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__body(i64 %increment, { %Array* }* %target) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %d = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %3 = sub i64 %d, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %j = phi i64 [ 0, %entry ], [ %11, %exiting__1 ]
  %4 = icmp sle i64 %j, %3
  br i1 %4, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %5 = sub i64 %d, 1
  %6 = sub i64 %5, %j
  %7 = load %Array*, %Array** %0, align 8
  %8 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %7, i64 %j)
  %9 = bitcast i8* %8 to %Qubit**
  %10 = load %Qubit*, %Qubit** %9, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__body(i64 %increment, i64 %6, %Qubit* %10)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %11 = add i64 %j, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  %12 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %12, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__adj(i64 %increment, { %Array* }* %target) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %__qsVar0__d__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %1)
  %3 = sub i64 %__qsVar0__d__, 1
  %4 = sub i64 %3, 0
  %5 = sdiv i64 %4, 1
  %6 = mul i64 1, %5
  %7 = add i64 0, %6
  %8 = load %Range, %Range* @EmptyRange, align 4
  %9 = insertvalue %Range %8, i64 %7, 0
  %10 = insertvalue %Range %9, i64 -1, 1
  %11 = insertvalue %Range %10, i64 0, 2
  %12 = extractvalue %Range %11, 0
  %13 = extractvalue %Range %11, 1
  %14 = extractvalue %Range %11, 2
  br label %preheader__1

preheader__1:                                     ; preds = %entry
  %15 = icmp sgt i64 %13, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar1__j__ = phi i64 [ %12, %preheader__1 ], [ %25, %exiting__1 ]
  %16 = icmp sle i64 %__qsVar1__j__, %14
  %17 = icmp sge i64 %__qsVar1__j__, %14
  %18 = select i1 %15, i1 %16, i1 %17
  br i1 %18, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %19 = sub i64 %__qsVar0__d__, 1
  %20 = sub i64 %19, %__qsVar1__j__
  %21 = load %Array*, %Array** %0, align 8
  %22 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %21, i64 %__qsVar1__j__)
  %23 = bitcast i8* %22 to %Qubit**
  %24 = load %Qubit*, %Qubit** %23, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__adj(i64 %increment, i64 %20, %Qubit* %24)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %25 = add i64 %__qsVar1__j__, %13
  br label %header__1

exit__1:                                          ; preds = %header__1
  %26 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %26, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctl(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %increment = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %d = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %6 = sub i64 %d, 1
  br label %header__1

header__1:                                        ; preds = %exiting__1, %entry
  %j = phi i64 [ 0, %entry ], [ %19, %exiting__1 ]
  %7 = icmp sle i64 %j, %6
  br i1 %7, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, i64, %Qubit* }*
  %10 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %9, i32 0, i32 2
  %13 = sub i64 %d, 1
  %14 = sub i64 %13, %j
  %15 = load %Array*, %Array** %3, align 8
  %16 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %15, i64 %j)
  %17 = bitcast i8* %16 to %Qubit**
  %18 = load %Qubit*, %Qubit** %17, align 8
  store i64 %increment, i64* %10, align 4
  store i64 %14, i64* %11, align 4
  store %Qubit* %18, %Qubit** %12, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctl(%Array* %__controlQubits__, { i64, i64, %Qubit* }* %9)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %19 = add i64 %j, 1
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  %20 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %20, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__ctladj(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %increment = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %__qsVar0__d__ = call i64 @__quantum__rt__array_get_size_1d(%Array* %4)
  %6 = sub i64 %__qsVar0__d__, 1
  %7 = sub i64 %6, 0
  %8 = sdiv i64 %7, 1
  %9 = mul i64 1, %8
  %10 = add i64 0, %9
  %11 = load %Range, %Range* @EmptyRange, align 4
  %12 = insertvalue %Range %11, i64 %10, 0
  %13 = insertvalue %Range %12, i64 -1, 1
  %14 = insertvalue %Range %13, i64 0, 2
  %15 = extractvalue %Range %14, 0
  %16 = extractvalue %Range %14, 1
  %17 = extractvalue %Range %14, 2
  br label %preheader__1

preheader__1:                                     ; preds = %entry
  %18 = icmp sgt i64 %16, 0
  br label %header__1

header__1:                                        ; preds = %exiting__1, %preheader__1
  %__qsVar1__j__ = phi i64 [ %15, %preheader__1 ], [ %33, %exiting__1 ]
  %19 = icmp sle i64 %__qsVar1__j__, %17
  %20 = icmp sge i64 %__qsVar1__j__, %17
  %21 = select i1 %18, i1 %19, i1 %20
  br i1 %21, label %body__1, label %exit__1

body__1:                                          ; preds = %header__1
  %22 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, i64, %Qubit* }* getelementptr ({ i64, i64, %Qubit* }, { i64, i64, %Qubit* }* null, i32 1) to i64))
  %23 = bitcast %Tuple* %22 to { i64, i64, %Qubit* }*
  %24 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %23, i32 0, i32 0
  %25 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %23, i32 0, i32 1
  %26 = getelementptr inbounds { i64, i64, %Qubit* }, { i64, i64, %Qubit* }* %23, i32 0, i32 2
  %27 = sub i64 %__qsVar0__d__, 1
  %28 = sub i64 %27, %__qsVar1__j__
  %29 = load %Array*, %Array** %3, align 8
  %30 = call i8* @__quantum__rt__array_get_element_ptr_1d(%Array* %29, i64 %__qsVar1__j__)
  %31 = bitcast i8* %30 to %Qubit**
  %32 = load %Qubit*, %Qubit** %31, align 8
  store i64 %increment, i64* %24, align 4
  store i64 %28, i64* %25, align 4
  store %Qubit* %32, %Qubit** %26, align 8
  call void @Microsoft__Quantum__Intrinsic__R1Frac__ctladj(%Array* %__controlQubits__, { i64, i64, %Qubit* }* %23)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %22, i32 -1)
  br label %exiting__1

exiting__1:                                       ; preds = %body__1
  %33 = add i64 %__qsVar1__j__, %16
  br label %header__1

exit__1:                                          ; preds = %header__1
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  %34 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %34, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementByInteger__adj(i64 %increment, { %Array* }* %target) {
entry:
  %0 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %1 = load %Array*, %Array** %0, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 1)
  %2 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 1)
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ %Callable*, i64 }* getelementptr ({ %Callable*, i64 }, { %Callable*, i64 }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { %Callable*, i64 }*
  %5 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %4, i32 0, i32 1
  %7 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %7, %Callable** %5, align 8
  store i64 %increment, i64* %6, align 4
  %8 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__2__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__1__FunctionTable, %Tuple* %3)
  call void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__adj(%Callable* %8, { %Array* }* %target)
  call void @__quantum__rt__array_update_alias_count(%Array* %1, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %2, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %8, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %8, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__2__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__2__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  %10 = call %Callable* @__quantum__rt__callable_copy(%Callable* %9, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %10)
  call void @__quantum__rt__callable_invoke(%Callable* %10, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %10, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__2__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__2__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %18)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementByInteger__ctl(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %increment = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %7 = bitcast %Tuple* %6 to { %Callable*, { %Array* }* }*
  %8 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %7, i32 0, i32 0
  %9 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %7, i32 0, i32 1
  %10 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ %Callable*, i64 }* getelementptr ({ %Callable*, i64 }, { %Callable*, i64 }* null, i32 1) to i64))
  %11 = bitcast %Tuple* %10 to { %Callable*, i64 }*
  %12 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %11, i32 0, i32 0
  %13 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %11, i32 0, i32 1
  %14 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %14, %Callable** %12, align 8
  store i64 %increment, i64* %13, align 4
  %15 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__3__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__1__FunctionTable, %Tuple* %10)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store %Callable* %15, %Callable** %8, align 8
  store { %Array* }* %target, { %Array* }** %9, align 8
  call void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__ctl(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %7)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__3__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__3__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  %10 = call %Callable* @__quantum__rt__callable_copy(%Callable* %9, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %10)
  call void @__quantum__rt__callable_invoke(%Callable* %10, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %10, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__3__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__3__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %18)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic__IncrementByInteger__ctladj(%Array* %__controlQubits__, { i64, { %Array* }* }* %0) {
entry:
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 1)
  %1 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 0
  %increment = load i64, i64* %1, align 4
  %2 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %0, i32 0, i32 1
  %target = load { %Array* }*, { %Array* }** %2, align 8
  %3 = getelementptr inbounds { %Array* }, { %Array* }* %target, i32 0, i32 0
  %4 = load %Array*, %Array** %3, align 8
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 1)
  %5 = bitcast { %Array* }* %target to %Tuple*
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 1)
  %6 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %7 = bitcast %Tuple* %6 to { %Callable*, { %Array* }* }*
  %8 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %7, i32 0, i32 0
  %9 = getelementptr inbounds { %Callable*, { %Array* }* }, { %Callable*, { %Array* }* }* %7, i32 0, i32 1
  %10 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ %Callable*, i64 }* getelementptr ({ %Callable*, i64 }, { %Callable*, i64 }* null, i32 1) to i64))
  %11 = bitcast %Tuple* %10 to { %Callable*, i64 }*
  %12 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %11, i32 0, i32 0
  %13 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %11, i32 0, i32 1
  %14 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @Microsoft__Quantum__Arithmetic__IncrementPhaseByInteger__FunctionTable, [2 x void (%Tuple*, i32)*]* null, %Tuple* null)
  store %Callable* %14, %Callable** %12, align 8
  store i64 %increment, i64* %13, align 4
  %15 = call %Callable* @__quantum__rt__callable_create([4 x void (%Tuple*, %Tuple*, %Tuple*)*]* @PartialApplication__4__FunctionTable, [2 x void (%Tuple*, i32)*]* @MemoryManagement__1__FunctionTable, %Tuple* %10)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 1)
  store %Callable* %15, %Callable** %8, align 8
  store { %Array* }* %target, { %Array* }** %9, align 8
  call void @Microsoft__Quantum__Arithmetic__ApplyPhaseLEOperationOnLECA__ctladj(%Array* %__controlQubits__, { %Callable*, { %Array* }* }* %7)
  call void @__quantum__rt__array_update_alias_count(%Array* %__controlQubits__, i32 -1)
  call void @__quantum__rt__array_update_alias_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__array_update_reference_count(%Array* %4, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %5, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %6, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__4__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %9, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__4__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %1 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 1
  %2 = load i64, i64* %1, align 4
  %3 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %4 = bitcast %Tuple* %3 to { i64, { %Array* }* }*
  %5 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 0
  %6 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %4, i32 0, i32 1
  store i64 %2, i64* %5, align 4
  %7 = bitcast %Tuple* %arg-tuple to { %Array* }*
  store { %Array* }* %7, { %Array* }** %6, align 8
  %8 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %0, i32 0, i32 0
  %9 = load %Callable*, %Callable** %8, align 8
  %10 = call %Callable* @__quantum__rt__callable_copy(%Callable* %9, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %10)
  call void @__quantum__rt__callable_invoke(%Callable* %10, %Tuple* %3, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %3, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %10, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %10, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__4__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__4__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { %Array* }* }*
  %1 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { %Array* }* }, { %Array*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, i64 }*
  %6 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 1
  %7 = load i64, i64* %6, align 4
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 ptrtoint ({ i64, { %Array* }* }* getelementptr ({ i64, { %Array* }* }, { i64, { %Array* }* }* null, i32 1) to i64))
  %9 = bitcast %Tuple* %8 to { i64, { %Array* }* }*
  %10 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { i64, { %Array* }* }, { i64, { %Array* }* }* %9, i32 0, i32 1
  store i64 %7, i64* %10, align 4
  store { %Array* }* %4, { %Array* }** %11, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %13 = bitcast %Tuple* %12 to { %Array*, { i64, { %Array* }* }* }*
  %14 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { %Array*, { i64, { %Array* }* }* }, { %Array*, { i64, { %Array* }* }* }* %13, i32 0, i32 1
  store %Array* %3, %Array** %14, align 8
  store { i64, { %Array* }* }* %9, { i64, { %Array* }* }** %15, align 8
  %16 = getelementptr inbounds { %Callable*, i64 }, { %Callable*, i64 }* %5, i32 0, i32 0
  %17 = load %Callable*, %Callable** %16, align 8
  %18 = call %Callable* @__quantum__rt__callable_copy(%Callable* %17, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %18)
  call void @__quantum__rt__callable_make_controlled(%Callable* %18)
  call void @__quantum__rt__callable_invoke(%Callable* %18, %Tuple* %12, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %18, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %18, i32 -1)
  ret void
}

declare void @__quantum__rt__result_update_reference_count(%Result*, i32)

define internal %Result* @Microsoft__Quantum__Measurement__MResetZ__body(%Qubit* %target) {
entry:
  %result = call %Result* @Microsoft__Quantum__Intrinsic__M__body(%Qubit* %target)
  %0 = call %Result* @__quantum__rt__result_get_one()
  %1 = call i1 @__quantum__rt__result_equal(%Result* %result, %Result* %0)
  br i1 %1, label %then0__1, label %continue__1

then0__1:                                         ; preds = %entry
  call void @__quantum__qis__x__body(%Qubit* %target)
  br label %continue__1

continue__1:                                      ; preds = %then0__1, %entry
  ret %Result* %result
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load { %Array* }*, { %Array* }** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____body({ %Array* }* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load { %Array* }*, { %Array* }** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____adj({ %Array* }* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctl(%Array* %3, { { %Array* }*, { %Array* }* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyOuterTTKAdder____ctladj(%Array* %3, { { %Array* }*, { %Array* }* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load { %Array* }*, { %Array* }** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____body({ %Array* }* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %3 = load { %Array* }*, { %Array* }** %1, align 8
  %4 = load { %Array* }*, { %Array* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____adj({ %Array* }* %3, { %Array* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctl(%Array* %3, { { %Array* }*, { %Array* }* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdderWithoutCarry____ctladj(%Array* %3, { { %Array* }*, { %Array* }* }* %4)
  ret void
}

define internal void @Lifted__PartialApplication__5__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %14, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__5__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %14, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__5__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__5__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %23)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }*, %Qubit* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %4 = load { %Array* }*, { %Array* }** %1, align 8
  %5 = load { %Array* }*, { %Array* }** %2, align 8
  %6 = load %Qubit*, %Qubit** %3, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____body({ %Array* }* %4, { %Array* }* %5, %Qubit* %6)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }*, %Qubit* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 1
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %0, i32 0, i32 2
  %4 = load { %Array* }*, { %Array* }** %1, align 8
  %5 = load { %Array* }*, { %Array* }** %2, align 8
  %6 = load %Qubit*, %Qubit** %3, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____adj({ %Array* }* %4, { %Array* }* %5, %Qubit* %6)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }*, %Qubit* }*, { { %Array* }*, { %Array* }*, %Qubit* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctl(%Array* %3, { { %Array* }*, { %Array* }*, %Qubit* }* %4)
  ret void
}

define internal void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }*, %Qubit* }*, { { %Array* }*, { %Array* }*, %Qubit* }** %2, align 8
  call void @Microsoft__Quantum__Arithmetic____QsRef1__ApplyInnerTTKAdder____ctladj(%Array* %3, { { %Array* }*, { %Array* }*, %Qubit* }* %4)
  ret void
}

define internal void @MemoryManagement__2__RefCount(%Tuple* %capture-tuple, i32 %count-change) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %1 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %0, i32 0, i32 0
  %2 = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_reference_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %capture-tuple, i32 %count-change)
  ret void
}

define internal void @MemoryManagement__2__AliasCount(%Tuple* %capture-tuple, i32 %count-change) {
entry:
  %0 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %1 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %0, i32 0, i32 0
  %2 = load %Callable*, %Callable** %1, align 8
  call void @__quantum__rt__capture_update_alias_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__callable_update_alias_count(%Callable* %2, i32 %count-change)
  call void @__quantum__rt__tuple_update_alias_count(%Tuple* %capture-tuple, i32 %count-change)
  ret void
}

define internal void @Lifted__PartialApplication__6__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %14, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__6__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %14, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__6__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__6__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %23)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__7__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %14, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__7__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %14, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__7__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__7__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %23)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__8__body__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  call void @__quantum__rt__callable_invoke(%Callable* %14, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__8__adj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { { %Array* }*, { %Array* }* }*
  %1 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 0
  %2 = load { %Array* }*, { %Array* }** %1, align 8
  %3 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %0, i32 0, i32 1
  %4 = load { %Array* }*, { %Array* }** %3, align 8
  %5 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %6 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 1
  %7 = load %Qubit*, %Qubit** %6, align 8
  %8 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %9 = bitcast %Tuple* %8 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %10 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 0
  %11 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 1
  %12 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %9, i32 0, i32 2
  store { %Array* }* %2, { %Array* }** %10, align 8
  store { %Array* }* %4, { %Array* }** %11, align 8
  store %Qubit* %7, %Qubit** %12, align 8
  %13 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %5, i32 0, i32 0
  %14 = load %Callable*, %Callable** %13, align 8
  %15 = call %Callable* @__quantum__rt__callable_copy(%Callable* %14, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %15)
  call void @__quantum__rt__callable_invoke(%Callable* %15, %Tuple* %8, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %8, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %15, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %15, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__8__ctl__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

define internal void @Lifted__PartialApplication__8__ctladj__wrapper(%Tuple* %capture-tuple, %Tuple* %arg-tuple, %Tuple* %result-tuple) {
entry:
  %0 = bitcast %Tuple* %arg-tuple to { %Array*, { { %Array* }*, { %Array* }* }* }*
  %1 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 0
  %2 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }* }* }, { %Array*, { { %Array* }*, { %Array* }* }* }* %0, i32 0, i32 1
  %3 = load %Array*, %Array** %1, align 8
  %4 = load { { %Array* }*, { %Array* }* }*, { { %Array* }*, { %Array* }* }** %2, align 8
  %5 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 0
  %6 = load { %Array* }*, { %Array* }** %5, align 8
  %7 = getelementptr inbounds { { %Array* }*, { %Array* }* }, { { %Array* }*, { %Array* }* }* %4, i32 0, i32 1
  %8 = load { %Array* }*, { %Array* }** %7, align 8
  %9 = bitcast %Tuple* %capture-tuple to { %Callable*, %Qubit* }*
  %10 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 1
  %11 = load %Qubit*, %Qubit** %10, align 8
  %12 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 3))
  %13 = bitcast %Tuple* %12 to { { %Array* }*, { %Array* }*, %Qubit* }*
  %14 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 0
  %15 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 1
  %16 = getelementptr inbounds { { %Array* }*, { %Array* }*, %Qubit* }, { { %Array* }*, { %Array* }*, %Qubit* }* %13, i32 0, i32 2
  store { %Array* }* %6, { %Array* }** %14, align 8
  store { %Array* }* %8, { %Array* }** %15, align 8
  store %Qubit* %11, %Qubit** %16, align 8
  %17 = call %Tuple* @__quantum__rt__tuple_create(i64 mul nuw (i64 ptrtoint (i1** getelementptr (i1*, i1** null, i32 1) to i64), i64 2))
  %18 = bitcast %Tuple* %17 to { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }*
  %19 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 0
  %20 = getelementptr inbounds { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }, { %Array*, { { %Array* }*, { %Array* }*, %Qubit* }* }* %18, i32 0, i32 1
  store %Array* %3, %Array** %19, align 8
  store { { %Array* }*, { %Array* }*, %Qubit* }* %13, { { %Array* }*, { %Array* }*, %Qubit* }** %20, align 8
  %21 = getelementptr inbounds { %Callable*, %Qubit* }, { %Callable*, %Qubit* }* %9, i32 0, i32 0
  %22 = load %Callable*, %Callable** %21, align 8
  %23 = call %Callable* @__quantum__rt__callable_copy(%Callable* %22, i1 false)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 1)
  call void @__quantum__rt__callable_make_adjoint(%Callable* %23)
  call void @__quantum__rt__callable_make_controlled(%Callable* %23)
  call void @__quantum__rt__callable_invoke(%Callable* %23, %Tuple* %17, %Tuple* %result-tuple)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %12, i32 -1)
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %17, i32 -1)
  call void @__quantum__rt__capture_update_reference_count(%Callable* %23, i32 -1)
  call void @__quantum__rt__callable_update_reference_count(%Callable* %23, i32 -1)
  ret void
}

declare %Result* @__quantum__rt__result_get_one()

define { i64, i64 }* @Sample__HelloQ__Interop() #1 {
entry:
  %0 = call { i64, i64 }* @Sample__HelloQ__body()
  ret { i64, i64 }* %0
}

define void @Sample__HelloQ() #2 {
entry:
  %0 = call { i64, i64 }* @Sample__HelloQ__body()
  %1 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @22, i32 0, i32 0))
  %2 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 0
  %3 = getelementptr inbounds { i64, i64 }, { i64, i64 }* %0, i32 0, i32 1
  %4 = load i64, i64* %2, align 4
  %5 = load i64, i64* %3, align 4
  %6 = call %String* @__quantum__rt__int_to_string(i64 %4)
  %7 = call %String* @__quantum__rt__string_concatenate(%String* %1, %String* %6)
  call void @__quantum__rt__string_update_reference_count(%String* %1, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %6, i32 -1)
  %8 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @23, i32 0, i32 0))
  %9 = call %String* @__quantum__rt__string_concatenate(%String* %7, %String* %8)
  call void @__quantum__rt__string_update_reference_count(%String* %7, i32 -1)
  %10 = call %String* @__quantum__rt__int_to_string(i64 %5)
  %11 = call %String* @__quantum__rt__string_concatenate(%String* %9, %String* %10)
  call void @__quantum__rt__string_update_reference_count(%String* %9, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %10, i32 -1)
  %12 = call %String* @__quantum__rt__string_create(i8* getelementptr inbounds ([2 x i8], [2 x i8]* @24, i32 0, i32 0))
  %13 = call %String* @__quantum__rt__string_concatenate(%String* %11, %String* %12)
  call void @__quantum__rt__string_update_reference_count(%String* %11, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %12, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %8, i32 -1)
  call void @__quantum__rt__message(%String* %13)
  %14 = bitcast { i64, i64 }* %0 to %Tuple*
  call void @__quantum__rt__tuple_update_reference_count(%Tuple* %14, i32 -1)
  call void @__quantum__rt__string_update_reference_count(%String* %13, i32 -1)
  ret void
}

attributes #0 = { nounwind readnone speculatable willreturn }
attributes #1 = { "InteropFriendly" }
attributes #2 = { "EntryPoint" }
