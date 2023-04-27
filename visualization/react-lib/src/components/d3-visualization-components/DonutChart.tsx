import * as React from "react";
import * as d3 from "d3";
import { PieArcDatum } from "d3-shape";
import "./DonutChart.css";

type Data = {
  title: string;
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
  const [selectedSlice, setSelectedSlice] = React.useState(null);

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

    svg
      .append("text")
      .attr("x", "250")
      .attr("y", "0")
      .attr("text-anchor", "middle")
      .style("font-size", "18px")
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

    arcs.append("title").text((d) => `${d.data.title} : ${d.value}`);

    const legend = svg
      .selectAll(".legend")
      .data(data)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", (d, i) => `translate(0, ${i * 20})`);

    // add color squares to the legend
    legend
      .append("rect")
      .attr("x", 200)
      .attr("y", 500)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", (d, i) => color(d.title) as string);

    // add text to the legend
    legend
      .append("text")
      .attr("x", 225)
      .attr("y", 509)
      .attr("dy", ".35em")
      .style("text-anchor", "start")
      .text((d) => `${d.title} : ${d.value}`);
  }, [data, innerRadius, outerRadius]);

  return (
    <div className="svg--center">
      <svg width={width} height={height} viewBox="-35 -35 1000 1000"></svg>
    </div>
  );
}

export default DonutChart;
