##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List, Optional, Union

import markdown


class HTMLWrapper:
    """
    Simple HTML wrapper to expose _repr_html_ for Jupyter clients.
    """
    def __init__(self, content: str):
        self.content = content

    def _repr_html_(self):
        return self.content


class MicrosoftEstimatorResult(dict):
    MAX_DEFAULT_ITEMS_IN_TABLE = 5

    def __init__(self, data: Union[Dict, List]):
        self._data = data

        if isinstance(data, dict):
            super().__init__(data)

            self._is_simple = True
            self._repr = self._item_result_table()
            self.summary = HTMLWrapper(self._item_result_summary_table())
        elif isinstance(data, list):
            super().__init__({idx: MicrosoftEstimatorResult(item_data)
                              for idx, item_data in enumerate(data)})

            self._data = data
            self._is_simple = False
            num_items = len(data)
            self._repr = ""
            if num_items > self.MAX_DEFAULT_ITEMS_IN_TABLE:
                self._repr += f"<p><b>Info:</b> <i>The overview table is " \
                              "cut off after " \
                              "{self.MAX_DEFAULT_ITEMS_IN_TABLE} items.  If " \
                              "you want to see all items, suffix the result " \
                              "variable with <code>[:]</code></i></p>"
                num_items = self.MAX_DEFAULT_ITEMS_IN_TABLE
            self._repr += self._batch_result_table(range(num_items))

    def data(self, idx: Optional[int] = None) -> Any:
        """
        Returns raw data of the result object.

        In case of a batching job, you can pass an index to access a specific
        item.
        """
        if idx is None:
            return self._data
        elif not self._is_simple:
            return self._data[idx]
        else:
            msg = "Cannot pass parameter 'idx' to 'data' for non-batching job"
            raise ValueError(msg)

    def _repr_html_(self):
        """
        HTML table representation of the result.
        """
        return self._repr

    def __getitem__(self, key):
        """
        If the result represents a batching job and key is a slice, a
        side-by-side table comparison is shown for the indexes represented by
        the slice.

        Otherwise, the key is used to access the raw data directly.
        """
        if isinstance(key, slice):
            if self._is_simple:
                msg = "Cannot pass slice to '__getitem__' for non-batching job"
                raise ValueError(msg)
            return HTMLWrapper(self._batch_result_table(range(len(self))[key]))
        else:
            return super().__getitem__(key)

    def _item_result_table(self):
        html = ""

        md = markdown.Markdown(extensions=['mdx_math'])
        for group in self['reportData']['groups']:
            html += f"""
                <details {"open" if group['alwaysVisible'] else ""}>
                    <summary style="display:list-item">
                        <strong>{group['title']}</strong>
                    </summary>
                    <table>"""
            for entry in group['entries']:
                val = self
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

        html += f"<details><summary style=\"display:list-item\"><strong>Assumptions</strong></summary><ul>"
        for assumption in self['reportData']['assumptions']:
            html += f"<li>{md.convert(assumption)}</li>"
        html += "</ul></details>"

        return html

    def _item_result_summary_table(self):
        html = """
            <style>
                .aqre-tooltip {
                    position: relative;
                    border-bottom: 1px dotted black;
                }

                .aqre-tooltip .aqre-tooltiptext {
                    font-weight: normal;
                    visibility: hidden;
                    width: 600px;
                    background-color: #e0e0e0;
                    color: black;
                    text-align: center;
                    border-radius: 6px;
                    padding: 5px 5px;
                    position: absolute;
                    z-index: 1;
                    top: 150%;
                    left: 50%;
                    margin-left: -200px;
                    border: solid 1px black;
                }

                .aqre-tooltip .aqre-tooltiptext::after {
                    content: "";
                    position: absolute;
                    bottom: 100%;
                    left: 50%;
                    margin-left: -5px;
                    border-width: 5px;
                    border-style: solid;
                    border-color: transparent transparent black transparent;
                }

                .aqre-tooltip:hover .aqre-tooltiptext {
                    visibility: visible;
                }
            </style>"""

        md = markdown.Markdown(extensions=['mdx_math'])
        for group in self['reportData']['groups']:
            html += f"""
                <details {"open" if group['alwaysVisible'] else ""}>
                    <summary style="display:list-item">
                        <strong>{group['title']}</strong>
                    </summary>
                    <table>"""
            for entry in group['entries']:
                val = self
                for key in entry['path'].split("/"):
                    val = val[key]
                explanation = md.convert(entry["explanation"])
                html += f"""
                    <tr class="aqre-tooltip">
                        <td style="font-weight: bold"><span class="aqre-tooltiptext">{explanation}</span>{entry['label']}</td>
                        <td>{val}</td>
                        <td style="text-align: left">{entry["description"]}</td>
                    </tr>
                """
            html += "</table></details>"

        html += f"<details><summary style=\'display:list-item\'><strong>Assumptions</strong></summary><ul>"
        for assumption in self['reportData']['assumptions']:
            html += f"<li>{md.convert(assumption)}</li>"
        html += "</ul></details>"

        return html

    def _batch_result_table(self, indices):
        html = ""

        md = markdown.Markdown(extensions=['mdx_math'])

        item_headers = "".join(f"<th>{i}</th>" for i in indices)

        for group_index, group in enumerate(self[0]['reportData']['groups']):
            html += f"""
                <details {"open" if group['alwaysVisible'] else ""}>
                    <summary style="display:list-item">
                        <strong>{group['title']}</strong>
                    </summary>
                    <table>
                        <thead><tr><th>Item</th>{item_headers}</tr></thead>"""

            visited_entries = set()

            for entry in [entry for index in indices for entry in self[index]['reportData']['groups'][group_index]['entries']]:
                label = entry['label']
                if label in visited_entries:
                    continue
                visited_entries.add(label)

                html += f"""
                    <tr>
                        <td style="font-weight: bold; vertical-align: top; white-space: nowrap">{label}</td>
                """

                for index in indices:
                    val = self[index]
                    for key in entry['path'].split("/"):
                        if key in val:
                            val = val[key]
                        else:
                            val = "N/A"
                            break
                    html += f"""
                            <td style="vertical-align: top; white-space: nowrap">{val}</td>
                    """

                html += """
                    </tr>
                """
            html += "</table></details>"

        html += f"<details><summary style=\"display:list-item\"><strong>Assumptions</strong></summary><ul>"
        for assumption in self[0]['reportData']['assumptions']:
            html += f"<li>{md.convert(assumption)}</li>"
        html += "</ul></details>"

        return html
