import { SpaceDiagram } from "quantum-visualization/src";

async function App(): Promise<JSX.Element> {
  const dataResponse = await fetch("samplejobdata.json");
  const data = await dataResponse.text();
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
}

export default App;
