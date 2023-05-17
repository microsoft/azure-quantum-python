import { SpaceDiagram } from "quantum-visualization/src";
import { TimeDiagram } from "quantum-visualization/src";

async function App(): Promise<JSX.Element> {
  var diagram = import.meta.env.VITE_DIAGRAM_TYPE;
  if (typeof diagram === "undefined" || diagram.length <= 0) {
    diagram = "spacediagram";
  }
  const diagramString = diagram.toLowerCase().replace(/\s/g, "");
  const dataResponse = await fetch("samplejobdata.json");
  const data = await dataResponse.text();

  if (diagramString === "spacediagram") {
    return (
      <div>
        <SpaceDiagram
          width={1000}
          height={1000}
          innerRadius={150}
          outerRadius={225}
          data={data}
        />
      </div>
    );
  } else {
    return (
      <div>
        <TimeDiagram width={1000} height={1000} data={data} />
      </div>
    );
  }
}

export default App;
