import React from "react";
import LineChart from "../d3-visualization-components/LineChart";

export type TimeChartProps = {
  numberTFactories: number;
  tFactoryRunTime: string;
  algorithmRuntime: string;
  width: number;
  height: number;
};

function TimeChart({
  numberTFactories,
  tFactoryRunTime,
  algorithmRuntime,
  width,
  height,
}: TimeChartProps): JSX.Element {
  const chartData = [
    {
      title: "T-states produced after each invocations runtime",
      value: numberTFactories,
      legendTitle: "T-states produced after each invocations runtime",
    },
    {
      title: "runtime",
      value: algorithmRuntime,
      legendTitle: "Algorithm",
    },
    {
      title: "runtime",
      value: tFactoryRunTime,
      legendTitle: "Single T-factory invocation",
    },
  ];

  const chartLength = width - 10;

  return (
    <div>
      <LineChart
        data={chartData}
        chartLength={chartLength}
        width={width}
        height={height}
      />
    </div>
  );
}

export default TimeChart;
