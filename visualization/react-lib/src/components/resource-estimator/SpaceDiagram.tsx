import React from "react";
import { SpaceChart } from "../space-chart";
import TableComponent from "../table/Table";
import { TableData } from "../table/Table";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";

interface SpaceDiagramProps {
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
  data: string;
}

function SpaceDiagram({
  width,
  height,
  innerRadius = 150,
  outerRadius = 225,
  data,
}: SpaceDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

  const physicalQubitsAlgorithm =
    jobResults.physicalCounts.breakdown.physicalQubitsForAlgorithm;
  const physicalQubitsTFactory =
    jobResults.physicalCounts.breakdown.physicalQubitsForTfactories;

  const numTFactories = jobResults.physicalCounts.breakdown.numTfactories;
  const numQubitsPerTFactory = Math.round(
    physicalQubitsTFactory / numTFactories
  );

  // TO DO: make name and description come from job results.
  const nodes: TableData[] = [
    {
      id: "0",
      name: "Physical resource estimates",
      type: 0,
    },
    {
      id: "1",
      name: "Total physical qubits",
      type: 1,
      value: jobResults.physicalCounts.physicalQubits.toString(),
      description:
        "Total physical qubits required for algorithm and t-factories.",
    },
    {
      id: "2",
      name: "T-factory parameters",
      type: 0,
    },
    {
      id: "3",
      name: "Total T-factory physical qubits",
      type: 1,
      value: physicalQubitsTFactory.toString(),
      description: "Total physical qubits required for t-factories.",
    },
    {
      id: "4",
      name: "Resource estimation breakdown",
      type: 0,
    },
    {
      id: "5",
      name: "Number of T-factory copies",
      type: 1,
      value: numTFactories.toString(),
    },
    {
      id: "6",
      name: "Physical qubits for single T-factory copy",
      type: 1,
      value: numQubitsPerTFactory.toString(),
    },
    {
      id: "8",
      name: "Physical algorithmic qubits",
      type: 1,
      value: physicalQubitsAlgorithm.toString(),
      description: "Total physical qubits required for algorithm execution.",
    },
    {
      id: "9",
      name: "Logical algorithmic qubits",
      type: 1,
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalQubits.toString(),
      description:
        "Total logical qubits made up of algorithmic physical qubits required for algorithm.",
    },
    {
      id: "10",
      name: "Logical qubit parameters",
      type: 0,
    },
    {
      id: "11",
      name: "Physical qubits",
      type: 1,
      value: jobResults.logicalQubit.physicalQubits.toString(),
      description:
        "Number of physical qubits which make up one logical algorithmic qubit.",
    },
  ];

  return (
    <div className="grid-container">
      <div className="diagram">
        <SpaceChart
          physicalQubitsAlgorithm={physicalQubitsAlgorithm}
          physicalQubitsTFactory={physicalQubitsTFactory}
          width={width}
          height={height}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
        />
      </div>
      <div className="table">
        <TableComponent nodes={nodes} width={width} height={height} />
      </div>
    </div>
  );
}

export default SpaceDiagram;
