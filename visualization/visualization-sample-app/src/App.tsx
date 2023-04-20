import './App.css';
import Loaders from 'module'
import {SpaceDiagram} from 'quantum-visualization/src'

function App() {
  return (
    <div className="App">
    <SpaceDiagram physicalQubitsAlgorithm={100} physicalQubitsTFactory={150} />
    </div>
  );
}

export default App;
