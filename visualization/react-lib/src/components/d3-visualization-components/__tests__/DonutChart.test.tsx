/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import React from "react";
import { create } from "react-test-renderer";

import { LegendData } from "../D3HelperFunctions";
import DonutChart, { DonutChartProps } from "../DonutChart";

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
      outerRadius: 200,
    };

    const component = create(<DonutChart {...donutProps}></DonutChart>);
    expect(component.toJSON()).toMatchSnapshot("DonutChart");
  });
});
