open Microsoft.Quantum.Arithmetic;

@EntryPoint()
operation EstimateMultiplier(bitwidth : Int) : Unit {
    use xs = Qubit[bitwidth];
    use ys = Qubit[bitwidth];
    use zs = Qubit[2 * bitwidth];

    MultiplyI(LittleEndian(xs), LittleEndian(ys), LittleEndian(zs));
}
