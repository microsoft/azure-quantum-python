import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";

export type LegendData = {
  title: string;
  legendTitle: string;
  value: string;
};

export type LineChartProps = {
  legendData: LegendData[];
  chartData: { [key: string]: any };
  width: number;
  height: number;
};

/* Helper Functions */
function drawEllipses(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  cx: number,
  cy: number,
  radius: number,
  fillColor: string
) {
  svg
    .append("circle")
    .attr("cx", cx)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);

  svg
    .append("circle")
    .attr("cx", cx + 15)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);

  svg
    .append("circle")
    .attr("cx", cx + 30)
    .attr("cy", cy)
    .attr("fill", fillColor)
    .attr("r", radius);
}
function drawLine(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  linePoints: number[][],
  className: string,
  id: string,
  strokeWidth: string,
  markerStart: string,
  markerEnd: string,
  fillColor: string,
  strokeColor: string,
  isDashed: boolean
) {
  // Create line generator
  const lineGenerator = d3.line();
  if (isDashed) {
    svg
      .append("path")
      .attr("class", className)
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
      .attr("class", className)
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

function drawLegend(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  legendData: LegendData[],
  dimensionsLegend: string,
  midpoint: number,
  chartBottomY: number,
  legendColor: d3.ScaleOrdinal<string, unknown, never>
) {
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
}

function drawText(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  text: string,
  x: number,
  y: number,
  className: string
) {
  svg
    .append("text")
    .attr("x", x)
    .attr("y", y)
    .text(text)
    .raise()
    .attr("class", className);
}

function drawArrow(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  color: string,
  id: string
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

function drawLineTick(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  width: number,
  height: number,
  color: string,
  id: string
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

function drawCircleMarkers(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  width: number,
  height: number,
  color: string,
  radius: number,
  refX: number,
  refY: number,
  cx: number,
  cy: number,
  id: string
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

function LineChart({ legendData, chartData, width, height }: LineChartProps) {
  React.useEffect(() => {
    const svg = d3.select("#linechart");
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
    const numberTFactoryInvocations: number =
      chartData["numberTFactoryInvocations"];
    const algorithmRuntime: number = 4500;
    const tFactoryRuntime: number = chartData["tFactoryRuntime"];
    const algorithmRuntimeFormatted: string =
      chartData["algorithmRuntimeFormatted"];
    const tFactoryRuntimeFormatted: string =
      chartData["tFactoryRuntimeFormatted"];
    const chartLength: number = chartData["chartLength"];

    /* Define chart constants */
    const tfactoryLineLabel =
      numberTStates +
      (numberTStates == 1
        ? " T state produced after each invocation's runtime"
        : " T states produced after each invocation's runtime");

    const chartBottomY = width / 2;
    const distBetweenCharts = 100;
    const lengthInner = chartLength - 100;
    const lengthTFactoryLine = lengthInner;
    const midpoint = chartLength / 2;
    const algorithmLineY = chartBottomY - distBetweenCharts;
    const tFactoryLineY = chartBottomY - distBetweenCharts * 2;
    const minAlgorithmLineLength = 50;
    const minTFactoryLength = 20;

    /* Define chart ratios */
    var lengthAlgorithmLine = lengthInner;
    var runtimeRatio = 1;

    var totalTFactoryRuntime = numberTFactoryInvocations * tFactoryRuntime;
    if (algorithmRuntime >= totalTFactoryRuntime) {
      runtimeRatio = algorithmRuntime / totalTFactoryRuntime;
    } else {
      lengthAlgorithmLine = Math.round(
        (algorithmRuntime / totalTFactoryRuntime) * lengthInner
      );
      if (lengthAlgorithmLine < minAlgorithmLineLength) {
        lengthAlgorithmLine = minAlgorithmLineLength;
      }
    }
    /* Define t-factory xScale and line points */
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
      .range([0, lengthTFactoryLine]);

    var tFactoryRefX = xScale(1) - runtimeRatio;

    var tFactoryDashedLine = [
      [tFactoryRefX + 3, chartBottomY],
      [tFactoryRefX + 3, tFactoryLineY],
    ];
    if (tFactoryRefX <= 0) {
      runtimeRatio = 5;
      tFactoryRefX = minTFactoryLength;
    }

    var algorithmDashedLineStart = lengthAlgorithmLine + 5;
    var algorithmTextY = chartBottomY - 10;

    /* Define line points */
    const algorithmRunTimeLine = [
      [0, algorithmLineY],
      [lengthAlgorithmLine, algorithmLineY],
    ];

    const timeLine = [
      [0, chartBottomY],
      [chartLength, chartBottomY],
    ];

    const algorithmDashedLine = [
      [algorithmDashedLineStart, chartBottomY],
      [algorithmDashedLineStart, algorithmLineY],
    ];

    /* Chart drawing */

    // Add chart title
    drawText(
      svg,
      "Time diagram",
      midpoint,
      chartBottomY - distBetweenCharts * 3,
      "title"
    );

    // Create legend
    var legendColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(legendData, (d) => {
          return d.title;
        }) as unknown as string
      )
      .range([algorithmRunTimeColor, tfactoryLineColor]);
    drawLegend(
      svg,
      legendData,
      dimensionsLegend,
      midpoint,
      chartBottomY,
      legendColor
    );

    /* Create algorithm line */

    // Create algorithm start bar
    drawLineTick(svg, 1, 10, algorithmRunTimeColor, "algorithmTick");
    // Create algorithm end arrow
    drawArrow(svg, algorithmRunTimeColor, "arrowAlgorithmLine");

    // Draw algorithm line
    drawLine(
      svg,
      algorithmRunTimeLine,
      "line",
      "algorithmRunTimeLine",
      strokeWidth,
      "url(#algorithmTick)",
      "url(#arrowAlgorithmLine)",
      algorithmRunTimeColor,
      algorithmRunTimeColor,
      false
    );

    // draw algorithm dashed line to show time
    drawLine(
      svg,
      algorithmDashedLine,
      "line",
      "endDashedLine",
      strokeWidth,
      "url(#circleMarker)",
      "url(#circleMarker)",
      "none",
      timeLineColor,
      true
    );

    drawCircleMarkers(
      svg,
      10,
      10,
      timeLineColor,
      1.5,
      5,
      5,
      5,
      5,
      "circleMarker"
    );

    drawText(
      svg,
      algorithmRuntimeFormatted,
      lengthAlgorithmLine + 10,
      algorithmTextY,
      "runtimeText"
    );

    /* Create TimeLine */
    // Create timeline start bar
    drawLineTick(svg, 1, 10, timeLineColor, "timeLineTick");
    // Create timeline end arrow
    drawArrow(svg, timeLineColor, "arrowTimeLine");
    // Draw timeline.
    drawLine(
      svg,
      timeLine,
      "line",
      "timeline",
      strokeWidth,
      "url(#timeLineTick)",
      "url(#arrowTimeLine)",
      timeLineColor,
      timeLineColor,
      false
    );

    // Append text labels to  time line.
    drawText(svg, "Time", chartLength + 10, chartBottomY + 10, "time");

    /* Create T-factory line */
    // Create tfactory start bar
    drawLineTick(svg, 1, 6, tfactoryLineColor, "tFactoryTick");

    // Create tfactory end arrow
    drawArrow(svg, tfactoryLineColor, "arrowTFactory");

    // Draw dashed line of single t-factory invocation runtime.
    drawLine(
      svg,
      tFactoryDashedLine,
      "line",
      "tfactoryDashedLine",
      strokeWidth,
      "url(#circleMarker)",
      "url(#circleMarker)",
      "none",
      timeLineColor,
      true
    );

    // Append single t-factory invocation runtime text
    drawText(
      svg,
      tFactoryRuntimeFormatted,
      tFactoryRefX + 5,
      chartBottomY + 20,
      "runtimeText"
    );

    // Append t-factory line label
    drawText(
      svg,
      tfactoryLineLabel,
      tFactoryRefX + 10,
      tFactoryLineY + 30,
      "runtimeText"
    );

    var numberTFactoryInvocationsText =
      numberTFactoryInvocations + " T factory invocations";
    drawText(
      svg,
      numberTFactoryInvocationsText,
      tFactoryRefX + 10,
      tFactoryLineY - 20,
      "runtimeText"
    );

    // Draw individual invocations lines
    for (let i = 0; i < numLines; i++) {
      var x1 = xScale(i);
      var x2 = xScale(i + 1) - runtimeRatio;
      var y = tFactoryLineY;
      var points = [
        [x1, y],
        [x2, y],
      ];

      drawLine(
        svg,
        points,
        "line",
        "tfactoryLine",
        strokeWidth,
        "url(#tFactoryTick)",
        "url(#arrowTFactory)",
        "none",
        tfactoryLineColor,
        false
      );
    }

    // Draw ellipses if more than 50 invocations.
    if (showSplit) {
      var rectWidth = (xScale(2) - xScale(1)) * 3 + 15;
      svg
        .append("rect")
        .attr("x", xScale(25))
        .attr("y", tFactoryLineY - 10)
        .attr("width", rectWidth)
        .attr("height", "20")
        .attr("fill", "#FFFFFF")
        .raise();

      var cx = xScale(25) + 15;
      var cy = tFactoryLineY;
      var radius = 4;
      drawEllipses(svg, cx, cy, radius, ellipsesColor);
    }
  }, [width, height]);

  return (
    <div>
      <div className="svg-container">
        <svg
          className="svg-element-flex"
          id="linechart"
          width={width}
          height={height}
        ></svg>
      </div>
    </div>
  );
}

export default LineChart;
