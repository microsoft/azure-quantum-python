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

    const lengthInner = chartLength - 20;

    var algorithmRunTimeLine = [
      [0, 0],
      [lengthInner, 0],
    ];

    const timeLine = [
      [0, 0],
      [chartLength, 0],
    ];
    const startDashedLine = [
      [40, -70],
      [40, 0],
    ];

    const endDashedLine = [
      [lengthInner, -70],
      [lengthInner, 0],
    ];

    var startMarkerPoints = [
      [0, 0],
      [0, 10],
      [2, 10],
      [2, 0],
    ];

    var startMarkerBoxWidth = 10;
    var startMarkerBoxHeight = 10;
    var refXRect = 2;
    var refYRect = startMarkerBoxHeight / 2;

    var arrowPoints = [
      [0, 0],
      [0, 8],
      [8, 4],
    ];
    var markerBoxWidth = 8;
    var markerBoxHeight = 8;
    var refX = markerBoxWidth / 2;
    var refY = markerBoxHeight / 2;

    var lineGenerator = d3.line();

    svg
      .append("defs")
      .append("marker")
      .attr("id", "arrowAlgorithmLine")
      .attr("viewBox", [0, 0, markerBoxWidth + 4, markerBoxHeight])
      .attr("refX", refX)
      .attr("refY", refY)
      .attr("markerWidth", markerBoxWidth - 3)
      .attr("markerHeight", markerBoxHeight - 4)
      .style("fill", "#00A2AD")
      .style("stroke", "#00A2AD")
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(arrowPoints));

    svg
      .append("defs")
      .append("marker")
      .attr("id", "startMarkerTimeLine")
      .attr("viewBox", [0, 0, startMarkerBoxWidth + 4, startMarkerBoxHeight])
      .attr("refX", refXRect)
      .attr("refY", refYRect)
      .attr("markerWidth", startMarkerBoxWidth)
      .attr("markerHeight", startMarkerBoxHeight)
      .style("fill", "#323130")
      .style("stroke", "#323130")
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(startMarkerPoints));

    svg
      .append("defs")
      .append("marker")
      .attr("id", "startMarkerAlgorithm")
      .attr("viewBox", [0, 0, startMarkerBoxWidth + 4, startMarkerBoxHeight])
      .attr("refX", refXRect)
      .attr("refY", refYRect)
      .attr("markerWidth", startMarkerBoxWidth - 3)
      .attr("markerHeight", startMarkerBoxHeight - 4)
      .style("fill", "#00A2AD")
      .style("stroke", "#00A2AD")
      .style("stroke-width", "1")
      .attr("orient", "auto-start-reverse")
      .append("path")
      .attr("d", d3.line()(startMarkerPoints));

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
      .style("fill", "#323130");

    svg
      .append("path")
      .attr("class", "line")
      .attr("d", lineGenerator(algorithmRunTimeLine))
      .style("fill", "none")
      .attr("stroke-width", "3")
      .attr("marker-end", "url(#arrowAlgorithmLine)")
      .attr("marker-start", "url(#startMarkerAlgorithm)")
      .attr("stroke", "#00A2AD");

    svg
      .append("text")
      .attr("x", timeLine[1][0] + 15)
      .attr("y", timeLine[1][1] + 75)
      .text(`Time`)
      .attr("class", "time");

    svg
      .append("path")
      .attr("class", "line")
      .attr("transform", "translate(" + 0 + "," + 70 + ")")
      .attr("d", lineGenerator(timeLine))
      .attr("stroke-width", "2")
      .style("fill", "none")
      .style("stroke", "#323130")
      .attr("marker-end", "url(#arrowTimeLine)")
      .attr("marker-start", "url(#startMarkerTimeLine)");

    svg
      .append("path")
      .attr("class", "line")
      .attr("transform", "translate(" + 0 + "," + 70 + ")")
      .attr("d", lineGenerator(startDashedLine))
      .attr("stroke-width", "2")
      .style("fill", "none")
      .style("stroke", "#323130")
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    svg
      .append("path")
      .attr("class", "line")
      .attr("transform", "translate(" + 8 + "," + 70 + ")")
      .attr("d", lineGenerator(endDashedLine))
      .attr("stroke-width", "2")
      .style("fill", "none")
      .style("stroke", "#323130")
      .style("stroke-dasharray", "3,3")
      .attr("marker-end", "url(#circleMarker)")
      .attr("marker-start", "url(#circleMarker)");

    // dashed lines:

    // create svg

    // set the number of lines
    const numberOfLines = 15;

    // set the maximum length of the chart
    const maxLength = 300;

    // determine the gap to place between each line
    let gap;
    if (numberOfLines > 100) {
      gap = maxLength / numberOfLines;
    } else {
      gap = maxLength / (numberOfLines - 1);
    }

    // define the x scale
    const xScale = d3
      .scaleLinear()
      .domain([0, numberOfLines])
      .range([0, maxLength]);

    // define the data
    let data = [];
    for (let i = 0; i <= numberOfLines; i++) {
      data.push({ x: xScale(i) });
    }

    // draw the lines
    svg
      .selectAll(".line")
      .data(data)
      .enter()
      .append("line")
      .attr("class", "line")
      .attr("x1", (d) => d.x)
      .attr("x2", (d) => d.x + 25)
      .attr("y1", 20)
      .attr("y2", 20)
      .attr("stroke", "black")
      .attr("stroke-width", 1);

    // draw the arrows
    /*
    svg
      .selectAll(".arrow")
      .data(data)
      .enter()
      .append("polygon")
      .attr("class", "arrow")
      .attr("points", (d) => `${d.x},${-5} ${d.x - 5},${0} ${d.x + 5},${0}`)
      .attr("fill", "black")
      .attr("stroke", "black")
      .attr("stroke-width", 2);*/

    // draw the elippses
    if (numberOfLines > 100) {
      svg
        .append("ellipse")
        .attr("cx", maxLength / 2)
        .attr("cy", height / 2)
        .attr("rx", gap / 2)
        .attr("ry", 10)
        .attr("fill", "black")
        .attr("stroke", "black")
        .attr("stroke-width", 2);
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
