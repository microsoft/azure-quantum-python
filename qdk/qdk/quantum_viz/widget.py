# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Module for Jupyter Widget that displays the quantum-viz circuit visualizer
"""
import uuid

from notebook.nbextensions import check_nbextension
from varname import varname, VarnameRetrievingError
from IPython.core.display import display, HTML

# Rel file path for Javascript source
JS_SOURCE = "qviz.min"

# Base URL for widget source javascript
BASE_URL = "/nbextensions/jupyter_qviz"

if check_nbextension("quantum_viz") is False:
    # Fallback option in case user didn't install Jupyter extension
    BASE_URL = "https://unpkg.com/@microsoft/quantum-viz.js@1.0.2/dist"

_HTML_STR_FORMAT = '''
<script type="text/javascript">
require.config({{
    paths: {{
        qviz: '{base_url}/{js_source}'
    }}
}});

require(['qviz'], function(qviz) {{
    function renderQuantumProgram(program) {{
        const targetDiv = document.getElementById('JSApp_{uid}');
        if (targetDiv != null) {{
            qviz.draw(program, targetDiv, qviz.STYLES['Default']);
        }}
    }}
    const data = {data};
    renderQuantumProgram(data);
}});
</script>
<div id="JSApp_{uid}"></div>
<div id="msg"></div>
'''


class QvizWidget:
    """Jupyter widget for displaying Quantum-viz quantum circuit.
    """
    n = 0

    def __init__(
        self,
        program: dict,
        width: int=400,
        height: int=350
    ):
        """Create QVizWidget instance

        :param program: Quantum program
        :type program: dict
        :param width: Widget width in pixels, defaults to 400
        :type width: int, optional
        :param height: Widget height in pixels, defaults to 350
        :type height: int, optional
        """
        try:
            self.name = varname()
        except VarnameRetrievingError:
            self.name = "_"

        self.width = width
        self.height = height
        self.value = program
        self._uids = []

    def _gen_uid(self):
        """Generate unique identifier for javascript applet"""
        uid = str(uuid.uuid1()).replace("-", "")
        # Keep track of all UIDs
        self._uids.append(uid)
        return uid

    def html_str(self, uid: str) -> str:
        """Returns an HTML string that contains the widget.

        :param uid: Unique identifier of widget
        :type uid: str
        :return: HTML string for displaying widget
        :rtype: str
        """
        QvizWidget.n += 1
        return _HTML_STR_FORMAT.format(
            base_url=BASE_URL,
            js_source=JS_SOURCE,
            uid=uid,
            data=self.value
        )

    def _ipython_display_(self):
        """Display the widget"""
        uid = self._gen_uid()
        qviz = HTML(self.html_str(uid=uid))
        display(qviz)
