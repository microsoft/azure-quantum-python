import React from "react";
import DonutChart from "../d3-visualization-components/DonutChart";
import "./SpaceChart.css";
export type SpaceChartProps = {
  physicalQubitsAlgorithm: number;
  physicalQubitsTFactory: number;
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
};

function SpaceChart({
  physicalQubitsAlgorithm,
  physicalQubitsTFactory,
  width,
  height,
  innerRadius,
  outerRadius,
}: SpaceChartProps) {
  const chartData = [
    {
      title: "Physical algorithmic qubits",
      value: physicalQubitsAlgorithm,
      legendTitle: "Algorithm qubits",
    },
    {
      title: "Physical T factory qubits",
      value: physicalQubitsTFactory,
      legendTitle: "T factory qubits",
    },
  ];

  return (
    <div>
      <DonutChart
        data={chartData}
        width={width}
        height={height}
        innerRadius={innerRadius}
        outerRadius={outerRadius} />
    </div>
  );
}

export default SpaceChart;
