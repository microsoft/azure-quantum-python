import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";

type Data = {
  title: string;
  legendTitle: string;
  value: string;
};

interface LineChartProps {
  chartData: Data[];
  chartLength: number;
  width: number;
  height: number;
}

// THIS FILE IS UNDER CONSTRUCTION.

function LineChart({ chartData, chartLength, width, height }: LineChartProps) {
  React.useEffect(() => {
    const svg = d3.select("svg");
    svg.selectAll("*").remove();

    /* Define Constants */
    const colors = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--d3-colors");
    const colorArray = colors.split(',');
    const algorithmRunTimeColor = colorArray[1];
    const tfactoryLineColor = colorArray[0];
    const timeLineColor = "#323130";

    const bottomY = 400;
    const distBetweenCharts = 100;
    const lengthInner = chartLength - 40;
    const originPoint = [0, 0];

    const algorithmRunTimeLine = [
      [0, bottomY - distBetweenCharts],
      [lengthInner, bottomY - distBetweenCharts],
    ];

    const timeLine = [
      [0, bottomY],
      [chartLength, bottomY],
    ];

    const startDashedLine = [
      [40, bottomY],
      [40, bottomY - (distBetweenCharts * 2)],
    ];

    const endDashedLine = [
      [lengthInner + 7, bottomY],
      [lengthInner + 7, bottomY - distBetweenCharts],
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

    const markerBoxWidth = 8;
    const markerBoxHeight = 8;
    const refX = markerBoxWidth / 2;
    const refY = markerBoxHeight / 2;

    // Create line generator 
    const lineGenerator = d3.line();

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
      .attr("stroke-width", "2")
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
      .attr("stroke-width", "2")
      .attr("marker-start", "url(#startMarkerTimeLine)")
      .attr("marker-end", "url(#arrowTimeLine)")
      .style("fill", timeLineColor)
      .style("stroke", timeLineColor)

    // Append text label to  time line.
    svg
      .append("text")
      .attr("x", chartLength + 10)
      .attr("y", bottomY + 5)
      .text(`Time`)
      .attr("class", "time");

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
      .attr("stroke-width", "2")
      .style("fill", "none")
      .style("stroke", timeLineColor)
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(endDashedLine))
      .attr("stroke-width", "2")
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
      .attr("refY", refYStartMarker -2)
      .attr("markerHeight", startMarkerBoxHeight - 4)
      .attr("markerWidth", startMarkerBoxWidth)
      .style("fill",tfactoryLineColor)
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
      .style("fill",tfactoryLineColor)
      .style("stroke", tfactoryLineColor)
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints));

   
    // set the number of lines
   var numLines = 60;

 
      const showSplit = (numLines > 50);
      if (showSplit) {
        numLines = 50;
      }

         // define the x scale
    const xScale = d3
    .scaleLinear()
    .domain([0,numLines])
    .range([0, lengthInner]);

    // define elipses marker
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
      .attr("r", 4)
      .style("fill", timeLineColor);

    // draw the lines
    for (let i = 0; i < numLines; i++) {
      let line = svg.append('line');
      line.attr('x1', xScale(i))
          .attr('x2', xScale(i+1))
          .attr('y1', bottomY - (distBetweenCharts * 2 ))
          .attr('y2', bottomY - (distBetweenCharts * 2 ))
          .attr("stroke-width", "2")
          .style("fill", "none")
          .style("stroke", tfactoryLineColor)
          .attr("marker-start", "url(#startMarkerTFactory)")
          .attr('marker-end', 'url(#arrowTFactory)');
    }
          if (showSplit) {
           svg.append('line')
           .attr('x1', xScale(25))
              .attr('x2', xScale(25))
              .attr('y1', 0)
              .attr('y2', bottomY - (distBetweenCharts * 2 ))
              .attr('marker-end', 'url(#circleMarkerElipses)');

              svg.append('line')
              .attr('x1', xScale(25+1))
              .attr('x2', xScale(25+1))
              .attr('y1', 0)
              .attr('y2', bottomY - (distBetweenCharts * 2 ))
              .attr('marker-end', 'url(#circleMarkerElipses)');

              svg.append('line')
              .attr('x1', xScale(25 - 1))
              .attr('x2', xScale(25 - 1))
              .attr('y1', 0)
              .attr('y2', bottomY - (distBetweenCharts * 2 ))
              .attr('marker-end', 'url(#circleMarkerElipses)');

    }
  }, [chartData, width, height]);

  return (
    <div>
      <div className="svg-container">
        <svg className="svg-element" width={width} height={height}></svg>
      </div>
    </div>
  );
}

export default LineChart;
