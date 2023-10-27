/*------------------------------------
  Copyright (c) Microsoft Corporation.
  Licensed under the MIT License.
  All rights reserved.
------------------------------------ */
import * as React from "react";
import { createRoot } from 'react-dom/client';
import { SpaceDiagram, TimeDiagram } from "quantum-visualization";
import { initializeIcons } from '@fluentui/react/lib/Icons';

initializeIcons();

const randomId = () => {
  return Math.random().toString(36).substring(7);
};

class SpaceDiagramComponent extends HTMLElement {
  connectedCallback() {
    const divId = "space-diagram-" + randomId();
    this.innerHTML = `<div id=${divId}> </div>`;
    const data = this.getAttribute("data");
    if (data) {
      const root = createRoot(
        document.getElementById(divId)
      );
      root.render(<SpaceDiagram data={data}/>);
    } else {
      console.error("Rendering error: Space Diagram requires data.");
    }
  }
}

class TimeDiagramComponent extends HTMLElement {
  connectedCallback() {
    const divId = "time-diagram-" + randomId();
    this.innerHTML = `<div id=${divId}> </div>`;
    const data = this.getAttribute("data");
    if (data) {
      const root = createRoot(
        document.getElementById(divId)
      );

      root.render(<TimeDiagram data={data}/>);
    } else {
      console.error("Rendering error: Time Diagram requires data.");
    }
  }
}

window.customElements.get("re-space-diagram") ||
window.customElements.define("re-space-diagram", SpaceDiagramComponent);

window.customElements.get("re-time-diagram") ||
window.customElements.define("re-time-diagram", TimeDiagramComponent);
