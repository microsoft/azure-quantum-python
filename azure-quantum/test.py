class ResourceEstimatorResult():
    def _repr_html_(self):
        return """
        <html>
        <body>
        <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>

        <div id="summary-block">
        <h2>D3.js is Easy to Use</h2>
        <p>The script below selects the body element and appends a paragraph with the text "Hello World!":</p> 

        <script>
        d3.select("#summary-block").append("p").text("Hello World!");
        </script>

        </body>
        </html>"""

