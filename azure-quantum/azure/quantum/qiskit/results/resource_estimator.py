try:
    from qiskit.result import Result
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

import markdown

class ResourceEstimatorResult(Result):
    def __init__(
        self,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

    def _repr_html_(self):
        return self._repr_html_success_() if self.success else self._repr_html_error_()

    def _repr_html_success_(self):
        html = ""

        md = markdown.Markdown(extensions=['mdx_math'])
        for group in self.data()['reportData']['groups']:
            html += f"""
                <details {"open" if group['alwaysVisible'] else ""}>
                    <summary style="display:list-item">
                        <strong>{group['title']}</strong>
                    </summary>
                <table>"""
            for entry in group['entries']:
                val = self.data()
                for key in entry['path'].split("/"):
                    val = val[key]
                explanation = md.convert(entry["explanation"])
                html += f"""
                    <tr>
                        <td style="font-weight: bold; vertical-align: top; white-space: nowrap">{entry['label']}</td>
                        <td style="vertical-align: top; white-space: nowrap">{val}</td>
                        <td style="text-align: left">
                            <strong>{entry["description"]}</strong>
                            <hr style="margin-top: 2px; margin-bottom: 0px; border-top: solid 1px black" />
                            {explanation}
                        </td>
                    </tr>
                """
            html += "</table></details>"

        html += f"<details> <summary style='display:list-item'><strong>Assumptions</strong></summary><ul>"
        for assumption in self.data()['reportData']['assumptions']:
            html += f"<li>{md.convert(assumption)}</li>"
        html += "</ul></details>"

        return html

    def _repr_html_error_(self):
        html = "<b>Job not successful</b>"
        if self.error_data is not None:
            html += f"""<br>Error code: {self.error_data['code']}
                <br>Error message: {self.error_data['message']}"""
        return html
