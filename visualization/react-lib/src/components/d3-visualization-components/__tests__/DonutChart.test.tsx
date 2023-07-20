import React from "react";
import DonutChart, { DonutChartProps } from "../DonutChart";
import { LegendData } from "../D3HelperFunctions";
import { create } from "react-test-renderer";
// Consider using react-faux-dom or jsdom to test d3 //
describe("Donut chart tests", () => {
  it("Verify Donut Chart", () => {
    const testData: LegendData[] = [
      {
        legendTitle: "Logical qubits",
        title: "Logical qubits",
        value: 50,
      },
      {
        legendTitle: "Physical qubits",
        title: "Physical qubits",
        value: 200,
      },
    ];

    const donutProps: DonutChartProps = {
      data: testData,
      width: 1000,
      height: 1000,
      innerRadius: 100,
      outerRadius: 200
    };

    const component = create(<DonutChart {...donutProps}></DonutChart>);
    const componentInstance = component.root;
    expect(component.toJSON()).toMatchSnapshot("DonutChart");
  });
});
