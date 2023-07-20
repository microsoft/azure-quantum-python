import React from "react";
import LineChart, { LineChartProps } from "../LineChart";
import { LegendData } from "../D3HelperFunctions";
import { create } from "react-test-renderer";

// Consider using react-faux-dom or jsdom to test d3 //
describe("Line chart tests", () => {
  it("Verify Line Chart", () => {
    const testLegendData: LegendData[] = [
      {
        title: "Algorithm",
        value: 10,
        legendTitle: "runtime",
      },
      {
        title: "Single T-factory invocation",
        value: 1,
        legendTitle: "runtime",
      },
    ];

    const chartDictionary: { [key: string]: any } = {
      numberTFactoryInvocations: "100",
      numberTStates: "5",
      algorithmRuntime: "10 ms",
      tFactoryRuntime: "1 ms",
      algorithmRuntimeFormatted: "10 ms",
      tFactoryRuntimeFormatted: "1 ms",
      chartLength: 800,
    };

    const lineProps: LineChartProps = {
      legendData: testLegendData,
      width: 1000,
      height: 1000,
      chartData: chartDictionary,
    };

    const component = create(<LineChart {...lineProps}></LineChart>);
    const componentInstance = component.root;
    expect(component.toJSON()).toMatchSnapshot("LineChart");
  });
});
