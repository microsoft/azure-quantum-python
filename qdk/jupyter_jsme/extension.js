// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

function jsmeOnLoad() {
    jsmeApp_ = new JSApplet.JSME("JSApp_", "400px", "350px", {
        "options" : "query,hydrogens",
        "smiles": ""
    });
}

function saveAs(var_name) {
    var molFile = jsmeApp_.molFile();
    var command = var_name + ' = """' + molFile + '"""';
    IPython.notebook.kernel.execute(command);
}
