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
}

function DonutChart({
  data,
  width,
  height,
  innerRadius,
  outerRadius,
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
    const chartColor = d3
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

    const legendColor = d3
      .scaleOrdinal()
      .domain(
        d3.extent(data, (d) => {
          return d.title;
        }) as unknown as string
      )
      .range(
        getComputedStyle(document.documentElement)
          .getPropertyValue("--d3-colors-legend")
          .split(", ")
      );

    // Add chart title
    svg
      .append("text")
      .attr("x", outerRadius)
      .attr("y", "-60")
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
      .attr("transform", `translate(${outerRadius + 60},${outerRadius + 50})`);

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

    //consider: https://stackoverflow.com/questions/24827589/d3-appending-html-to-nodes

    // Create legend
    const legend = svg
      .selectAll(".legend")
      .data(data)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", (d, i) => `translate(${i * innerRadius}, 0)`);

    legend
      .append("rect")
      .attr("x", 100)
      .attr("y", 500)
      .attr("width", 5)
      .attr("height", 45)
      .style("fill", (d, i) => legendColor(d.title) as string);

    // add text to the legend
    legend
      .append("text")
      .attr("x", 120)
      .attr("y", 508)
      .text((d) => legendTitlePreText)
      .attr("class", "legend")
      .attr("transform", (d, i) => `translate(${i}, 0)`);

    legend
      .append("text")
      .attr("x", 120)
      .attr("y", 520)
      .text((d) => `${d.legendTitle}`)
      .attr("class", "legend-maintext")
      .attr("transform", (d, i) => `translate(${i}, 0)`);

    legend
      .append("text")
      .attr("x", 120)
      .attr("y", 544)
      .text((d) => `${d.value.toLocaleString("en-US")}`)
      .attr("class", "legend-values")
      .attr("transform", (d, i) => `translate(${i}, 0)`);

    // Add total qubits and title to the middle of the donut chart
    const total = d3.sum(data, (d) => d.value).toLocaleString("en-US");

    svg
      .append("text")
      .attr("x", outerRadius)
      .attr("y", outerRadius - 20)
      .text(donutMiddleTitle)
      .attr("class", "donut-middle-title");

    svg
      .append("text")
      .attr("x", outerRadius)
      .attr("y", outerRadius + 35)
      .text(`${total}`)
      .attr("class", "donut-middle-text");
  }, [data, innerRadius, outerRadius]);

  return (
    <div className="svg-container">
      <svg className="svg-element" width={width} height={height}></svg>
    </div>
  );
}

export default DonutChart;
