import React from "react";
import TableComponent from "../table/Table";
import { TableData } from "../table/Table";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";
import { TimeChart } from "../time-chart";

interface TimeDiagramProps {
  width: number;
  height: number;
  data: string;
}

function TimeDiagram({ width, height, data }: TimeDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

  const algorithmRuntime = jobResults.physicalCountsFormatted.runtime;
  const tFactoryRuntime = jobResults.physicalCountsFormatted.tfactoryRuntime;
  const numTFactoryInvocations =
    jobResults.physicalCounts.breakdown.numTfactoryRuns;

  // TO DO: get names and descriptions from data.
  const nodes: TableData[] = [
    {
      id: "0",
      name: "Physical resource estimates",
      type: 0,
    },
    {
      id: "1",
      name: "Runtime",
      type: 1,
      value: algorithmRuntime,
      description: "Total runtime of algorithm",
    },
    {
      id: "2",
      name: "T-factory parameters",
      type: 0,
    },
    {
      id: "3",
      name: "Runtime",
      type: 1,
      value: tFactoryRuntime,
      description: "Single T-factory invocation runtime",
    },
    {
      id: "4",
      name: "Resource estimation breakdown",
      type: 0,
    },
    {
      id: "5",
      name: "Number of T-factory invocations",
      type: 1,
      value: numTFactoryInvocations.toString(),
    },
    {
      id: "6",
      name: "Logical depth",
      type: 1,
      value: jobResults.physicalCounts.breakdown.logicalDepth.toString(),
    },
    {
      id: "7",
      name: "Algorithmic logical depth",
      type: 1,
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalDepth.toString(),
    },
    {
      id: "8",
      name: "Pre-layout logical resources",
      type: 0,
    },
    {
      id: "9",
      name: "T-gates",
      type: 1,
      value: jobResults.logicalCounts.tCount.toString(),
    },
    {
      id: "10",
      name: "R-gates",
      type: 1,
      value: jobResults.logicalCounts.rotationCount.toString(),
    },
    {
      id: "11",
      name: "Logical depth rotation gates",
      type: 1,
      value: jobResults.logicalCounts.rotationDepth.toString(),
    },

    {
      id: "12",
      name: "CCZ gates",
      type: 1,
      value: jobResults.logicalCounts.cczCount.toString(),
    },
    {
      id: "13",
      name: "CCIX gates",
      type: 1,
      value: jobResults.logicalCounts.ccixCount.toString(),
    },
    {
      id: "14",
      name: "Measurement operations",
      type: 1,
      value: jobResults.logicalCounts.measurementCount.toString(),
    },
    {
      id: "15",
      name: "Logical qubit parameters",
      type: 0,
    },
    {
      id: "16",
      name: "Logical cycle time",
      type: 1,
      value: jobResults.physicalCountsFormatted.logicalCycleTime,
    },
  ];

  return (
    <div className="grid-container">
      <div className="diagram">
        <TimeChart
          numberTFactories={numTFactoryInvocations.toString()}
          algorithmRuntime={algorithmRuntime}
          tFactoryRunTime={tFactoryRuntime}
          width={width}
          height={height}
        ></TimeChart>
      </div>

    </div>
  );
}

export default TimeDiagram;



