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

    const color = d3
      .scaleOrdinal()
      .domain(
        d3.extent(data, (d) => {
          return d.title;
        }) as unknown as string
      )
      .range(["#0078D4", "#EF6950", "#B7B8B9"]);

    const legendColor = d3.scaleOrdinal().domain(
      d3.extent(data, (d) => {
        return d.title;
      }) as unknown as string
    ).range(["#7FBBE9", "#EF6950", "#B7B8B9"]);

    svg
      .append("text")
      .attr("x", "225")
      .attr("y", "-60")
      .attr("text-anchor", "middle")
      .attr("class", "title")
      .text("Space diagram");

    const pieGenerator = d3
      .pie<Data>()
      .padAngle(0.01)
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
      .attr("transform", `translate(${outerRadius},${outerRadius})`);

    arcs
      .append("path")
      .attr("d", arcGenerator)
      .attr("fill", (d) => {
        return color(d.data.title) as string;
      })
      .style("opacity", 0.5)
      .on("mouseover", (d) => {
        const arcHover = d3
          .arc<PieArcDatum<Data>>()
          .innerRadius(150)
          .outerRadius(250);
        d3.select(d.target).attr("d", arcHover);
        d3.select(d.target).style("opacity", 0.65);
      })
      .on("mouseout", (d) => {
        d3.select(d.target).attr("d", arcGenerator);
        d3.select(d.target).style("opacity", 0.5);
      });

    arcs.append("title").text((d) => `${d.data.title} : ${d.value.toLocaleString("en-us")}`);

    const legend = svg
      .selectAll(".legend")
      .data(data)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", (d, i) => `translate(${i * 150}, 0)`);

    legend
      .append("rect")
      .attr("x", 110)
      .attr("y", 500)
      .attr("width", 5)
      .attr("height", 45)
      .style("fill", (d, i) => legendColor(d.title) as string);


    legend.append("text")
      .attr("x", 120)
      .attr("y", 508)
      .text((d) => "Physical")
      .style("font-size", "10px")
      .style("font-family", "Segoe UI")
      .style("line-height", "14px")
      .style("fill", "black")
      .style("font-weight", "600")
      .style("font-style", "normal")
      .attr("transform", (d, i) => `translate(${i}, 0)`);


    // add text to the legend
    legend.append("text")
      .attr("x", 120)
      .attr("y", 520)
      .text((d) => `${d.legendTitle}`)
      .style("font-size", "10px")
      .style("fill", "#000000")
      .style("font-family", "Segoe UI")
      .style("line-height", "14px")
      .style("font-weight", "400")
      .style("font-style", "normal")
      .attr("transform", (d, i) => `translate(${i}, 0)`);


    legend.append("text")
      .attr("x", 120)
      .attr("y", 544)
      .text((d) => `${d.value.toLocaleString("en-US")}`)
      .style("font-size", "24px")
      .style("font-family", "Segoe UI")
      .style("line-height", "32px")
      .style("fill", "#24272B")
      .style("font-style", "normal")
      .style("font-weight", "600")
      .attr("transform", (d, i) => `translate(${i}, 0)`);


    const total = d3.sum(data, (d) => d.value).toLocaleString("en-US");


    svg.append("text")
      .attr("x", outerRadius)
      .attr("y", outerRadius - 20)
      .text(`Total physical qubits`)
      .style("font-size", "16px")
      .style("fill", "#323130")
      .style("font-weight", "400")
      .style("font-style", "normal")
      .attr("text-anchor", "middle")
      .style("font-family", "Segoe UI")
      .style("line-height", "21px");


    svg.append("text")
      .attr("x", outerRadius)
      .attr("y", outerRadius + 35)
      .text(`${total}`)
      .style("font-size", "55px")
      .style("fill", "#323130")
      .style("font-weight", "400")
      .style("font-style", "normal")
      .attr("text-anchor", "middle")
      .style("font-family", "Segoe UI")
      .style("line-height", "73px");


  }, [data, innerRadius, outerRadius]);

  return (
    <div className="svg-container">
      <svg className="svg-element" width={width} height={height} viewBox="-100 -100 1000 1000"></svg>
    </div>
  );
}

export default DonutChart;
