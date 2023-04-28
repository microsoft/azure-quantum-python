import React from "react";
import LineChart from "../d3-visualization-components/LineChart";
/*
export type SpaceDiagramProps = {
  physicalQubitsAlgorithm: number;
  physicalQubitsTFactory: number;
}*/

//function SpaceDiagram({physicalQubitsAlgorithm, physicalQubitsTFactory}: SpaceDiagramProps): JSX.Element{
function TimeDiagram() {
  const data = [{ title: "Number of t-states", value: 17, legendTitle: "Single T-factory invocation runtime" },
    { title: "Time", value: 180, legendTitle: "Time"},
    { title: "Algorithm runtime", value: 180, legendTitle: "Algorithm runtime"}
  ];
return (
    <div>
      <LineChart
        data={data}
        lengthInner={100}
        lengthOuter={15}
        width = {100}
        height = {100}
        marginVal = {20}
      />
    </div>
  );
}

export default TimeDiagram;
