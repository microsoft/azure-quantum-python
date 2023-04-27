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

function OnClick(slice: Data) {
  // create a tooltip
  var Tooltip = d3
    .select("#div_template")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px");

  Tooltip.html("The exact value of<br>this cell is: " + slice.value)
    .style("left", d3.pointer(slice)[0] + 70 + "px")
    .style("top", d3.pointer(slice)[1] + "px");
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
      .range(d3.schemePastel1);

    const pieGenerator = d3
      .pie<Data>()
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
      .style("opacity", 0.8)
      .on("mouseover", (d, i) => {
        d3.select(`#tooltip-${i.index}`).style("visibility", "visible");
        d3.select(`#tooltiptext-${i.index}`).style("visibility", "visible");
      })
      .on("mouseout", (d, i) => {
        d3.select(`#tooltip-${i.index}`).style("visibility", "hidden");
        d3.select(`#tooltiptext-${i.index}`).style("visibility", "hidden");
      });

    arcs
      .append("text")
      .attr("transform", (d) => `translate(${arcGenerator.centroid(d)})`)
      .attr("text-anchor", "middle")
      .text((d) => d.data.value);

    data.forEach((item, i) => {
      arcs
        .append("rect")
        .attr("x", outerRadius - 50)
        .attr("y", -outerRadius + 30 * i)
        .attr("class", "tooltip")
        .attr("id", `tooltip-${i}`)
        .attr("width", 200)
        .attr("height", 20)
        .attr("opacity", 0.9)
        .style("visibility", "hidden");
    });
  }, [data, innerRadius, outerRadius]);

  return (
    <div>
      <svg width={width} height={height} className="donut-chart"></svg>
    </div>
  );
}

export default DonutChart;
