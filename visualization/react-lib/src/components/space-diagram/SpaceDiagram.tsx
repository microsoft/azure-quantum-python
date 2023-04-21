
import React from 'react';
import DonutChart from '../d3-visualization-components/DonutChart';

/*
export type SpaceDiagramProps = {
  physicalQubitsAlgorithm: number;
  physicalQubitsTFactory: number;
}*/

 //function SpaceDiagram({physicalQubitsAlgorithm, physicalQubitsTFactory}: SpaceDiagramProps): JSX.Element{
  function SpaceDiagram() {
  const data = [
    {title: 'Physical algorithmic qubits', value: 100},
    {title: 'Physical T-Factory qubits', value: 25}
  ];

  return (
    <div>
      <DonutChart data={data}  width={500} height={500} innerRadius = {100} outerRadius = {250} color="green" />
    </div>
  );
};

export default SpaceDiagram;

