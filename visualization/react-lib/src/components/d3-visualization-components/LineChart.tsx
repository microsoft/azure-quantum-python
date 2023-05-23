import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";
import { Tooltip } from "@mui/material";

type LegendData = {
  title: string;
  legendTitle: string;
  value: string;
};

interface LineChartProps {
  legendData: LegendData[];
  chartData: { [key: string]: any };
  width: number;
  height: number;
}

function LineChart({ legendData, chartData, width, height }: LineChartProps) {
  React.useEffect(() => {
    const svg = d3.select("svg");
    svg.selectAll("*").remove();

    /* Define Constants from CSS */
    const colors = getComputedStyle(document.documentElement).getPropertyValue(
      "--d3-colors"
    );

    const dimensionsLegend = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--dimensions-legend");

    const strokeWidth = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--stroke-width");

    const colorArray = colors.split(",");
    const algorithmRunTimeColor = colorArray[1];
    const tfactoryLineColor = colorArray[0];
    const ellipsesColor = colorArray[2];
    const timeLineColor = colorArray[3];

    /* Define chart data from dictionary */
    const numberTStates: number = chartData["numberTStates"];
    const numberTFactoryInvocations: number = 78;
    //chartData["numberTFactoryInvocations"];
    const algorithmRuntime: number = 6000;
    const tFactoryRuntime: number = 20;
    const algorithmRuntimeFormatted: string =
      chartData["algorithmRuntimeFormatted"];
    const tFactoryRuntimeFormatted: string =
      chartData["tFactoryRuntimeFormatted"];
    const chartLength: number = chartData["chartLength"];

    /* Define chart constants */
    const tfactoryLineLabel =
      numberTStates +
      (numberTStates == 1
        ? " T-state produced after each invocations runtime"
        : " T-states produced after each invocations runtime");

    const chartBottomY = width / 2;
    const distBetweenCharts = 100;
    const lengthInner = chartLength - 100;
    const originPoint = [0, 0];
    const midpoint = chartLength / 2;

    /* Define chart ratios */
    const tFactoryAlgorithmRuntimeDiffNanoseconds =
      algorithmRuntime - tFactoryRuntime;
    var tFactoryTimeAdjGap = 0;
    var lengthInnerAdj = lengthInner;
    if (tFactoryAlgorithmRuntimeDiffNanoseconds > 0) {
      var lengthDiff = Math.round(
        lengthInner *
          (tFactoryAlgorithmRuntimeDiffNanoseconds / algorithmRuntime)
      );
      lengthInnerAdj = lengthInner - lengthDiff;
      tFactoryTimeAdjGap = lengthDiff / numberTFactoryInvocations / 100;
    }

    /* Define line points */
    const algorithmRunTimeLine = [
      [0, chartBottomY - distBetweenCharts],
      [lengthInner, chartBottomY - distBetweenCharts],
    ];

    const timeLine = [
      [0, chartBottomY],
      [chartLength, chartBottomY],
    ];

    const endDashedLine = [
      [lengthInner + 7, chartBottomY],
      [lengthInner + 7, chartBottomY - distBetweenCharts],
    ];

    const startMarkerBoxWidth = 1;
    const startMarkerBoxHeight = 10;
    const refXStartMarker = 1;
    const refYStartMarker = startMarkerBoxHeight / 2;

    const startMarkerPoints = [
      originPoint,
      [0, startMarkerBoxHeight],
      [startMarkerBoxWidth, startMarkerBoxHeight],
      [startMarkerBoxWidth, 0],
    ];

    const arrowPoints = [
      [0, 0],
      [0, 3],
      [3, 1.5],
    ];

    const translationValX = width / 4;
    const translationValY = height / 4;

    // Define values for arrows
    const markerBoxWidth = 8;
    const markerBoxHeight = 8;
    const refX = markerBoxWidth / 2;
    const refY = markerBoxHeight / 2;

    // Create line generator
    const lineGenerator = d3.line();

    // Add chart title
    svg
      .append("text")
      .attr("x", midpoint)
      .attr("y", chartBottomY - distBetweenCharts * 3)
      .attr("class", "title")
      .text("Time diagram");

    // Create legend
    var legendColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(legendData, (d) => {
          return d.title;
        }) as unknown as string
      )
      .range([algorithmRunTimeColor, tfactoryLineColor]);

    const legend = svg
      .selectAll(".legend")
      .data(legendData)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr(
        "transform",
        (d, i) => `translate(${(i * midpoint) / 4}, ${chartBottomY})`
      );

    legend
      .append("rect")
      .attr("width", dimensionsLegend.toString())
      .attr("height", dimensionsLegend.toString())
      .attr("x", 0)
      .attr("y", 50)
      .style("fill", (d, i) => legendColor(d.title) as string);

    legend
      .append("text")
      .attr("x", 25)
      .attr("y", 60)
      .text((d) => `${d.title}`)
      .attr("class", "legend");

    legend
      .append("text")
      .attr("x", 25)
      .attr("y", 75)
      .text((d) => `${d.legendTitle}`)
      .attr("class", "legend-maintext");

    /* Create algorithm line */

    // Create algorithm start bar
    svg
      .append("defs")
      .append("marker")
      .attr("id", "startMarkerAlgorithm")
      .attr("class", "startMarkerAlgorithm")
      .attr("refX", refXStartMarker)
      .attr("refY", refYStartMarker)
      .attr("markerHeight", startMarkerBoxHeight)
      .attr("markerWidth", startMarkerBoxWidth)
      .style("fill", algorithmRunTimeColor)
      .style("stroke", algorithmRunTimeColor)
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(startMarkerPoints as any));

    // Create algorithm end arrow
    svg
      .append("marker")
      .attr("id", "arrowAlgorithmLine")
      .attr("viewBox", [0, 0, markerBoxWidth + 4, markerBoxHeight])
      .attr("refX", refX)
      .attr("refY", refY)
      .attr("markerWidth", markerBoxWidth - 3)
      .attr("markerHeight", markerBoxHeight - 4)
      .style("fill", algorithmRunTimeColor)
      .style("stroke", algorithmRunTimeColor)
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints as any));

    // Draw algorithm line
    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(algorithmRunTimeLine as any))
      .style("fill", "none")
      .attr("stroke-width", strokeWidth)
      .attr("marker-end", "url(#arrowAlgorithmLine)")
      .attr("marker-start", "url(#startMarkerAlgorithm)")
      .style("stroke", algorithmRunTimeColor);

    // Create timeline start bar
    svg
      .append("defs")
      .append("marker")
      .attr("id", "startMarkerTimeLine")
      .attr("refX", refXStartMarker)
      .attr("refY", refYStartMarker)
      .attr("markerHeight", startMarkerBoxHeight)
      .attr("markerWidth", startMarkerBoxWidth)
      .style("fill", timeLineColor)
      .style("stroke", timeLineColor)
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(startMarkerPoints as any));

    // Create timeline end arrow
    svg
      .append("marker")
      .attr("id", "arrowTimeLine")
      .attr("viewBox", [0, 0, markerBoxWidth + 4, markerBoxHeight])
      .attr("refX", refX)
      .attr("refY", refY)
      .attr("markerWidth", markerBoxWidth - 3)
      .attr("markerHeight", markerBoxHeight - 4)
      .style("fill", timeLineColor)
      .style("stroke", timeLineColor)
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints as any));

    // Draw timeline.
    svg
      .append("path")
      .attr("class", "line")
      .attr("id", "timeline")
      .attr("d", lineGenerator(timeLine as any))
      .attr("stroke-width", strokeWidth)
      .attr("marker-start", "url(#startMarkerTimeLine)")
      .attr("marker-end", "url(#arrowTimeLine)")
      .style("fill", timeLineColor)
      .style("stroke", timeLineColor);

    // Append text labels to  time line.
    svg
      .append("text")
      .attr("x", chartLength + 10)
      .attr("y", chartBottomY + 10)
      .text("Time")
      .attr("class", "time");

    svg
      .append("text")
      .attr("x", lengthInner + 15)
      .attr("y", chartBottomY - 10)
      .text(algorithmRuntimeFormatted)
      .attr("class", "runtimeText");

    // Define circle markers for dashed lines.
    svg
      .append("defs")
      .append("marker")
      .attr("id", "circleMarker")
      .attr("viewBox", [0, 0, 20, 20])
      .attr("refX", 5)
      .attr("refY", 5)
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .append("circle")
      .attr("cx", 5)
      .attr("cy", 5)
      .attr("r", 3)
      .style("fill", timeLineColor);

    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(endDashedLine as any))
      .attr("stroke-width", strokeWidth)
      .style("fill", "none")
      .style("stroke", timeLineColor)
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    // Create tfactory start bar
    svg
      .append("defs")
      .append("marker")
      .attr("id", "startMarkerTFactory")
      .attr("refX", refXStartMarker)
      .attr("refY", refYStartMarker - 2)
      .attr("markerHeight", startMarkerBoxHeight - 4)
      .attr("markerWidth", startMarkerBoxWidth)
      .style("fill", tfactoryLineColor)
      .style("stroke", tfactoryLineColor)
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(startMarkerPoints as any));

    // Create timeline end arrow
    svg
      .append("marker")
      .attr("id", "arrowTFactory")
      .attr("refX", 2)
      .attr("refY", 1.5)
      .attr("markerWidth", 3)
      .attr("markerHeight", 3)
      .style("fill", tfactoryLineColor)
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints as any));

    // set the number of lines
    var numLines = numberTFactoryInvocations;

    // If more t-factory invocations than 50, set showSplit variable to insert ellipses.
    const showSplit = numLines > 50;
    if (showSplit) {
      numLines = 50;
    }

    // define the x scale
    const xScale = d3
      .scaleLinear()
      .domain([0, numLines + numLines * tFactoryTimeAdjGap])
      .range([0, lengthInner]);

    // define ellipses marker
    svg
      .append("defs")
      .append("marker")
      .attr("id", "circleMarkerElipses")
      .attr("viewBox", [0, 0, 10, 10])
      .attr("refX", 5)
      .attr("refY", 5)
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .append("circle")
      .attr("cx", 5)
      .attr("cy", 5)
      .attr("r", 3)
      .style("fill", ellipsesColor);

    // draw the lines

    const tFactoryDashedLine = [
      [xScale(1) + 1, chartBottomY],
      [xScale(1) + 1, chartBottomY - distBetweenCharts * 2],
    ];

    // Draw dashed line of single t-factory invocation runtime.
    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(tFactoryDashedLine as any))
      .attr("stroke-width", strokeWidth)
      .style("fill", "none")
      .style("stroke", timeLineColor)
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    // Append single t-factory invocation runtime text
    svg
      .append("text")
      .attr("x", xScale(1) + 10)
      .attr("y", chartBottomY - 10)
      .text(tFactoryRuntimeFormatted)
      .attr("class", "runtimeText");

    // Append t-factory line label
    svg
      .append("text")
      .attr("x", xScale(1) + 10)
      .attr("y", chartBottomY - distBetweenCharts * 2 + 30)
      .text(tfactoryLineLabel)
      .attr("class", "runtimeText");

    for (let i = 0; i < numLines - 1; i++) {
      let line = svg.append("line");
      line
        .attr("x1", xScale(i) + i * xScale(tFactoryTimeAdjGap))
        .attr("x2", xScale(i + 1) + i * xScale(tFactoryTimeAdjGap))
        .attr("y1", chartBottomY - distBetweenCharts * 2)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("stroke-width", strokeWidth)
        .attr("id", "tfactoryLine")
        .style("fill", "none")
        .style("stroke", tfactoryLineColor)
        .attr("marker-start", "url(#startMarkerTFactory)")
        .attr("marker-end", "url(#arrowTFactory)")
        .lower();
    }

    var lastLineStartx = numLines - 1;
    let lastLine = svg.append("line");
    lastLine
      .attr(
        "x1",
        xScale(lastLineStartx) + lastLineStartx * xScale(tFactoryTimeAdjGap)
      )
      .attr(
        "x2",
        xScale(lastLineStartx + 1) + lastLineStartx * xScale(tFactoryTimeAdjGap)
      )
      .attr("y1", chartBottomY - distBetweenCharts * 2)
      .attr("y2", chartBottomY - distBetweenCharts * 2)
      .attr("stroke-width", strokeWidth)
      .attr("id", "tfactoryLine")
      .style("fill", "none")
      .style("stroke", tfactoryLineColor)
      .attr("marker-start", "url(#startMarkerTFactory)")
      .attr("marker-end", "url(#arrowTFactory)")
      .lower();

    if (showSplit) {
      svg
        .append("rect")
        .attr("x", lengthInner / 2 - 20)
        .attr("y", chartBottomY - distBetweenCharts * 2 - 10)
        .attr("width", "40")
        .attr("height", "20")
        .attr("fill", "#FFFFFF")
        .raise();

      var ellipsesStartX = numLines / 2;

      svg
        .append("line")
        .attr("x1", lengthInner / 2)
        .attr("x2", lengthInner / 2)
        .attr("y1", chartBottomY - distBetweenCharts * 2)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("marker-end", "url(#circleMarkerElipses)");

      svg
        .append("line")
        .attr("x1", lengthInner / 2 + 10)
        .attr("x2", lengthInner / 2 + 10)
        .attr("y1", chartBottomY - distBetweenCharts * 2)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("marker-end", "url(#circleMarkerElipses)");

      svg
        .append("line")
        .attr("x1", lengthInner / 2 - 10)
        .attr("x2", lengthInner / 2 - 10)
        .attr("y1", chartBottomY - distBetweenCharts * 2)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("marker-end", "url(#circleMarkerElipses)");
    }
  }, [width, height]);

  return (
    <div>
      <div className="svg-container">
        <svg className="svg-element" width={width} height={height}></svg>
      </div>
    </div>
  );
}

export default LineChart;
