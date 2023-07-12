import React from "react";
import TableComponent from "../table/Table";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";
import { TimeChart } from "../time-chart";
import { TableData } from "../table/Table";

interface TimeDiagramProps {
  data: string;
}

function TimeDiagram({ data }: TimeDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

  const diagramRef = React.useRef<any>();

  const [width, setWidth] = React.useState(0);
  const [height, setHeight] = React.useState(0);

  const handleSize = () => {
    const height = diagramRef?.current?.offsetHeight;
    const width = diagramRef?.current?.offsetWidth;
    if (height) {
      setHeight(height);
    }
    if (width) {
      setWidth(width * 0.8);
    }
  }
  React.useLayoutEffect(() => {
    handleSize();
    window.addEventListener("resize", handleSize);
  }, [diagramRef]);

  const algorithmRuntimeFormatted = jobResults.physicalCountsFormatted.runtime;
  const tFactoryRuntimeFormatted =
    jobResults.physicalCountsFormatted.tfactoryRuntime;
  const numTFactoryInvocations =
    jobResults.physicalCounts.breakdown.numTfactoryRuns;

  // TO DO: get names and descriptions from data.
  const tableDictionary: {
    [name: string]: {
      type: number;
      description?: string;
      value?: string;
    };
  } = {
    "Physical resource estimates": {
      type: 0,
    },
    "Algorithm runtime": {
      type: 1,
      value: algorithmRuntimeFormatted,
      description: "Total runtime of algorithm.",
    },
    "T-factory parameters": {
      type: 0,
    },
    "T-factory runtime": {
      type: 1,
      value: tFactoryRuntimeFormatted,
      description: "Runtime of a single T factory.",
    },
    "Resource estimation breakdown": {
      type: 0,
    },
    "Number of T-factory invocations": {
      type: 1,
      value: numTFactoryInvocations.toString(),
      description: "Number of times all T factories are invoked.",
    },
    "Number of T states per invocation": {
      type: 1,
      value: jobResults.logicalCounts.tCount.toString(),
      description:
        "Number of output T states produced in a single run of T factory.",
    },
    "Logical depth": {
      type: 1,
      value: jobResults.physicalCounts.breakdown.logicalDepth.toString(),
      description:
        "A single T factory may cause logical depth to increase from algorithmic logical depth if its execution time is slower than the algorithm's.",
    },
    "Algorithmic logical depth": {
      type: 1,
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalDepth.toString(),
      description: "Number of logical cycles for the algorithm.",
    },
    "Pre-layout logical resources": {
      type: 0,
    },
    "T-gates": {
      type: 1,
      value: jobResults.logicalCounts.tCount.toString(),
      description: "Number of T gates in the input quantum program.",
    },
    "R-gates": {
      type: 1,
      value: jobResults.logicalCounts.rotationCount.toString(),
      description: "Number of rotation gates in the input quantum program.",
    },
    "Logical depth rotation gates": {
      type: 1,
      value: jobResults.logicalCounts.rotationDepth.toString(),
      description: "Depth of rotation gates in the input quantum program.",
    },
    "CCZ gates": {
      type: 1,
      value: jobResults.logicalCounts.cczCount.toString(),
      description: "Number of CCZ-gates in the input quantum program.",
    },
    "CCiX gates": {
      type: 1,
      value: jobResults.logicalCounts.ccixCount.toString(),
      description: "Number of CCiX-gates in the input quantum program.",
    },
    "Measurement operations": {
      type: 1,
      value: jobResults.logicalCounts.measurementCount.toString(),
      description:
        "Number of single qubit measurements in the input quantum program.",
    },
    "Logical qubit parameters": {
      type: 0,
    },
    "Logical cycle time": {
      type: 1,
      value: jobResults.physicalCountsFormatted.logicalCycleTime,
      description: "Duration of a logical cycle in nanoseconds.",
    },
  };

  const chartDictionary: { [key: string]: any } = {
    numberTFactoryInvocations: numTFactoryInvocations.toString(),
    numberTStates: jobResults.logicalCounts.tCount.toString(),
    algorithmRuntime: jobResults.physicalCounts.runtime,
    tFactoryRuntime: jobResults.tfactory.runtime,
    algorithmRuntimeFormatted: algorithmRuntimeFormatted,
    tFactoryRuntimeFormatted: tFactoryRuntimeFormatted,
    chartLength: width - 200,
  };

  const tableDataArray: TableData[] = Object.keys(tableDictionary).map(
    (key, i) => {
      return {
        id: i.toString(),
        name: key,
        type: tableDictionary[key].type,
        value: tableDictionary[key].value,
        description: tableDictionary[key].description,
      };
    }
  );

  return (
    <div className="grid-container">
      <div className="diagram" ref={diagramRef}>
        <TimeChart
          chartData={chartDictionary}
          width={width}
          height={height}
        ></TimeChart>
      </div>
      <div className="table">
        <TableComponent nodes={tableDataArray} width={width} height={height} />
      </div>
    </div>
  );
}

export default TimeDiagram;
