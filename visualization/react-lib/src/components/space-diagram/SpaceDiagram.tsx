import React from "react";
import DonutChart from "../d3-visualization-components/DonutChart";

/*
export type SpaceDiagramProps = {
  physicalQubitsAlgorithm: number;
  physicalQubitsTFactory: number;
}*/

//function SpaceDiagram({physicalQubitsAlgorithm, physicalQubitsTFactory}: SpaceDiagramProps): JSX.Element{
function SpaceDiagram() {
  const data = [
    { title: "Physical algorithmic qubits", value: 108575, legendTitle: "Algorithm qubits" },
    { title: "Physical T-factory qubits", value: 36890, legendTitle: "T-factory qubits"},
  ];

  return (
    <div>
      <DonutChart
        data={data}
        width={1000}
        height={1000}
        innerRadius={150}
        outerRadius={225}
      />
    </div>
  );
}

export default SpaceDiagram;
