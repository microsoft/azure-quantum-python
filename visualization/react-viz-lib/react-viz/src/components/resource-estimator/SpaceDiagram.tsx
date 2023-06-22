import { SpaceChart } from "../space-chart";
import TableComponent from "../table/Table";
import { TableData } from "../table/Table";
import { JobResults } from "../../models/JobResults";
import "./Diagram.css";

interface SpaceDiagramProps {
  width: number;
  height: number;
  innerRadius: number;
  outerRadius: number;
  data: string;
}

function SpaceDiagram({
  width,
  height,
  innerRadius = 150,
  outerRadius = 225,
  data,
}: SpaceDiagramProps) {
  let jobResults = JSON.parse(data) as JobResults;

  const physicalQubitsAlgorithm =
    jobResults.physicalCounts.breakdown.physicalQubitsForAlgorithm;
  const physicalQubitsTFactory =
    jobResults.physicalCounts.breakdown.physicalQubitsForTfactories;

  const numTFactories = jobResults.physicalCounts.breakdown.numTfactories;
  const numQubitsPerTFactory = Math.round(
    physicalQubitsTFactory / numTFactories
  );

  const tableDictionary: {
    [name: string]: {
      type: number;
      description?: string;
      value?: string;
    };
  } = {
    "Physical resource estimates": { type: 0 },
    "Total physical qubits": {
      type: 1,
      description:
        "Total physical qubits required for algorithm and T factories.",
      value: jobResults.physicalCounts.physicalQubits.toString(),
    },
    "T factory parameters": { type: 0 },
    "Physical T factory qubits": {
      type: 1,
      description: "Number of physical qubits for the T factories.",
      value: physicalQubitsTFactory.toString(),
    },
    "Resource estimation breakdown": { type: 0 },
    "Number of T factory copies": {
      type: 1,
      description:
        "Number of T factories capable of producing the demanded T states during the algorithm's runtime.",
      value: numTFactories.toString(),
    },
    "Physical qubits for single T factory": {
      type: 1,
      value: numQubitsPerTFactory.toString(),
    },
    "Physical algorithmic qubits": {
      type: 1,
      description: "Number of logical qubits for the algorithm after layout.",
      value: physicalQubitsAlgorithm.toString(),
    },
    "Logical algorithmic qubits": {
      type: 1,
      description: "Number of logical qubits for the algorithm after layout.",
      value:
        jobResults.physicalCounts.breakdown.algorithmicLogicalQubits.toString(),
    },
    "Logical qubit parameters": { type: 0 },
    "Physical qubits": {
      type: 1,
      description: "Number of physical qubits per logical qubit.",
      value: jobResults.logicalQubit.physicalQubits.toString(),
    },
  };

  const tableDataArray: TableData[] = Object.keys(tableDictionary).map(
    (key, i) => {
      return {
        id: i.toString(),
        name: key,
        type: tableDictionary[key].type,
        value: tableDictionary[key].value,
        description: tableDictionary[key].description,
      };
    }
  );

  return (
    <div className="grid-container">
      <div className="diagram">
        <SpaceChart
          physicalQubitsAlgorithm={physicalQubitsAlgorithm}
          physicalQubitsTFactory={physicalQubitsTFactory}
          width={width}
          height={height}
          innerRadius={innerRadius}
          outerRadius={outerRadius}
        />
      </div>
      <div className="table">
        <TableComponent nodes={tableDataArray} width={width} height={height} />
      </div>
    </div>
  );
}

export default SpaceDiagram;