import React from "react";
import { SpaceChart } from "./space-chart";
import TableComponent from "./table/Table";
import { TableData } from "./table/Table";
import { JobResults } from "../models/JobResults";
import "./SpaceDiagram.css";

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
      value: jobResults.physicalCounts.physicalQubits,
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
      value: physicalQubitsTFactory,
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
      value: numTFactories,
    },
    {
      id: "6",
      name: "Physical qubits for single T-factory copy",
      type: 1,
      value: numQubitsPerTFactory,
    },
    {
      id: "8",
      name: "Physical algorithmic qubits",
      type: 1,
      value: physicalQubitsAlgorithm,
    },
    {
      id: "9",
      name: "Logical algorithmic qubits",
      type: 1,
      value: jobResults.physicalCounts.breakdown.algorithmicLogicalQubits,
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
      value: jobResults.logicalQubit.physicalQubits,
    },
  ];
  const width2 = width * 2;
  const height2 = height * 2;
  return (
    <div className="grid-container">
      <div>
        <SpaceChart
          physicalQubitsAlgorithm={physicalQubitsAlgorithm}
          physicalQubitsTFactory={physicalQubitsTFactory}
          width={width}
          height={height}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
        />
      </div>
      <div className="table-element">
        <TableComponent nodes={nodes} width={width} height={height} />
      </div>
    </div>
  );
}

export default SpaceDiagram;
