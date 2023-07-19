import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";
import * as d3Format from 'd3-format';

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
function drawTFactoryLines(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, numLines: number, tFactoryXScale: Function,
  chartStartX: number, tFactoryLineY: number, strokeWidth: string, tfactoryLineColor: string, startVal: number) {
  for (let i = startVal; i < numLines; i++) {
    var x1 = tFactoryXScale(i) + chartStartX;
    var x2 = (tFactoryXScale(i + 1)) + chartStartX;
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
}
function drawEllipses(
  svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>,
  cx: number,
  cy: number,
  spaceBetween: number,
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
  chartStartX: number,
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
      (d, i) => `translate(${(midpoint * i + chartStartX)}, ${chartBottomY})`);

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
    const algorithmRuntime: number = chartData["algorithmRuntime"]
    const tFactoryRuntime: number = chartData["tFactoryRuntime"];
    const algorithmRuntimeFormatted: string =
      chartData["algorithmRuntimeFormatted"];
    const tFactoryRuntimeFormatted: string =
      chartData["tFactoryRuntimeFormatted"];

    /* Define chart constants */
    const numTStatesString: string = d3Format.format(',.0f')(numberTStates);

    const tfactoryLineLabel: string =
      numTStatesString +
      (numberTStates == 1
        ? " T state produced after  each invocation's runtime".split('  ').join('\n')
        : " T states produced after asdfdsf  each invocation's runtime").split('  ').join('\n');

    /* Define chart dimensions */
    const chartStartY = 0.6 * height;
    const verticalLineSpacingDist = 0.15 * height;
    const xAxisLength = 0.85 * width;
    const chartStartX = 0.05 * width;
    const chartLength = xAxisLength - (xAxisLength * 0.15)
    const midpoint = xAxisLength / 2;
    const algorithmLineY = chartStartY - verticalLineSpacingDist;
    const tFactoryLineY = chartStartY - verticalLineSpacingDist * 2;

    /* Define chart length ratios */
    const minAlgorithmLineLength = xAxisLength * 0.05;
    const minTFactoryInvocationLength = xAxisLength * 0.015;
    var lengthAlgorithmLine = chartLength;
    var lengthTFactoryLine = chartLength;
    var runtimeRatio = 1;

    var totalTFactoryRuntime = numberTFactoryInvocations * tFactoryRuntime;

    if (algorithmRuntime > totalTFactoryRuntime) {
      // Algorithm is longer.
      runtimeRatio = totalTFactoryRuntime / algorithmRuntime;
      lengthTFactoryLine = runtimeRatio * chartLength;
    } else if (algorithmRuntime < totalTFactoryRuntime) {
      // Algorithm shouldn't be shorter, but if it is, handle appropriately.
      runtimeRatio = algorithmRuntime / totalTFactoryRuntime;
      lengthAlgorithmLine = runtimeRatio * chartLength;
    }
    if (lengthAlgorithmLine < minAlgorithmLineLength) {
      lengthAlgorithmLine = minAlgorithmLineLength;
    }

    /* Draw Timeline */
    const timeLine = [
      [chartStartX, chartStartY],
      [chartStartX + xAxisLength, chartStartY],
    ];

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
    drawText(svg, "Time", xAxisLength + chartStartX + 5, chartStartY, "time");

    /* Draw Chart Title and Legend */

    // Add chart title
    drawText(
      svg,
      "Time diagram",
      midpoint,
      chartStartY - verticalLineSpacingDist * 3,
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
      chartStartY,
      chartStartX,
      legendColor
    );

    /* Draw Algorithm line */
    const algorithmRunTimeLine = [
      [chartStartX, algorithmLineY],
      [chartStartX + lengthAlgorithmLine, algorithmLineY],
    ];

    var algorithmDashedLineStart = lengthAlgorithmLine + 5;
    var algorithmTextY = chartStartY - 10;

    const algorithmDashedLine = [
      [chartStartX + algorithmDashedLineStart, chartStartY],
      [chartStartX + algorithmDashedLineStart, algorithmLineY],
    ];

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

    // Append runtime text
    drawText(
      svg,
      algorithmRuntimeFormatted,
      lengthAlgorithmLine + chartStartX + 10,
      algorithmTextY,
      "runtimeText"
    );

    /* Define t-factory xScale and line points */
    var numLines = numberTFactoryInvocations;

    // If more t-factory invocations than 50, set showSplit variable to insert ellipses.
    const showSplit = numLines > 50;
    if (showSplit) {
      numLines = 56;
    }

    if ((lengthTFactoryLine / numLines) < minTFactoryInvocationLength) {
      lengthTFactoryLine = minTFactoryInvocationLength * numLines;
    }

    // define the x scaling for T factory invocation length
    const tFactoryXScale = d3
      .scaleLinear()
      .domain([0, numLines])
      .range([0, lengthTFactoryLine]);

    // length of 1 t-factory invocation
    var tFactoryRefX = tFactoryXScale(1);

    var tFactoryDashedLine = [
      [chartStartX + tFactoryRefX + 5, chartStartY],
      [chartStartX + tFactoryRefX + 5, tFactoryLineY],
    ];

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
      tFactoryRefX + chartStartX + 5,
      chartStartY + 20,
      "runtimeText"
    );

    // Append t-factory line label
    drawText(
      svg,
      tfactoryLineLabel,
      tFactoryRefX + chartStartX + 10,
      tFactoryLineY + 30,
      "runtimeText"
    );

    const numberTFactoryInvocationsStr: string = d3Format.format(',.0f')(numberTFactoryInvocations)
    var numberTFactoryInvocationsText =
      numberTFactoryInvocationsStr +
      (numberTFactoryInvocations == 1
        ? " T factory invocation"
        : " T factory invocations");

    drawText(
      svg,
      numberTFactoryInvocationsText,
      tFactoryRefX + chartStartX + 10,
      tFactoryLineY - 20,
      "runtimeText"
    );

    // Draw individual invocations lines
    if (!showSplit) {
      drawTFactoryLines(svg, numLines, tFactoryXScale, chartStartX, tFactoryLineY, strokeWidth, tfactoryLineColor, 0);
    }
    else {
      // draw first 25 segments
      numLines = 25;
      drawTFactoryLines(svg, numLines, tFactoryXScale, chartStartX, tFactoryLineY, strokeWidth, tfactoryLineColor, 0);

      // draw ellipses in middle
      var cx = tFactoryXScale(26) + chartStartX;
      var cy = tFactoryLineY;
      var radius = tFactoryXScale(1) / 4;
      var spaceBetween = tFactoryXScale(1);
      drawEllipses(svg, cx, cy, spaceBetween, radius, ellipsesColor);

      // draw last 25 segments
      numLines = 54;
      drawTFactoryLines(svg, numLines, tFactoryXScale, chartStartX, tFactoryLineY, strokeWidth, tfactoryLineColor, 29);
    }

  }, [width, height]);

  return (
    <div>
      <div className="line-svg-container">
        <svg
          id="linechart"
          width={width}
          height={height}
        ></svg>
      </div>
    </div >
  );
}

export default LineChart;
