/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { IColumn, IGroup, ThemeProvider } from "@fluentui/react";

import { JobResults } from "../../models/JobResults";
import DonutChart from "../d3-visualization-components/DonutChart";
import { GetColumns } from "../table/Column";
import { IItem, IState, TableComponent } from "../table/Table";

import "./Diagram.css";

export interface SpaceDiagramProps {
  data: string;
}

function SpaceDiagram({ data }: SpaceDiagramProps) {
  // Parse job results data.
  const jobResults = JSON.parse(data) as JobResults;

  /*------------------------------ Configure canvas sizing ------------------------------  */
  const diagramRef = React.useRef<any>();
  const [width, setWidth] = React.useState(0);
  const [height, setHeight] = React.useState(0);
  const [innerRadius, setInnerRadius] = React.useState(0);
  const [outerRadius, setOuterRadius] = React.useState(0);

  const handleWidth = () => {
    const width = diagramRef?.current?.offsetWidth;
    if (width) {
      setWidth(width);
      if (height) {
        const outerRadius = 0.3 * Math.min(height * 0.7, width);
        const innerRadius = 0.75 * outerRadius;
        setOuterRadius(outerRadius);
        setInnerRadius(innerRadius);
      }
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
  const physicalQubitsAlgorithm =
    jobResults.physicalCounts.breakdown.physicalQubitsForAlgorithm;
  const physicalQubitsTFactory =
    jobResults.physicalCounts.breakdown.physicalQubitsForTfactories;

  const numTFactories = jobResults.physicalCounts.breakdown.numTfactories;
  const numQubitsPerTFactory = Math.round(
    physicalQubitsTFactory / numTFactories,
  );

  const chartData = [
    {
      title: "Physical",
      value: physicalQubitsAlgorithm,
      legendTitle: "Algorithm qubits",
    },
    {
      title: "Physical",
      value: physicalQubitsTFactory,
      legendTitle: "T factory qubits",
    },
  ];

  const numTFactoryQubitsString =
    "Physical qubits per single T factory (" +
    numQubitsPerTFactory.toLocaleString() +
    ") * T factory copies (" +
    numTFactories.toLocaleString() +
    ") = " +
    physicalQubitsTFactory.toLocaleString() +
    " Total physical qubits required for all T factories.";

  const tableItems: IItem[] = [
    {
      name: "Total physical qubits",
      value: jobResults.physicalCounts.physicalQubits.toLocaleString(),
      description:
        "Total physical qubits required for algorithm and T factories.",
    },
    {
      name: "Physical T factory qubits",
      value: physicalQubitsTFactory.toLocaleString(),
      description:
        "Total number of physical qubits required for the T factories.",
    },
    {
      name: "T factory copies",
      value: numTFactories.toLocaleString(),
      description:
        "Number of T factories executed in parallel capable of producing the demanded T states during the algorithm's runtime.",
    },
    {
      name: "Physical qubits per T factory",
      value: numQubitsPerTFactory.toLocaleString(),
      description: numTFactoryQubitsString,
    },
    {
      name: "Physical algorithmic qubits",
      value: physicalQubitsAlgorithm.toLocaleString(),
      description: "Number of logical qubits for the algorithm after layout.",
    },
    {
      name: "Logical algorithmic qubits",
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalQubits.toLocaleString(),
      description: "Number of logical qubits for the algorithm after layout.",
    },
    {
      name: "Physical qubits",
      value: jobResults.logicalQubit.physicalQubits.toLocaleString(),
      description: "Number of physical qubits per logical qubit.",
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
      count: 4,
    },
    {
      key: "4",
      name: "Logical qubit parameters",
      startIndex: 6,
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

  return (
    <div className="grid-container">
      <div className="diagram" ref={diagramRef}>
        <DonutChart
          data={chartData}
          width={width}
          height={height}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
        />
      </div>
      <div className="table">
        <Table />
      </div>
    </div>
  );
}

export default SpaceDiagram;
