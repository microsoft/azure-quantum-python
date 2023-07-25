/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import * as React from "react";
import * as d3 from "d3";
import * as d3Format from "d3-format";
import { PieArcDatum } from "d3-shape";

import * as d3Helper from "./D3HelperFunctions";
import { TextStyle } from "./D3HelperFunctions";

export type DonutChartProps = {
  data: d3Helper.LegendData[];
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
};

/* Define styles */
const titleStyle: TextStyle = {
  fontFamily: "Segoe UI",
  fontStyle: "normal",
  fontWeight: "600",
  fontSize: "35",
  lineHeight: "47",
  display: "flex",
  alignItems: "center",
  textAlign: "center",
  color: "#201f1e",
  textAnchor: "middle",
};

const donutMiddleTitleStyle: TextStyle = {
  fontSize: "18",
  color: "#323130",
  fontWeight: "400",
  fontStyle: "normal",
  textAnchor: "middle",
  fontFamily: "Segoe UI",
  lineHeight: "21",
  alignItems: "center",
  textAlign: "center",
  display: "flex",
};

const donutMiddleTextStyle: TextStyle = {
  fontSize: "55",
  color: "#323130",
  fontWeight: "400",
  fontStyle: "normal",
  textAnchor: "middle",
  fontFamily: "Segoe UI",
  lineHeight: "73",
  alignItems: "center",
  textAlign: "center",
  display: "flex",
};

function DonutChart({
  data,
  width,
  height,
  innerRadius,
  outerRadius,
}: DonutChartProps) {
  React.useEffect(() => {
    /* ------------------------------------------------------------ Set up and define constants ------------------------------------------------------------  */
    const svg = d3.select("#donutchart");
    svg.selectAll("*").remove();

    /*------------------------------  Define chart dimensions ------------------------------  */
    const innerRadiusHover = innerRadius;
    const outerRadiusHover = outerRadius + 25;
    const donutMiddleTitle = "Total physical qubits";
    const padAngle = 0.01;

    const translationValX: number = width / 4;
    const translationValY: number = height / 4;

    /* ------------------------------  Define chart styling constants ------------------------------ */
    const chartOpacity = 0.75;
    const chartHoverOpacity = 1;
    const colorArray = ["#1a5d8c", "#8c1a5c", "#aebac0", "#323130"];

    /*------------------------------  Define color ranges  ------------------------------  */
    const algorithmRunTimeColor = colorArray[1];
    const tfactoryLineColor = colorArray[0];

    const chartColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(data, (d) => {
          return d.legendTitle;
        }) as unknown as string,
      )
      .range([algorithmRunTimeColor, tfactoryLineColor]);

    /* ------------------------------------------------------------ Begin draw chart ------------------------------------------------------------  */

    /*------------------------------  Create pie and arc generators  ------------------------------  */
    const pieGenerator = d3
      .pie<d3Helper.LegendData>()
      .padAngle(padAngle)
      .value((d) => d.value)
      .sort(null);

    const arcGenerator = d3
      .arc<PieArcDatum<d3Helper.LegendData>>()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    const pieData = pieGenerator(data);

    const arcs = svg
      .selectAll("g")
      .data(pieData)
      .enter()
      .append("g")
      .attr("class", "arc")
      .attr(
        "transform",
        `translate(${innerRadius + translationValX},${
          innerRadius + translationValY
        })`,
      );

    /*------------------------------  Fill donut chart and apply hover  ------------------------------  */
    arcs
      .append("path")
      .attr("d", arcGenerator)
      .attr("fill", (d) => {
        return chartColor(d.data.legendTitle) as string;
      })
      .style("opacity", chartOpacity)
      .on("mouseover", (d) => {
        const arcHover = d3
          .arc<PieArcDatum<d3Helper.LegendData>>()
          .innerRadius(innerRadiusHover)
          .outerRadius(outerRadiusHover);
        d3.select(d.target).attr("d", arcHover as any);
        d3.select(d.target).style("opacity", chartHoverOpacity);
      })
      .on("mouseout", (d) => {
        d3.select(d.target).attr("d", arcGenerator as any);
        d3.select(d.target).style("opacity", chartOpacity);
      });

    // Add tooltips
    arcs
      .append("title")
      .text(
        (d) =>
          `${d.data.title} ${d.data.legendTitle} : ${d3Format.format(",.0f")(
            d.value,
          )}`,
      );

    /*------------------------------  Draw Legend ------------------------------  */
    const legendY = translationValY + outerRadius * 2 + 10;
    const midpoint = outerRadius + 10;
    d3Helper.drawLegend(
      svg,
      data,
      midpoint,
      legendY,
      translationValX,
      chartColor,
      true,
      false,
    );

    /*------------------------------  Add text and titles  ------------------------------  */

    // Add chart title
    d3Helper.drawText(
      svg,
      "Space diagram",
      innerRadius + translationValX,
      translationValY - innerRadius,
      titleStyle,
    );

    // Add middle text
    const totalQubits = d3.sum(data, (d) => d.value);
    const totalQubitsStr = d3Format.format(",.0f")(totalQubits);

    d3Helper.drawText(
      svg,
      donutMiddleTitle,
      innerRadius + translationValX,
      translationValY + innerRadius - 25,
      donutMiddleTitleStyle,
    );
    d3Helper.drawText(
      svg,
      totalQubitsStr,
      innerRadius + translationValX,
      translationValY + innerRadius + 25,
      donutMiddleTextStyle,
    );
  }, [data, innerRadius, outerRadius]);

  return (
    <div
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <svg id="donutchart" width={width} height={height}></svg>
    </div>
  );
}

export default DonutChart;
