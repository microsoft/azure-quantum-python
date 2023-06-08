import LineChart from "../d3-visualization-components/LineChart";

export type TimeChartProps = {
  chartData: { [key: string]: any };
  width: number;
  height: number;
};

function TimeChart({ chartData, width, height }: TimeChartProps): JSX.Element {
  const legendData = [
    {
      title: "Algorithm",
      value: chartData["algorithmRuntimeFormatted"].value,
      legendTitle: "runtime",
    },
    {
      title: "Single T-factory invocation",
      value: chartData["tFactoryRuntimeFormatted"].value,
      legendTitle: "runtime",
    },
  ];

  return (
    <div>
      <LineChart
        legendData={legendData}
        chartData={chartData}
        width={width}
        height={height}
      />
    </div>
  );
}

export default TimeChart;
