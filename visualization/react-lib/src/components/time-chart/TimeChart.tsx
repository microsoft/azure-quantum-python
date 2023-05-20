import React from "react";
import LineChart from "../d3-visualization-components/LineChart";

export type TimeChartProps = {
  numberTFactoryInvocations: number;
  numberTStates: number;
  algorithmRunTime: string;
  tFactoryRunTime: string;
  width: number;
  height: number;
};

function TimeChart({
  numberTFactoryInvocations,
  numberTStates,
  algorithmRunTime,
  tFactoryRunTime,
  width,
  height,
}: TimeChartProps): JSX.Element {
  const chartLength = width - 100;

  const legendData = [
    {
      title: "Algorithm",
      value: algorithmRunTime,
      legendTitle: "runtime",
    },
    {
      title: "Single T-factory invocation",
      value: tFactoryRunTime,
      legendTitle: "runtime",
    },
  ];
  return (
    <div>
      <LineChart
        legendData={legendData}
        numberTFactoryInvocations={numberTFactoryInvocations}
        numberTStates={numberTStates}
        algorithmRunTime={algorithmRunTime}
        tFactoryRunTime={tFactoryRunTime}
        chartLength={chartLength}
        width={width}
        height={height}
      />
    </div>
  );
}

export default TimeChart;
