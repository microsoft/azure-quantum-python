import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";
import { RowGroup } from "../Table";
import Table from "../Table";

type Data = {
  title: string;
  legendTitle: string;
  value: number;
};

interface LineChartProps {
  data: Data[];
  lengthOuter: number;
  lengthInner: number;
  width: number;
  height: number;
  marginVal: number;
}

function LineChart({
  data,
  lengthInner,
  lengthOuter,
  width,
  height,
  marginVal,
}: LineChartProps) {
  React.useEffect(() => {
    const svg = d3.select("svg");
    svg.selectAll("*").remove();

    var algorithmRunTimeLine = [
      [0, 0],
      [lengthInner, 0],
    ];
    const timeLine = [
      [0, 0],
      [lengthOuter, 0],
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
  }, [data, width, height]);

  /*
  var subHeadings: string[] = ["Name", "value"];
  const headings = ["Name1", "Value1"];
  var values = [1, 2];
  const tableData = {
    headings: ["Name", "Location", "Age"],
    subheadings: ["First", "Last", "City"],
    data: [
      ["John", "Doe", "Chicago"],
      ["Jane", "Doe", "New York City"],
      ["Dave", "Smith", "Los Angeles"],
    ],
  };*/

  const rowGroups: RowGroup[] = [
    {
      header: "Physical resource estimates",
      rows: [
        {
          data: [["Physical qubits", "1235423"]],
        },
      ],
    },
    {
      header: "T-factory parameters",
      rows: [
        {
          data: [["Physical qubits", "1214"]],
        },
      ],
    },
    {
      header: "Resource estimation breakdown",
      rows: [
        {
          data: [["Number of T-factory copies", "1214"]],
        },
        {
          data: [["Physical qubits for single T-factory copy", "1214"]],
        },
        {
          data: [["Total physical T-factory qubits", "1214"]],
        },
        {
          data: [["Physical algorithmic qubits", "1214"]],
        },
        {
          data: [["Logical algorithmic qubits", "1214"]],
        },
      ],
    },
    {
      header: "Logical qubit parameters",
      rows: [
        {
          data: [["Physical qubits", "1214"]],
        },
      ],
    },
  ];

  return (
    <div>
      <div className="svg-container">
        <svg
          className="svg-element"
          width={100}
          height={100}
          viewBox="-100 -100 1000 1000"
        ></svg>
      </div>
      <Table rowGroups={rowGroups} />
    </div>
  );
}

export default LineChart;
