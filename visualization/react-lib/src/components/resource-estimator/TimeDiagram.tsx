import React from "react";
import { TableComponent, IItem, IState } from "../table/Table";
import { ThemeProvider, IGroup, IColumn } from "@fluentui/react";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";
import { TimeChart } from "../time-chart";
import { getTheme, mergeStyleSets } from "@fluentui/react/lib/Styling";
import { TooltipHost, ITooltipHostStyles } from '@fluentui/react/lib/Tooltip';
import { Icon } from '@fluentui/react/lib/Icon';

interface TimeDiagramProps {
  data: string;
}

const classNames = mergeStyleSets({
  cellText: {
    overflow: "hidden",
    textOverflow: "ellipsis",
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
      fill: getTheme().semanticColors.infoIcon,
  },
});

function TimeDiagram({ data }: TimeDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

  const diagramRef = React.useRef<any>();

  const [width, setWidth] = React.useState(0);
  const [height, setHeight] = React.useState(0);

  const handleWidth = () => {
    const width = diagramRef?.current?.offsetWidth;
    if (width) {
      setWidth(width);
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

  const algorithmRuntimeFormatted = jobResults.physicalCountsFormatted.runtime;
  const tFactoryRuntimeFormatted =
    jobResults.physicalCountsFormatted.tfactoryRuntime;
  const numTFactoryInvocations =
    jobResults.physicalCounts.breakdown.numTfactoryRuns;

  const tableItems: IItem[] = [
    {
      name: "Algorithm runtime",
      value: algorithmRuntimeFormatted,
      description: "Total runtime of algorithm."
    },
    {
      name: "T-factory runtime",
      value: tFactoryRuntimeFormatted,
      description: "Runtime of a single T factory."
    },
    {
      name: "Number of T-factory invocations",
      value: numTFactoryInvocations.toString(),
      description: "Number of times all T factories are invoked.",
    },
    {
      name: "Number of T states per invocation",
      value: jobResults.logicalCounts.tCount.toString(),
      description:
        "Number of output T states produced in a single run of T factory.",
    },
    {
      name: "Logical depth",
      value: jobResults.physicalCounts.breakdown.logicalDepth.toString(),
      description:
        "A single T factory may cause logical depth to increase from algorithmic logical depth if its execution time is slower than the algorithm's.",
    },
    {
      name: "Algorithmic logical depth",
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalDepth.toString(),
      description: "Number of logical cycles for the algorithm.",
    },
    {
      name: "T-gates",
      value: jobResults.logicalCounts.tCount.toString(),
      description: "Number of T gates in the input quantum program.",
    },
    {
      name: "R-gates",
      value: jobResults.logicalCounts.rotationCount.toString(),
      description: "Number of rotation gates in the input quantum program.",
    },
    {
      name: "Logical depth rotation gates",
      value: jobResults.logicalCounts.rotationDepth.toString(),
      description: "Depth of rotation gates in the input quantum program.",
    },
    {
      name: "CCZ gates",
      value: jobResults.logicalCounts.cczCount.toString(),
      description: "Number of CCZ-gates in the input quantum program.",
    },
    {
      name: "CCiX gates",
      value: jobResults.logicalCounts.ccixCount.toString(),
      description: "Number of CCiX-gates in the input quantum program.",
    },
    {
      name: "Measurement operations",
      value: jobResults.logicalCounts.measurementCount.toString(),
      description:
        "Number of single qubit measurements in the input quantum program.",
    },
    {
      name: "Logical cycle time",
      value: jobResults.physicalCountsFormatted.logicalCycleTime,
      description: "Duration of a logical cycle in nanoseconds.",
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
      name: 'T-factory parameters',
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
      name: 'Pre-layout logical resources',
      startIndex: 6,
      count: 6,
    },
    {
      key: "5",
      name: 'Logical cycle time',
      startIndex: 12,
      count: 1,
    }
  ];

  const tableProps: IState =
  {
    items: tableItems,
    groups: tableGroups,
    showItemIndexInView: false,
    isCompactMode: false,
  };

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
                  <Icon iconName="InfoSolid" className={classNames.infoIcon}/>
                </TooltipHost>
              : <></>
            }
          </div>
        )
      },
      minWidth: 220,
      flexGrow: 3,
    },
    {
      key: 'value',
      name: 'Value',
      onRender: (item: IItem) => {
        return (
          <div className={classNames.cellText} data-is-focusable={true}>
            {item.value}
          </div>
        )
      },
      minWidth: 50,
      flexGrow: 1,
    },
  ];

  const chartDictionary: { [key: string]: any } = {
    numberTFactoryInvocations: numTFactoryInvocations.toString(),
    numberTStates: jobResults.logicalCounts.tCount.toString(),
    algorithmRuntime: jobResults.physicalCounts.runtime,
    tFactoryRuntime: jobResults.tfactory.runtime,
    algorithmRuntimeFormatted: algorithmRuntimeFormatted,
    tFactoryRuntimeFormatted: tFactoryRuntimeFormatted,
  };

  const Table = () => <ThemeProvider><TableComponent state={tableProps} columns={columns} /></ThemeProvider>;

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
        <Table />
      </div>
    </div>
  );
}

export default TimeDiagram;

