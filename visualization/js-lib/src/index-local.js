import * as React from "react";
import { createRoot } from 'react-dom/client';
import { SpaceDiagram, TimeDiagram } from "quantum-visualization";

class SpaceDiagramComponent extends HTMLElement {
  connectedCallback() {
    // TODO :we need to genarate a random id
    this.innerHTML = `<div id="space-diagram"> </div>`;
    const data = this.getAttribute("data");
    if (data) {
      const root = createRoot(
        document.getElementById('space-diagram')
      );
      root.render(<SpaceDiagram width={1000} height={1000} data={data} />);
    } else {
      console.error("Rendering error: Space Diagram requires data.");
    }
  }
}

class TimeDiagramComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<div id="time-diagram"> </div>`;
    const data = this.getAttribute("data");
    if (data) {
      const root = createRoot(
        document.getElementById('time-diagram')
      );
    

      root.render(<TimeDiagram data={data}  width={1000} height={1000}/>);
    } else {
      console.error("Rendering error: Time Diagram requires data.");
    }
  }
}

window.customElements.get("re-space-diagram") ||
window.customElements.define("re-space-diagram", SpaceDiagramComponent);

window.customElements.get("re-time-diagram") ||
window.customElements.define("re-time-diagram", TimeDiagramComponent);
