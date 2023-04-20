
import React from 'react';
import DonutChart from '../d3-visualization-components/DonutChart';

type SpaceDiagramProps = {
  physicalQubitsAlgorithm: number,
  physicalQubitsTFactory: number
}
function SpaceDiagram({physicalQubitsAlgorithm, physicalQubitsTFactory}: SpaceDiagramProps){
 
  const data = [
    {title: 'Physical algorithmic qubits', value: physicalQubitsAlgorithm},
    {title: 'Physical T-Factory qubits', value: physicalQubitsTFactory}
  ];

  return (
    <div>
      <DonutChart data={data}  width={500} height={500} innerRadius = {100} outerRadius = {250} color="green" />
    </div>
  );
};

export default SpaceDiagram;
