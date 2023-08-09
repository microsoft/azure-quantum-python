/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { IColumn, IGroup, ThemeProvider } from "@fluentui/react";

import { JobResults } from "../../models/JobResults";
import LineChart from "../d3-visualization-components/LineChart";
import { GetColumns } from "../table/Column";
import { IItem, IState, TableComponent } from "../table/Table";

import "./Diagram.css";

export interface TimeDiagramProps {
  data: string;
}

// Takes the runtime string from the data and formats it with the appropriate symbol for unit of time.
// If no mapping is found, the runtime will be returned with a space between the time and label.
function FormatRuntime(rawRuntime : string) : string{
   /* Define time abbreviation mapping */
   let timeMap : Map<string, string> = new Map([
    ["milliseconds", "ms"],
    ["millisecs", "ms"],
    ["seconds", "s"],
    ["secs", "s"],
    ["minutes", "min"],
    ["mins", "min"],
    ["hours", "h"],
    ["hrs", "h"],
    ["days", "d"],
    ["weeks", "wk"],
    ["wks", "wk"],
    ["months", "mo"],
    ["mos", "mo"],
    ["years", "yr"],
    ["yrs", "yr"],
    ["microseconds", "\u00B5s"],
    ["nanoseconds", "ns"],
    ["picoseconds", "ps"],
    ["microsecs", "\u00B5s"],
    ["nanosecs", "ns"],
    ["picosecs", "ps"]
]);

const runTimeArray = rawRuntime.split(/(\d+)/).filter(Boolean);
const runTimeUnit = timeMap.get(runTimeArray[1]);

var runTimeFormatted = "";
if(runTimeUnit){
  runTimeFormatted = `${runTimeArray[0]} ${runTimeUnit}`;
}
else{
  runTimeFormatted = `${runTimeArray[0]} ${runTimeArray[1]}`;
}

return runTimeFormatted;
}

