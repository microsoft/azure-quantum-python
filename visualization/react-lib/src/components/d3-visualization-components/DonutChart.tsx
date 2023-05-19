import * as React from "react";
import * as d3 from "d3";
import { PieArcDatum } from "d3-shape";
import "./CSS/DonutChart.css";

type Data = {
  title: string;
  legendTitle: string;
  value: number;
};

interface DonutChartProps {
  data: Data[];
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
  translationValX: number;
  translationValY: number;
}

function DonutChart({
  data,
  width,
  height,
  innerRadius,
  outerRadius,
  translationValX,
  translationValY,
}: DonutChartProps) {
  React.useEffect(() => {
    const svg = d3.select("svg");
    svg.selectAll("*").remove();

    // Define constants
    const innerRadiusHover = innerRadius;
    const outerRadiusHover = outerRadius + 25;
    const donutMiddleTitle = "Total physical qubits";
    const legendTitlePreText = "Physical";
    const padAngle = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--pad-angle");

    const chartOpacity = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--chart-opacity");
    const chartHoverOpacity = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--chart-hover-opacity");

    // Define chart and legend color ranges.
    var chartColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(data, (d) => {
          return d.title;
        }) as unknown as string
      )
      .range(
        getComputedStyle(document.documentElement)
          .getPropertyValue("--d3-colors")
          .split(", ")
      );

    // Add chart title
    svg
      .append("text")
      .attr("x", innerRadius + translationValX)
      .attr("y",  translationValY - innerRadius)
      .attr("class", "title")
      .text("Space diagram");

    // Create pie and arc generators
    const pieGenerator = d3
      .pie<Data>()
      .padAngle(padAngle)
      .value((d) => d.value)
      .sort(null);

    const arcGenerator = d3
      .arc<PieArcDatum<Data>>()
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
        `translate(${innerRadius + translationValX},${
          innerRadius + translationValY
        })`
      );

    // Fill donut chart, apply hover.
    arcs
      .append("path")
      .attr("d", arcGenerator)
      .attr("fill", (d) => {
        return chartColor(d.data.title) as string;
      })
      .style("opacity", chartOpacity)
      .on("mouseover", (d) => {
        const arcHover = d3
          .arc<PieArcDatum<Data>>()
          .innerRadius(innerRadiusHover)
          .outerRadius(outerRadiusHover);
        d3.select(d.target).attr("d", arcHover);
        d3.select(d.target).style("opacity", chartHoverOpacity);
      })
      .on("mouseout", (d) => {
        d3.select(d.target).attr("d", arcGenerator);
        d3.select(d.target).style("opacity", chartOpacity);
      });

    // Add tooltips
    arcs
      .append("title")
      .text((d) => `${d.data.title} : ${d.value.toLocaleString("en-us")}`);

    // Create legend
    const legend = svg
      .selectAll(".legend")
      .data(data)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr(
        "transform",
        (d, i) =>
          `translate(${i * translationValX}, ${translationValY})`
      );

    legend
      .append("rect")
      .attr("width", 20)
      .attr("height", 20)
      .attr("x", translationValX - 30).attr("y", translationValY  + outerRadius + 10)
      .style("fill", (d, i) => chartColor(d.title) as string);

    // add text to the legend
    legend
      .append("text")
      .text((d) => legendTitlePreText)
      .attr("class", "legend")
      .attr("x", 0).attr("y", translationValY  + outerRadius)
      .attr("transform", (d, i) => `translate(${translationValX}, 0)`);

    legend
      .append("text")
      .attr("x", 0).attr("y", translationValY  + outerRadius + 15)
      .text((d) => `${d.legendTitle}`)
      .attr("class", "legend-maintext")
      .attr("transform", (d, i) => `translate(${translationValX}, 0)`);

    legend
      .append("text")
      .attr("x", 0).attr("y", translationValY  + outerRadius + 45)
      .text((d) => `${d.value.toLocaleString("en-US")}`)
      .attr("class", "legend-values")
      .attr("transform", (d, i) => `translate(${translationValX}, 0)`);

    // Add total qubits and title to the middle of the donut chart
    const total = d3.sum(data, (d) => d.value).toLocaleString("en-US");

    svg
      .append("text")
      .text(donutMiddleTitle)
      .attr("class", "donut-middle-title")
      .attr(
        "transform",
        `translate(${innerRadius + translationValX},${
         translationValY  + innerRadius - 25
        })`
      );

    svg
      .append("text")
      .text(`${total}`)
      .attr("class", "donut-middle-text")
      .attr(
        "transform",
        `translate(${innerRadius + translationValX},${
          innerRadius + translationValY + 25
        })`
      );

  }, [data, innerRadius, outerRadius]);

  return (
    <div className="svg-container">
      <svg  width={width} height={height}></svg>
    </div>
  );
}

export default DonutChart;
