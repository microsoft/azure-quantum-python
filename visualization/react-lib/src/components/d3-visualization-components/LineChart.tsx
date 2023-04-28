import * as React from "react";
import * as d3 from "d3";
import "./CSS/LineChart.css";

type Data = {
  title: string;
  legendTitle: string;
  value: number;
};

interface LineChartProps {
  data: Data[];
  lengthOuter: number;
  lengthInner: number;
  width : number;
  height: number;
  marginVal: number;
}

function LineChart({
  data,
lengthInner,
lengthOuter,
width,
height,
marginVal
}: LineChartProps) {
    React.useEffect(() => {
        var widthAdj = width - marginVal;
        var heightAdj = height - marginVal;
        const svg = d3.select("svg");

        svg.selectAll("*").remove();

        const range1 = [[0, 0], [lengthInner, 0]];
        const range2 = [[0,0], [lengthOuter, 0]];

    const dataArray = data.values;

    const color = d3.scaleOrdinal().domain(
        d3.extent(data, (d) => {
          return d.title;
        }) as unknown as string
      ).range(["#7FBBE9", "#EF6950", "#B7B8B9"]);

        const xScale = d3
        .scaleLinear()
        .domain([0, lengthOuter])
        .range([0, width]);

        const yScale = d3
        .scaleLinear()
        .domain([0, 20])
        .range([height, 0]);


        var line = d3.line()
        .x(function(d) { return xScale(d[0]); }) 
        .y(function(d) { return yScale(d[1]); }) 
        .curve(d3.curveMonotoneX)
        
        svg.append('g')
        .selectAll("dot")
        .data(range1)
        .enter()
        .append("rect")
        .attr("x", function (d) { return xScale(d[0]); } )
        .attr("y", function (d) { return yScale(d[1]); } )
        .attr("width", 5)
        .attr("height", 20)
        .attr("transform", "translate(" + 99 + "," + 90 + ")")
        .style("fill", "pink");

        svg.append("path")
        .datum(range1) 
        .attr("class", "line") 
        .attr("transform", "translate(" + 100 + "," + 100 + ")")
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", "#CC0000")
        .style("stroke-width", "2");

    }, [data, width, height]);

    return (
      <div className="svg-container">
        <svg className="svg-element" width={1000} height={1000} viewBox="-100 -100 1000 1000"></svg>
      </div>
    );

}

export default LineChart;