import React from "react";
import DonutChart, { Data, DonutChartProps } from "../DonutChart";
import { create } from "react-test-renderer";
// Consider using react-faux-dom or jsdom to test d3 //
describe("Donut chart tests", () => {
  it("Verify Donut Chart", () => {
    const testData: Data[] = [
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
      outerRadius: 200,
      translationValX: 2,
      translationValY: 1,
    };

    const component = create(<DonutChart {...donutProps}></DonutChart>);
    const componentInstance = component.root;
    expect(component.toJSON()).toMatchSnapshot("DonutChart");
  });
});
