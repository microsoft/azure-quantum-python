/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { create } from "react-test-renderer";

import LineChart, { LineChartProps } from "../LineChart";

describe("Line chart tests", () => {
  it("Verify Line Chart", () => {
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
      width: 1000,
      height: 1000,
      chartData: chartDictionary,
    };

    const component = create(<LineChart {...lineProps}></LineChart>);
    expect(component.toJSON()).toMatchSnapshot("LineChart");
  });
});
