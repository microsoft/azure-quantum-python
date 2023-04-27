import React from "react";
import DonutChart from "../d3-visualization-components/DonutChart";
import "./SpaceDiagram.css";
/*
export type SpaceDiagramProps = {
  physicalQubitsAlgorithm: number;
  physicalQubitsTFactory: number;
}*/

//function SpaceDiagram({physicalQubitsAlgorithm, physicalQubitsTFactory}: SpaceDiagramProps): JSX.Element{
function SpaceDiagram() {
  const data = [
    { title: "Physical algorithmic qubits", value: 100 },
    { title: "Physical T-Factory qubits", value: 25 },
  ];

  return (
    <div>
      <div className="space-diagram"> Space diagram </div>
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
