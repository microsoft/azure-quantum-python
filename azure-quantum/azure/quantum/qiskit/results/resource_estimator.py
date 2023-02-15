try:
    from qiskit.result import Result
    import markdown
    import copy
    from qiskit.result.models import ExperimentResult
    from qiskit.qobj import QobjHeader
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

class ResourceEstimatorBatchResult(Result):
    """
    A customized result for a resource estimation batching job.
    """

    MAX_DEFAULT_ITEMS_IN_TABLE = 5

    def __init__(
            self,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        # Creates individual result items for each item in the batch results
        self.result_items = [ResourceEstimatorResult(**{**kwargs, "results": [result]}) for result in self.results]

    @classmethod
    def from_dict(cls, data):
        """
        Overrides default behavior from Result.from_dict to account for batching
        data.
        """
        in_data = copy.copy(data)

        # We know that we have exactly one result here
        result = in_data.pop("results")[0]
        # All resource estimation results are in the data field, which we are going to flatten over all results
        data = result["data"]
        in_data["results"] = [ExperimentResult.from_dict({**result, "data": d}) for d in data]
        if "header" in in_data:
            in_data["header"] = QobjHeader.from_dict(in_data.pop("header"))
        return cls(**in_data)

    def __len__(self):
        """
        Returns the number of items in the batching job.
        """
        return len(self.results)

    def _repr_html_(self):
        """
        HTML representation of the result object; dispatches based on job
        success.
        """
        return self._repr_html_success_() if self.success else self._repr_html_error_()

    def _repr_html_success_(self):
        num_items = len(self.results)
        if num_items > self.MAX_DEFAULT_ITEMS_IN_TABLE:
            html = f"<p><b>Info:</b> <i>The overview table is cut off after {self.MAX_DEFAULT_ITEMS_IN_TABLE} items.  If you want to see all items, suffix the result variable with <code>[0:{num_items}]</code></i></p>"
            return html + _batch_result_html_table(self, range(self.MAX_DEFAULT_ITEMS_IN_TABLE))
        else:
            return _batch_result_html_table(self, range(len(self.results)))

    def _repr_html_error_(self):
        html = "<b>Job not successful</b>"
        if self.error_data is not None:
            html += f"""<br>Error code: {self.error_data['code']}
                <br>Error message: {self.error_data['message']}"""
        return html

    def plot(self, **kwargs):
        """
        Plots all result items in a space time plot, where the x-axis shows
        total runtime, and the y-axis shows total number of physical qubits.
        Both axes are in log-scale.

        Attributes:
            labels (list): List of labels for the legend.
        """
        import matplotlib.pyplot as plt

        labels = kwargs.pop("labels", [])

        [xs, ys] = zip(*[(self.data(i)['physicalCounts']['runtime'], self.data(i)['physicalCounts']['physicalQubits']) for i in range(len(self))])

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

        time_units = [nsec, usec, msec, sec, min, hour, day, week, month, year, decade, century]
        time_labels = ["1 ns", "1 µs", "1 ms", "1 s", "1 min", "1 hour", "1 day", "1 week", "1 month", "1 year", "1 decade", "1 century"]

        cutoff = next((i for i, x in enumerate(time_units) if x > max(xs)), len(time_units) - 1) + 1

        plt.xticks(time_units[0:cutoff], time_labels[0:cutoff], rotation=90)
        plt.legend(loc="upper left")
        plt.show()

    def __getitem__(self, key):
        if isinstance(key, slice):
            from IPython.display import display, HTML
            display(HTML(_batch_result_html_table(self, range(len(self.results))[key])))
        else:
            return self.result_items[key]

class ResourceEstimatorResult(Result):
    """
    A customized result for a resource estimation job.
    """

    def __init__(
        self,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

        # We also create a summary view based on a different result type.
        self.summary = ResourceEstimatorResultSummary(**kwargs)

    def _repr_html_(self):
        """
        HTML representation of the result object; dispatches based on job
        success.
        """
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

        html += f"<details><summary style=\"display:list-item\"><strong>Assumptions</strong></summary><ul>"
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

class ResourceEstimatorResultSummary(Result):
    def __init__(
        self,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)

    def _repr_html_(self):
        return self._repr_html_success_() if self.success else self._repr_html_error_()

    def _repr_html_success_(self):
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
                    <tr class="aqre-tooltip">
                        <td style="font-weight: bold"><span class="aqre-tooltiptext">{explanation}</span>{entry['label']}</td>
                        <td>{val}</td>
                        <td style="text-align: left">{entry["description"]}</td>
                    </tr>
                """
            html += "</table></details>"

        html += f"<details><summary style=\'display:list-item\'><strong>Assumptions</strong></summary><ul>"
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

def _batch_result_html_table(result, indices):
    html = ""

    md = markdown.Markdown(extensions=['mdx_math'])

    item_headers = "".join(f"<th>{i}</th>" for i in indices)

    for group_index, group in enumerate(result.data(0)['reportData']['groups']):
        html += f"""
            <details {"open" if group['alwaysVisible'] else ""}>
                <summary style="display:list-item">
                    <strong>{group['title']}</strong>
                </summary>
                <table>
                    <thead><tr><th>Item</th>{item_headers}</tr></thead>"""

        visited_entries = set()

        for entry in [entry for index in indices for entry in result.data(index)['reportData']['groups'][group_index]['entries']]:
            label = entry['label']
            if label in visited_entries:
                continue
            visited_entries.add(label)

            html += f"""
                <tr>
                    <td style="font-weight: bold; vertical-align: top; white-space: nowrap">{label}</td>
            """

            for index in indices:
                val = result.data(index)
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
    for assumption in result.data(0)['reportData']['assumptions']:
        html += f"<li>{md.convert(assumption)}</li>"
    html += "</ul></details>"

    return html
