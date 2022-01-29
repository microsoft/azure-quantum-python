namespace union {

    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;

    @EntryPoint()
    operation HelloQ() : (Int, Int) {
        Message("Hello quantum world!");

        use q_a = Qubit[3];
        use q_b = Qubit[3];

        let a = LittleEndian(q_a);
        let b = LittleEndian(q_b);

        
        Message("Initial state");
        //DumpMachine();

        IncrementByInteger(1, a);
        IncrementByInteger(4, b);

        Message("State a:");
        DumpRegister((), q_a);

        Message("State b:");
        DumpRegister((), q_b);

        // Adjoint QFT(LittleEndianAsBigEndian(a));
        // Adjoint QFT(LittleEndianAsBigEndian(b));

        Message("a phase:");
        DumpRegister((), q_a);
        Message("b phase:");
        DumpRegister((), q_b);
        
        AddI(a, b);

        Message("After AddI");
        Message("a phase:");
        DumpRegister((), q_a);
        Message("b phase:");
        DumpRegister((), q_b);
        
        Message("After QFT");
        // QFT(LittleEndianAsBigEndian(a));
        // QFT(LittleEndianAsBigEndian(b));

        Message("a result:");
        DumpRegister((), q_a);
        Message("b result:");
        DumpRegister((), q_b);

        return (MeasureInteger(a), MeasureInteger(b));
    }
}

