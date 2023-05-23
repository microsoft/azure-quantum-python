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

  const algorithmRuntimeFormatted = jobResults.physicalCountsFormatted.runtime;
  const tFactoryRuntimeFormatted =
    jobResults.physicalCountsFormatted.tfactoryRuntime;
  const numTFactoryInvocations =
    jobResults.physicalCounts.breakdown.numTfactoryRuns;
  const numTStates = jobResults.tfactory.numTstates;

  // TO DO: get names and descriptions from data.
  const tableDictionary = {
    "Physical resource estimates": {
      type: 0,
    },
    "Algorithm runtime": {
      type: 1,
      value: algorithmRuntimeFormatted,
      description: "Total runtime of algorithm",
    },
    "T-factory parameters": {
      type: 0,
    },
    "T-factory runtime": {
      type: 1,
      value: tFactoryRuntimeFormatted,
      description: "Single T-factory invocation runtime",
    },
    "Resource estimation breakdown": {
      type: 0,
    },
    "Number of T-factory invocations": {
      type: 1,
      value: numTFactoryInvocations.toString(),
    },
    "Logical depth": {
      type: 1,
      value: jobResults.physicalCounts.breakdown.logicalDepth.toString(),
    },
    "Algorithmic logical depth": {
      type: 1,
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalDepth.toString(),
    },
    "Pre-layout logical resources": {
      type: 0,
    },
    "T-gates": {
      type: 1,
      value: jobResults.logicalCounts.tCount.toString(),
    },
    "R-gates": {
      type: 1,
      value: jobResults.logicalCounts.rotationCount.toString(),
    },
    "Logical depth rotation gates": {
      type: 1,
      value: jobResults.logicalCounts.rotationDepth.toString(),
    },
    "CCZ gates": {
      type: 1,
      value: jobResults.logicalCounts.cczCount.toString(),
    },
    "CCIX gates": {
      type: 1,
      value: jobResults.logicalCounts.ccixCount.toString(),
    },
    "Measurement operations": {
      type: 1,
      value: jobResults.logicalCounts.measurementCount.toString(),
    },
    "Logical qubit parameters": {
      type: 0,
    },
    "Logical cycle time": {
      type: 1,
      value: jobResults.physicalCountsFormatted.logicalCycleTime,
    },
  };

  const chartDictionary: { [key: string]: any } = {
    numberTFactoryInvocations: numTFactoryInvocations.toString(),
    numberTStates: jobResults.logicalCounts.tCount.toString(),
    algorithmRuntime: jobResults.physicalCounts.runtime,
    tFactoryRuntime: jobResults.tfactory.runtime,
    algorithmRuntimeFormatted: algorithmRuntimeFormatted,
    tFactoryRuntimeFormatted: tFactoryRuntimeFormatted,
    chartLength: width - 100,
  };

  return (
    <div className="grid-container">
      <div className="diagram">
        <TimeChart
          chartData={chartDictionary}
          width={width}
          height={height}
        ></TimeChart>
      </div>
    </div>
  );
}

export default TimeDiagram;