function TimeDiagram({ data }: TimeDiagramProps) {
  // Parse job results data.
  const jobResults = JSON.parse(data) as JobResults;

  /*------------------------------ Configure canvas sizing ------------------------------  */
  const diagramRef = React.useRef<any>();
  const [width, setWidth] = React.useState(0);
  const [height, setHeight] = React.useState(0);

  const handleWidth = () => {
    const width = diagramRef?.current?.offsetWidth;
    if (width) {
      setWidth(width);
    }
  };
  const handleSize = () => {
    handleWidth();
    const height = diagramRef?.current?.offsetHeight;
    if (height) {
      setHeight(height);
    }
  };
  React.useLayoutEffect(() => {
    handleSize();
    window.addEventListener("resize", handleWidth);
  }, [diagramRef.current]);

  /*------------------------------  Define and parse table and chart data ------------------------------  */
  const algorithmRuntimeFormatted = FormatRuntime(jobResults.physicalCountsFormatted.runtime);
  const tFactoryRuntimeFormatted = FormatRuntime(jobResults.physicalCountsFormatted.tfactoryRuntime);
  const logicalCycleTimeFormatted = FormatRuntime (jobResults.physicalCountsFormatted.logicalCycleTime);

  const numTFactoryInvocations =
    jobResults.physicalCounts.breakdown.numTfactoryRuns;

  const numTfactories = jobResults.physicalCounts.breakdown.numTfactories;
  const numTStatesPerSingleTfactory = jobResults.tfactory.numTstates;
  const numTStatesAllTfactoriesOneInvocation =
    numTStatesPerSingleTfactory * numTfactories;

  const numTStatesPerInvocationString =
    "Output T states of single T factory  (" +
    numTStatesPerSingleTfactory +
    ") * T factories (" +
    numTfactories +
    ") = " +
    numTStatesAllTfactoriesOneInvocation +
    " T states produced by a single invocation of all T factories.";
  const tableItems: IItem[] = [
    {
      name: "Algorithm runtime",
      value: algorithmRuntimeFormatted,
      description: "Total runtime of algorithm.",
    },
    {
      name: "T factory runtime",
      value: tFactoryRuntimeFormatted,
      description: "Runtime of a single T factory.",
    },
    {
      name: "T factory copies",
      value: numTfactories.toLocaleString(),
      description:
        "Number of T factories executed in parallel capable of producing the demanded T states during the algorithm's runtime.",
    },
    {
      name: "T factory invocations",
      value: numTFactoryInvocations.toLocaleString(),
      description: "Number of times all T factories are invoked concurrently.",
    },
    {
      name: "T states per single T factory run",
      value: numTStatesPerSingleTfactory.toLocaleString(),
      description: "Number of T states produced by a single T factory run.",
    },
    {
      name: "T states per invocation",
      value: numTStatesAllTfactoriesOneInvocation.toLocaleString(),
      description: numTStatesPerInvocationString,
    },
    {
      name: "Logical depth",
      value: jobResults.physicalCounts.breakdown.logicalDepth.toLocaleString(),
      description:
        "A single T factory may cause logical depth to increase from algorithmic logical depth if its execution time is slower than the algorithm's.",
    },
    {
      name: "Algorithmic logical depth",
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalDepth.toLocaleString(),
      description: "Number of logical cycles for the algorithm.",
    },
    {
      name: "T gates",
      value: jobResults.logicalCounts.tCount.toLocaleString(),
      description: "Number of T gates in the input quantum program.",
    },
    {
      name: "R gates",
      value: jobResults.logicalCounts.rotationCount.toLocaleString(),
      description: "Number of rotation gates in the input quantum program.",
    },
    {
      name: "Logical depth rotation gates",
      value: jobResults.logicalCounts.rotationDepth.toLocaleString(),
      description: "Depth of rotation gates in the input quantum program.",
    },
    {
      name: "CCZ gates",
      value: jobResults.logicalCounts.cczCount.toLocaleString(),
      description: "Number of CCZ-gates in the input quantum program.",
    },
    {
      name: "CCiX gates",
      value: jobResults.logicalCounts.ccixCount.toLocaleString(),
      description: "Number of CCiX-gates in the input quantum program.",
    },
    {
      name: "Measurement operations",
      value: jobResults.logicalCounts.measurementCount.toLocaleString(),
      description:
        "Number of single qubit measurements in the input quantum program.",
    },
    {
      name: "Logical cycle time",
      value: logicalCycleTimeFormatted,
      description: "Duration of a logical cycle in nanoseconds.",
    },
  ];

  const tableGroups: IGroup[] = [
    {
      key: "1",
      name: "Physical resource estimates",
      startIndex: 0,
      count: 1,
    },
    {
      key: "2",
      name: "T factory parameters",
      startIndex: 1,
      count: 1,
    },
    {
      key: "3",
      name: "Resource estimation breakdown",
      startIndex: 2,
      count: 6,
    },
    {
      key: "4",
      name: "Pre-layout logical resources",
      startIndex: 8,
      count: 6,
    },
    {
      key: "5",
      name: "Logical cycle time",
      startIndex: 14,
      count: 1,
    },
  ];

  /*------------------------------  Create table ------------------------------  */
  const tableProps: IState = {
    items: tableItems,
    groups: tableGroups,
    showItemIndexInView: false,
    isCompactMode: false,
  };
  const columns: IColumn[] = GetColumns();
  const Table = () => (
    <ThemeProvider>
      <TableComponent state={tableProps} columns={columns} />
    </ThemeProvider>
  );

  /*------------------------------  Create chart data dictionary ------------------------------  */
  const chartDictionary: { [key: string]: any } = {
    numberTFactoryInvocations: numTFactoryInvocations.toString(),
    numberTStates: numTStatesAllTfactoriesOneInvocation,
    algorithmRuntime: jobResults.physicalCounts.runtime,
    tFactoryRuntime: jobResults.tfactory.runtime,
    algorithmRuntimeFormatted: algorithmRuntimeFormatted,
    tFactoryRuntimeFormatted: tFactoryRuntimeFormatted,
  };

  return (
    <div className="grid-container">
      <div className="diagram" ref={diagramRef}>
        <LineChart
          chartData={chartDictionary}
          width={width}
          height={height}
        ></LineChart>
      </div>
      <div className="table">
        <Table />
      </div>
    </div>
  );
}

export default TimeDiagram;
