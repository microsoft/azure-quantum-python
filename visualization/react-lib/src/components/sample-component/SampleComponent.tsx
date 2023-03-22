
import React from "react";
import "./SampleComponent.css";

function SampleComponent({ label, type = "text" }: {label: string, type: string}) {
    return (
        <div className="simple-form-group">
            {label && <label className="simple-text-label">{label}</label>}
            <input
                type={type}
                className="simple-text-input"
            />
        </div>
    );
}

export default SampleComponent;