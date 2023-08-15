##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict, List, Optional, Union

import json
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
            self.diagram = EstimatorResultDiagram(self.data().copy())

        elif isinstance(data, list):
            super().__init__({idx: MicrosoftEstimatorResult(item_data)
                              for idx, item_data in enumerate(data)})

            self._data = data
            self._is_simple = False
            num_items = len(data)
            self._repr = ""
            if num_items > self.MAX_DEFAULT_ITEMS_IN_TABLE:
                self._repr += "<p><b>Info:</b> <i>The overview table is " \
                              "cut off after " \
                              f"{self.MAX_DEFAULT_ITEMS_IN_TABLE} items. If " \
                              "you want to see all items, suffix the result " \
                              "variable with <code>[:]</code></i></p>"
                num_items = self.MAX_DEFAULT_ITEMS_IN_TABLE
            self._repr += self._batch_result_table(range(num_items))

            # Add plot function for batching jobs
            self.plot = self._plot
            self.summary_data_frame = self._summary_data_frame

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

    def _plot(self, **kwargs):
        """
        Plots all result items in a space time plot, where the x-axis shows
        total runtime, and the y-axis shows total number of physical qubits.
        Both axes are in log-scale.
        Attributes:
            labels (list): List of labels for the legend.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "Missing optional 'matplotlib' dependency. To install run: "
                "pip install matplotlib"
            )

        labels = kwargs.pop("labels", [])

        [xs, ys] = zip(*[
            (self.data(i)['physicalCounts']['runtime'],
             self.data(i)['physicalCounts']['physicalQubits'])
             for i in range(len(self))])

        _ = plt.figure(figsize=(15, 8))

        plt.ylabel('Physical qubits')
        plt.xlabel('Runtime')
        plt.loglog()
        for i, (x, y) in enumerate(zip(xs, ys)):
            if isinstance(labels, list) and i < len(labels):
                label = labels[i]
            else:
                label = str(i)
            plt.scatter(x=[x], y=[y], label=label, marker="os+x"[i % 4])

        nsec = 1
        usec = 1e3 * nsec
        msec = 1e3 * usec
        sec = 1e3 * msec
        min = 60 * sec
        hour = 60 * min
        day = 24 * hour
        week = 7 * day
        month = 31 * day
        year = 365 * month
        decade = 10 * year
        century = 10 * decade

        time_units = [
            nsec, usec, msec, sec, min, hour, day, week,
            month, year, decade, century]
        time_labels = [
            "1 ns", "1 µs", "1 ms", "1 s", "1 min", "1 hour", "1 day",
            "1 week", "1 month", "1 year", "1 decade", "1 century"]

        cutoff = next(
            (i for i, x in enumerate(time_units) if x > max(xs)),
            len(time_units) - 1) + 1

        plt.xticks(time_units[0:cutoff], time_labels[0:cutoff], rotation=90)
        plt.legend(loc="upper left")
        plt.show()

    @property
    def json(self):
        """
        Returns a JSON representation of the resource estimation result data.
        """
        if not hasattr(self, "_json"):
            import json
            self._json = json.dumps(self._data)

        return self._json

    def _summary_data_frame(self, **kwargs):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "Missing optional 'pandas' dependency. To install run: "
                "pip install pandas"
            )

        # get labels or use default value, then extend with missing elements,
        # and truncate extra elements
        labels = kwargs.pop("labels", [])
        labels.extend(range(len(labels), len(self)))
        labels = labels[:len(self)]

        def get_row(result):
            formatted = result["physicalCountsFormatted"]

            return (
                formatted["algorithmicLogicalQubits"],
                formatted["logicalDepth"],
                formatted["numTstates"],
                result["logicalQubit"]["codeDistance"],
                formatted["numTfactories"],
                formatted["physicalQubitsForTfactoriesPercentage"],
                formatted["physicalQubits"],
                formatted["rqops"],
                formatted["runtime"]
            )

        data = [get_row(self.data(index)) for index in range(len(self))]
        columns = ["Logical qubits", "Logical depth", "T states",
                   "Code distance", "T factories", "T factory fraction",
                   "Physical qubits", "rQOPS", "Physical runtime"]
        return pd.DataFrame(data, columns=columns, index=labels)

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


class EstimatorResultDiagram:
    def __init__(self, data):
        data.pop("reportData")
        self.data_json = json.dumps(data).replace(" ", "")
        self.vis_lib = "https://cdn-aquavisualization-prod.azureedge.net/resource-estimation/index.js"
        self.space = HTMLWrapper(self._space_diagram())
        self.time = HTMLWrapper(self._time_diagram())

    def _space_diagram(self):
        html = f"""
            <script src={self.vis_lib}></script>
            <re-space-diagram data={self.data_json}></re-space-diagram>"""
        return html

    def _time_diagram(self):
        html = f"""
            <script src={self.vis_lib}></script>
            <re-time-diagram data={self.data_json}></re-time-diagram>"""
        return html