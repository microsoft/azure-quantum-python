import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";

type Data = {
  title: string;
  legendTitle: string;
  value: string;
};

interface LineChartProps {
  legendData: Data[];
  numberTFactoryInvocations: number;
  numberTStates: number;
  algorithmRunTime: string;
  tFactoryRunTime: string;
  chartLength: number;
  width: number;
  height: number;
}

// THIS FILE IS UNDER CONSTRUCTION.

function LineChart({
  legendData,
  numberTFactoryInvocations,
  numberTStates,
  algorithmRunTime,
  tFactoryRunTime,
  chartLength,
  width,
  height,
}: LineChartProps) {
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

    /* Define line points */
    const algorithmRunTimeLine = [
      [0, chartBottomY - distBetweenCharts],
      [lengthInner, chartBottomY - distBetweenCharts],
    ];

    const timeLine = [
      [0, chartBottomY],
      [chartLength, chartBottomY],
    ];

    const startDashedLine = [
      [40, chartBottomY],
      [40, chartBottomY - distBetweenCharts * 2],
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
      [0, 8],
      [8, 4],
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
      .attr("d", d3.line()(startMarkerPoints));

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
      .attr("d", d3.line()(arrowPoints));

    // Draw algorithm line
    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(algorithmRunTimeLine))
      .style("fill", "none")
      .attr("stroke-width", strokeWidth)
      .attr("marker-end", "url(#arrowAlgorithmLine)")
      .attr("marker-start", "url(#startMarkerAlgorithm)")
      .style("stroke", algorithmRunTimeColor);

    /* Create time line */

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
      .attr("d", d3.line()(startMarkerPoints));

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
      .attr("d", d3.line()(arrowPoints));

    // Draw timeline.
    svg
      .append("path")
      .attr("class", "line")
      .attr("id", "timeline")
      .attr("d", lineGenerator(timeLine))
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
      .attr("x", 50)
      .attr("y", chartBottomY - 10)
      .text(tFactoryRunTime)
      .attr("class", "runtimeText");

    svg
      .append("text")
      .attr("x", lengthInner + 15)
      .attr("y", chartBottomY - 10)
      .text(algorithmRunTime)
      .attr("class", "runtimeText");

    svg
      .append("text")
      .attr("x", 50)
      .attr("y", chartBottomY - distBetweenCharts * 2 + 30)
      .text(tfactoryLineLabel)
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

    // Define dashed vertical lines.
    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(startDashedLine))
      .attr("stroke-width", strokeWidth)
      .style("fill", "none")
      .style("stroke", timeLineColor)
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(endDashedLine))
      .attr("stroke-width", strokeWidth)
      .style("fill", "none")
      .style("stroke", timeLineColor)
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    // dashed lines:

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
      .attr("d", d3.line()(startMarkerPoints));

    // Create timeline end arrow
    svg
      .append("marker")
      .attr("id", "arrowTFactory")
      .attr("viewBox", [0, 0, markerBoxWidth + 4, markerBoxHeight])
      .attr("refX", refX + 3)
      .attr("refY", refY)
      .attr("markerWidth", markerBoxWidth - 3)
      .attr("markerHeight", markerBoxHeight - 4)
      .style("fill", tfactoryLineColor)
      .style("stroke", tfactoryLineColor)
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints));

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
      .domain([0, numLines])
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
    for (let i = 0; i < numLines - 1; i++) {
      let line = svg.append("line");
      line
        .attr("x1", xScale(i))
        .attr("x2", xScale(i + 1))
        .attr("y1", chartBottomY - distBetweenCharts * 2)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("stroke-width", strokeWidth)
        .style("fill", "none")
        .style("stroke", tfactoryLineColor)
        .attr("marker-start", "url(#startMarkerTFactory)")
        .attr("marker-end", "url(#arrowTFactory)")
        .lower();
    }

    let endLine = svg.append("line");
    endLine
      .attr("x1", xScale(numLines - 1))
      .attr("x2", xScale(numLines))
      .attr("y1", chartBottomY - distBetweenCharts * 2)
      .attr("y2", chartBottomY - distBetweenCharts * 2)
      .attr("stroke-width", strokeWidth)
      .style("fill", "none")
      .style("stroke", tfactoryLineColor)
      .attr("marker-start", "url(#startMarkerTFactory)")
      .attr("marker-end", "url(#arrowTFactory)")
      .lower();

    if (showSplit) {
      svg
        .append("rect")
        .attr("x", xScale(23.5))
        .attr("y", chartBottomY - distBetweenCharts * 2 - 10)
        .attr("width", "55")
        .attr("height", "20")
        .attr("fill", "#FFFFFF")
        .raise();

      var ellipsesStartX = 25;
      svg
        .append("line")
        .attr("x1", xScale(ellipsesStartX))
        .attr("x2", xScale(ellipsesStartX))
        .attr("y1", 0)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("marker-end", "url(#circleMarkerElipses)");

      svg
        .append("line")
        .attr("x1", xScale(ellipsesStartX + 1))
        .attr("x2", xScale(ellipsesStartX + 1))
        .attr("y1", 0)
        .attr("y2", chartBottomY - distBetweenCharts * 2)
        .attr("marker-end", "url(#circleMarkerElipses)");

      svg
        .append("line")
        .attr("x1", xScale(ellipsesStartX - 1))
        .attr("x2", xScale(ellipsesStartX - 1))
        .attr("y1", 0)
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
