import React from "react";
import { SpaceChart } from "../space-chart";
import { TableComponent, IItem, IState } from "../table/Table";
import { ThemeProvider, IGroup, IColumn, IDetailsColumnStyles } from "@fluentui/react";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";
import { getTheme, mergeStyleSets } from "@fluentui/react/lib/Styling";
import { TooltipHost, TooltipOverflowMode } from '@fluentui/react/lib/Tooltip';
import { Icon } from '@fluentui/react/lib/Icon';

const classNames = mergeStyleSets({
  cellText: {
    overflow: "hidden",
    textOverflow: "ellipsis",
    color: "#343434"
  },
  tooltipHost: {
    marginLeft: "8px",
    cursor: "default",
  },
  infoIcon: {
    width: "12px",
    height: "12px",
    display: "inline-block",
    verticalAlign: "-0.1rem",
    color: "#343434"
  },
});

interface SpaceDiagramProps {
  data: string;
}

function SpaceDiagram({
  data,
}: SpaceDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

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
  }
  const handleSize = () => {
    handleWidth();
    const height = diagramRef?.current?.offsetHeight;
    if (height) {
      setHeight(height);
    }
  }
  React.useLayoutEffect(() => {
    handleSize();
    window.addEventListener("resize", handleWidth);
  }, [diagramRef.current]);

  const physicalQubitsAlgorithm =
    jobResults.physicalCounts.breakdown.physicalQubitsForAlgorithm;
  const physicalQubitsTFactory =
    jobResults.physicalCounts.breakdown.physicalQubitsForTfactories;

  const numTFactories = jobResults.physicalCounts.breakdown.numTfactories;
  const numQubitsPerTFactory = Math.round(
    physicalQubitsTFactory / numTFactories
  );

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
      description: "Number of physical qubits for the T factories.",
    },
    {
      name: "Number of T factory copies",
      value: numTFactories.toLocaleString(),
      description: "Number of T factories capable of producing the demanded T states during the algorithm's runtime."
    },
    {
      name: "Physical qubits for single T factory",
      value: numQubitsPerTFactory.toLocaleString(),
      description: ""
    },
    {
      name: "Physical algorithmic qubits",
      value: physicalQubitsAlgorithm.toLocaleString(),
      description: "Number of logical qubits for the algorithm after layout."
    },
    {
      name: "Logical algorithmic qubits",
      value: jobResults.physicalCounts.breakdown.algorithmicLogicalQubits.toLocaleString(),
      description: "Number of logical qubits for the algorithm after layout."
    },
    {
      name: "Physical qubits",
      value: jobResults.logicalQubit.physicalQubits.toLocaleString(),
      description: "Number of physical qubits per logical qubit."
    }
  ];

  const tableGroups: IGroup[] = [
    {
      key: "1",
      name: 'Physical resource estimates',
      startIndex: 0,
      count: 1
    },
    {
      key: "2",
      name: 'T factory parameters',
      startIndex: 1,
      count: 1
    },
    {
      key: "3",
      name: 'Resource estimation breakdown',
      startIndex: 2,
      count: 4,
    },
    {
      key: "4",
      name: 'Logical qubit parameters',
      startIndex: 6,
      count: 1
    }
  ];

  const tableProps: IState =
  {
    items: tableItems,
    groups: tableGroups,
    showItemIndexInView: false,
    isCompactMode: false,
  };


  const headerStyle: Partial<IDetailsColumnStyles> = {
    cellTooltip: {
      color: getTheme().palette.orange,
    }
  }

  const columns: IColumn[] = [
    {
      key: 'name',
      name: 'Name',
      onRender: (item: IItem) => {
        return (
          <div className={classNames.cellText} data-is-focusable={true}>
            {item.name}
            {
              item.description
                ? <TooltipHost hostClassName={classNames.tooltipHost} content={item.description}>
                  <Icon iconName="Info" className={classNames.infoIcon} />
                </TooltipHost>
                : <></>
            }
          </div>
        )
      },
      minWidth: 220,
      flexGrow: 3,
      styles: headerStyle,
    },
    {
      key: 'value',
      name: 'Value',
      onRender: (item: IItem) => {
        return (

          <div className={classNames.cellText} data-is-focusable={true}>
            <TooltipHost hostClassName={classNames.tooltipHost} content={item.value} overflowMode={TooltipOverflowMode.Parent}>
              {item.value}
            </TooltipHost>
          </div>
        )
      },
      minWidth: 50,
      flexGrow: 1,
    },
  ];

  const Table = () => <ThemeProvider><TableComponent state={tableProps} columns={columns} /></ThemeProvider>;

  return (
    <div className="grid-container">
      <div className="diagram" ref={diagramRef}>
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
        <Table />
      </div>
    </div>
  );
}

export default SpaceDiagram;
