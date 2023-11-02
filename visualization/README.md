# Visualization

This folder contains visualizations for the resource estimation feature.

- react-lib: source code for the visualization components and D3 integration.
- js-lib: wrapper JavaScript library which packages the visualization components into a consumable JavaScript package by clients.

Refer to **build** folder to build and package the js-lib and react-lib.

For react-build project:

```
- npm run build // builds react-lib
- npm run tests //runs all tests and code coverage
- npm run testsonly //excludes code coverage
- npm run updatetests //updates test snapshots and runs tests with no coverage
```
