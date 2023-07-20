import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";
import * as d3Format from 'd3-format';
import * as d3Helper from "./D3HelperFunctions";
import "./CSS/Shared.css";

export type LineChartProps = {
  legendData: d3Helper.LegendData[];
  chartData: { [key: string]: any };
  width: number;
  height: number;
};

/* Helper Functions */
function drawChartVerticalLine(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, startX: number, startY: number, textStartY: number, length: number, lineColor: string, strokeWidth: string, id: string, label: string) {

  const dashedVerticalLinePoints = [
    [startX, startY],
    [startX, length],
  ];

  d3Helper.drawCircleMarkers(
    svg,
    10,
    10,
    lineColor,
    1.5,
    5,
    5,
    5,
    5,
    "circleMarker"
  );

  d3Helper.drawLine(
    svg,
    dashedVerticalLinePoints,
    "line",
    id + "dashedLine",
    strokeWidth,
    "url(#circleMarker)",
    "url(#circleMarker)",
    "none",
    lineColor,
    true
  );

  // Append runtime text
  d3Helper.drawText(
    svg,
    label,
    startX + 10,
    textStartY,
    "runtimeText"
  );
}
function drawChartHorizontalLine(svg: d3.Selection<d3.BaseType, unknown, HTMLElement, any>, startX: number, startY: number, length: number, lineColor: string, strokeWidth: string, id: string, label: string) {
  const linePoints = [
    [startX, startY],
    [startX + length, startY],
  ];

  // Create start bar
  var lineTickId = id + "Tick";
  d3Helper.drawLineTick(svg, 1, 10, lineColor, lineTickId);
  // Create end arrow
  var arrowId = id + "Arrow";
  d3Helper.drawArrow(svg, lineColor, arrowId);

  // Draw line
  d3Helper.drawLine(
    svg,
    linePoints,
    "line",
    id + "line",
    strokeWidth,
    "url(#" + lineTickId + ")",
    "url(#" + arrowId + ")",
    lineColor,
    lineColor,
    false
  );

  // Append text labels to  line if applicable.
  if (label != null || label != "") {
    d3Helper.drawText(svg, label, startX + length + 5, startY, "lineLabel");
  }
}
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

    d3Helper.drawLine(
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

/* Line Chart Component */
function LineChart({ legendData, chartData, width, height }: LineChartProps) {
  React.useEffect(() => {
    /* ------------------------------------------------------------ Set up and define constants ------------------------------------------------------------  */
    const svg = d3.select("#linechart");
    svg.selectAll("*").remove();

    /* ------------------------------  Define styles from CSS ------------------------------ */
    const colors = getComputedStyle(document.documentElement).getPropertyValue(
      "--d3-colors"
    );
    const strokeWidth = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--stroke-width");

    const colorArray = colors.split(",");
    const algorithmRunTimeColor = colorArray[1];
    const tfactoryLineColor = colorArray[0];
    const ellipsesColor = colorArray[2];
    const timeLineColor = colorArray[3];

    /*------------------------------  Define chart data from dictionary ------------------------------  */
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
        ? " T state produced after each invocation's runtime"
        : " T states produced after each invocation's runtime");

    /* ------------------------------  Define chart dimensions ------------------------------ */
    const chartStartY = 0.6 * height;
    const verticalLineSpacingDist = 0.15 * height;
    const xAxisLength = 0.85 * width;
    const chartStartX = 0.05 * width;
    const chartLength = xAxisLength - (xAxisLength * 0.15)
    const midpoint = xAxisLength / 2;
    const algorithmLineY = chartStartY - verticalLineSpacingDist;
    const tFactoryLineY = chartStartY - verticalLineSpacingDist * 2;

    /* ------------------------------  Define chart length ratios ------------------------------ */
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

    /* ------------------------------------------------------------ Begin draw chart ------------------------------------------------------------  */

    /* ------------------------------ Draw Chart Title and Legend ------------------------------ */

    // Add chart title
    d3Helper.drawText(
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

    d3Helper.drawLegend(
      svg,
      legendData,
      midpoint,
      chartStartY,
      chartStartX,
      legendColor,
      false,
      true
    );

    /* ------------------------------ Draw Timeline ------------------------------ */
    drawChartHorizontalLine(svg, chartStartX, chartStartY, xAxisLength, timeLineColor, strokeWidth, "time", "Time");

    /*------------------------------  Draw Algorithm lines------------------------------  */
    drawChartHorizontalLine(svg, chartStartX, algorithmLineY, lengthAlgorithmLine, algorithmRunTimeColor, strokeWidth, "algorithm", "");
    var algorithmDashedLineStart = lengthAlgorithmLine + 5 + chartStartX;
    var textStartAlgorithmY = chartStartY - 10;
    drawChartVerticalLine(svg, algorithmDashedLineStart, chartStartY, textStartAlgorithmY, algorithmLineY, timeLineColor, strokeWidth, "algorithm", algorithmRuntimeFormatted);

    /* ------------------------------ Draw T factory lines and labels ------------------------------ */

    // Define T factory xScale and number of lines
    var numLines = numberTFactoryInvocations;

    // If more T factory invocations than 50, set showSplit variable to insert ellipses.
    const showSplit = numLines > 50;
    if (showSplit) {
      numLines = 56;
    }

    if ((lengthTFactoryLine / numLines) < minTFactoryInvocationLength) {
      lengthTFactoryLine = minTFactoryInvocationLength * numLines;
    }

    // Define the x scaling for T factory invocation length.
    const tFactoryXScale = d3
      .scaleLinear()
      .domain([0, numLines])
      .range([0, lengthTFactoryLine]);

    // Length of 1 T factory invocation line segement.
    var tFactoryRefX = tFactoryXScale(1);

    // Create T factory start bar.
    d3Helper.drawLineTick(svg, 1, 6, tfactoryLineColor, "tFactoryTick");

    // Create tfactory end arrow
    d3Helper.drawArrow(svg, tfactoryLineColor, "arrowTFactory");

    // Draw dashed line of single T factory invocation runtime.
    var tFactoryDashedLineStartX = chartStartX + tFactoryRefX + 5;
    var textStartTFactoryY = chartStartY + 20;
    drawChartVerticalLine(svg, tFactoryDashedLineStartX, chartStartY, textStartTFactoryY, tFactoryLineY, timeLineColor, strokeWidth, "tfactory", tFactoryRuntimeFormatted);

    // Append T factory line labels.
    d3Helper.drawText(
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

    d3Helper.drawText(
      svg,
      numberTFactoryInvocationsText,
      tFactoryRefX + chartStartX + 10,
      tFactoryLineY - 20,
      "runtimeText"
    );

    /* ------------------------------ Draw T factory main line ------------------------------ */
    // Draw individual invocations lines.
    if (!showSplit) {
      drawTFactoryLines(svg, numLines, tFactoryXScale, chartStartX, tFactoryLineY, strokeWidth, tfactoryLineColor, 0);
    }
    else {
      // Draw first 25 segments.
      numLines = 25;
      drawTFactoryLines(svg, numLines, tFactoryXScale, chartStartX, tFactoryLineY, strokeWidth, tfactoryLineColor, 0);

      // Draw ellipses in middle.
      var cx = tFactoryXScale(26) + chartStartX;
      var cy = tFactoryLineY;
      var radius = tFactoryXScale(1) / 4;
      var spaceBetween = tFactoryXScale(1);
      d3Helper.drawEllipses(svg, cx, cy, spaceBetween, radius, ellipsesColor);

      // Draw last 25 segments.
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
