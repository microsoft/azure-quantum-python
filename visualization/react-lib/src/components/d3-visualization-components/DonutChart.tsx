import * as React from "react";
import * as d3 from "d3";
import { PieArcDatum } from "d3-shape";
import "./CSS/DonutChart.css";
import * as d3Format from "d3-format";
import * as d3Helper from "./D3HelperFunctions";
import "./CSS/Shared.css";

export type DonutChartProps = {
  data: d3Helper.LegendData[];
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
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
    const padAngle: number = 0.01;

    const translationValX: number = width / 4;
    const translationValY: number = height / 4;

    /* ------------------------------  Define styles from CSS ------------------------------ */
    const chartOpacity = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--chart-opacity");
    const chartHoverOpacity = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--chart-hover-opacity");

    const colors = getComputedStyle(document.documentElement).getPropertyValue(
      "--d3-colors"
    );

    /*------------------------------  Define color ranges  ------------------------------  */
    const colorArray = colors.split(",");
    const algorithmRunTimeColor = colorArray[1];
    const tfactoryLineColor = colorArray[0];

    var chartColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(data, (d) => {
          return d.legendTitle;
        }) as unknown as string
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
        `translate(${innerRadius + translationValX},${innerRadius + translationValY
        })`
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
            d.value
          )}`
      );

    /*------------------------------  Draw Legend ------------------------------  */
    var legendY = translationValY + outerRadius * 2 + 10;
    var midpoint = outerRadius + 10;
    d3Helper.drawLegend(
      svg,
      data,
      midpoint,
      legendY,
      translationValX,
      chartColor,
      true,
      false
    );

    /*------------------------------  Add text and titles  ------------------------------  */

    // Add chart title
    d3Helper.drawText(
      svg,
      "Space diagram",
      innerRadius + translationValX,
      translationValY - innerRadius,
      "title"
    );

    // Add middle text
    const totalQubits = d3.sum(data, (d) => d.value);
    const totalQubitsStr = d3Format.format(",.0f")(totalQubits);

    d3Helper.drawText(
      svg,
      donutMiddleTitle,
      innerRadius + translationValX,
      translationValY + innerRadius - 25,
      "donut-middle-title"
    );
    d3Helper.drawText(
      svg,
      totalQubitsStr,
      innerRadius + translationValX,
      translationValY + innerRadius + 25,
      "donut-middle-text"
    );
  }, [data, innerRadius, outerRadius]);

  return (
    <div className="donut-svg-container">
      <svg id="donutchart" width={width} height={height}></svg>
    </div>
  );
}

export default DonutChart;
