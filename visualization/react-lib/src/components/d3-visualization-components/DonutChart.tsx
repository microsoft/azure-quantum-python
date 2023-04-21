import * as React from 'react';
import * as d3 from 'd3';
import { PieArcDatum } from 'd3-shape';

type  Data = {
  title: string;
  value: number;
}

interface DonutChartProps {
  data: Data[];
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
}

function DonutChart({data, width, height, innerRadius, outerRadius} : DonutChartProps) {

  // create a ref to store the chart
  const donutRef = React.useRef(null)

  // create a function to draw the chart
  const drawChart = () => {
    // access the chart ref
    const chart = donutRef.current;
    if (!chart) return;

    // define the pie generator
    const pie = d3.pie<Data>()
      .value((d: any) => d.value)
      .sort(null);

      const color = d3
      .scaleOrdinal()
      .domain(
        (d3.extent(data, (d) => {
          return d.title
        }) as unknown) as string
      )
      .range(d3.schemePastel1)

    const path = d3.arc<PieArcDatum<Data>>().innerRadius(innerRadius).outerRadius(outerRadius);
   
    const svg = d3.select(donutRef.current)
      .append("svg")
      .attr("width", width)
    .attr("height", height);

    const arcs = svg.selectAll('.arc')
      .data(pie(data))
      .enter()
      .append("g")
      .attr("class", "arc")
      .attr("transform", `translate(${outerRadius},${outerRadius})`);
    
      arcs.append('path')
      .attr("d", path)
      .attr("fill",  (d) => {
        return color(d.data.title) as string
      })

    arcs.on("mouseover", function(d) {
      d3.select(this)
        .style("fill", "orange");
      svg.append("text")
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .attr("class", "tooltip")
        .text(d.data);
    });

    arcs.on("mouseout", function(d) {
      d3.select(this)
        .style("fill",  "green")
      d3.select(".tooltip").remove();
    });
  
}



  // useEffect to draw the chart
  React.useEffect(() => {
    drawChart();
  }, [data, width, height, innerRadius, outerRadius]);

  // render the chart
  return <g ref={donutRef} />;
};

export default DonutChart;