/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import * as d3 from "d3";
import * as d3Format from "d3-format";

export type LegendData = {
  title: string;
  legendTitle: string;
  value: number;
};

export interface TextStyle {
  fontFamily: string;
  fontStyle: string;
  fontWeight: string;
  fontSize: string;
  lineHeight: string;
  display: string;
  alignItems: string | null | undefined;
  textAlign: string | null | undefined;
  color: string;
  textAnchor: string | null | undefined;
}

export function drawEllipses(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  cx: number,
  cy: number,
  spaceBetween: number,
  radius: number,
  fillColor: string,
) {
  svg
    .append("circle")
    .attr("cx", cx)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);

  svg
    .append("circle")
    .attr("cx", cx + spaceBetween)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);

  svg
    .append("circle")
    .attr("cx", cx + spaceBetween * 2)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);
}

export function drawLine(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  linePoints: number[][],
  id: string,
  strokeWidth: string,
  markerStart: string,
  markerEnd: string,
  fillColor: string,
  strokeColor: string,
  isDashed: boolean,
) {
  // Create line generator
  const lineGenerator = d3.line();
  if (isDashed) {
    svg
      .append("path")
      .attr("id", id)
      .attr("d", lineGenerator(linePoints as any))
      .attr("stroke-width", strokeWidth)
      .attr("marker-start", markerStart)
      .attr("marker-end", markerEnd)
      .style("fill", fillColor)
      .style("stroke-dasharray", "3,3")
      .style("stroke", strokeColor);
  } else {
    svg
      .append("path")
      .attr("id", id)
      .attr("d", lineGenerator(linePoints as any))
      .attr("stroke-width", strokeWidth)
      .attr("marker-start", markerStart)
      .attr("marker-end", markerEnd)
      .style("fill", fillColor)
      .style("stroke", strokeColor)
      .lower();
  }
}

export function drawLegend(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  legendData: LegendData[],
  midpoint: number,
  chartBottomY: number,
  chartStartX: number,
  legendColor: d3.ScaleOrdinal<string, unknown, never>,
  showLegendValues: boolean,
  useTitleForColor: boolean,
) {
  const legend = svg
    .selectAll(".legend")
    .data(legendData)
    .enter()
    .append("g")
    .attr(
      "transform",
      (d, i) => `translate(${midpoint * i + chartStartX}, ${chartBottomY})`,
    );

  if (useTitleForColor) {
    legend
      .append("rect")
      .attr("width", 20)
      .attr("height", 20)
      .attr("x", 0)
      .attr("y", 50)
      .style("fill", (d) => legendColor(d.title) as string);
  } else {
    legend
      .append("rect")
      .attr("width", 20)
      .attr("height", 20)
      .attr("x", 0)
      .attr("y", 50)
      .style("fill", (d) => legendColor(d.legendTitle) as string);
  }

  legend
    .append("text")
    .attr("x", 25)
    .attr("y", 60)
    .text((d) => `${d.title}`)
    .style("font-size", "14px")
    .style("font-family", "Segoe UI")
    .style("line-height", "18px")
    .style("fill", "black")
    .style("font-weight", "600")
    .style("font-style", "normal");

  legend
    .append("text")
    .attr("x", 25)
    .attr("y", 75)
    .text((d) => `${d.legendTitle}`)
    .style("font-size", "14px")
    .style("font-family", "Segoe UI")
    .style("line-height", "18px")
    .style("fill", "black")
    .style("font-weight", "400")
    .style("font-style", "normal");

  if (showLegendValues) {
    legend
      .append("text")
      .attr("x", 25)
      .attr("y", 100)
      .text((d) => `${d3Format.format(",.0f")(d.value)}`)
      .style("font-size", "28px")
      .style("font-family", "Segoe UI")
      .style("line-height", "34px")
      .style("fill", "#24272b")
      .style("font-style", "normal")
      .style("font-weight", "600");
  }
}

export function drawText(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  text: string,
  x: number,
  y: number,
  styles: TextStyle,
) {
  const alignItems = styles.alignItems ? styles.alignItems : "";
  const textAlign = styles.textAlign ? styles.textAlign : "";
  const textAnchor = styles.textAnchor ? styles.textAnchor : "";

  svg
    .append("text")
    .attr("x", x)
    .attr("y", y)
    .text(text)
    .raise()
    .style("font-family", styles.fontFamily)
    .style("font-style", styles.fontStyle)
    .style("font-weight", styles.fontWeight)
    .style("font-size", styles.fontSize)
    .style("line-height", styles.lineHeight)
    .style("display", styles.display)
    .style("align-items", alignItems)
    .style("text-align", textAlign)
    .style("fill", styles.color)
    .style("text-anchor", textAnchor);
}

export function drawArrow(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  color: string,
  id: string,
) {
  const markerDim = 3;
  const refX = 2;
  const refY = 1.5;
  const arrowPoints = [
    [0, 0],
    [0, markerDim],
    [markerDim, refY],
  ];

  svg
    .append("marker")
    .attr("id", id)
    .attr("refX", refX)
    .attr("refY", refY)
    .attr("markerWidth", markerDim)
    .attr("markerHeight", markerDim)
    .style("fill", color)
    .attr("orient", "auto-start-reverse")
    .append("path")
    .attr("d", d3.line()(arrowPoints as any));
}

export function drawLineTick(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  width: number,
  height: number,
  color: string,
  id: string,
) {
  const refX = 1;
  const refY = height / 2;

  const markerPoints = [
    [0, 0],
    [0, height],
    [width, height],
    [width, 0],
  ];

  svg
    .append("defs")
    .append("marker")
    .attr("id", id)
    .attr("refX", refX)
    .attr("refY", refY)
    .attr("markerHeight", height)
    .attr("markerWidth", width)
    .style("fill", color)
    .style("stroke", color)
    .attr("orient", "auto-start-reverse")
    .append("path")
    .attr("d", d3.line()(markerPoints as any));
}

export function drawCircleMarkers(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  width: number,
  height: number,
  color: string,
  radius: number,
  refX: number,
  refY: number,
  cx: number,
  cy: number,
  id: string,
) {
  svg
    .append("defs")
    .append("marker")
    .attr("id", id)
    .attr("refX", refX)
    .attr("refY", refY)
    .attr("markerWidth", width)
    .attr("markerHeight", height)
    .append("circle")
    .attr("cx", cx)
    .attr("cy", cy)
    .attr("r", radius)
    .style("fill", color);
}
