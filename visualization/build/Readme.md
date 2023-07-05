## How to build JS library

### 1. Run build.sh scipt from the build folder.

### <u>OR</u>

### 2. Complete the following steps

- cd react-lib
- npm install
- npm run build
- npm link
- cd node_modules/react
- npm link
- cd js-lib
- npm link react quantum-visualization
- npm run build

### <u>ADO pipeline flow for CI/CD </u>

#### [<i> microsoft.visualization <i>](https://ms-quantum.visualstudio.com/Quantum%20Program/_build?definitionId=789&_a=summary)

The build pipeline is divided into 3 yaml files.

1. The root build, visualization-lib.yml, is triggered with PRs and branch commits.
2. Visualization-lib.yml triggers react-lib-build.yml which builds react-lib and creates an npm link.
3. Following react-lib-build.yml, js-lib-build.yml is triggered which links to react-lib and builds the js-lib and publishes the index.js to the build artifacts for library consumption.
