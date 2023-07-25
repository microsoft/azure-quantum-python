#!/bin/bash 
# assume working directory to be "visualization/build"

cd ../react-lib
npm install
if [ $? -ne 0 ]; then
  echo 'Failed to install: react-lib'
  exit 1 
else
  echo 'Successfully install: react-lib'
fi

npm run build:prod
if [ $? -ne 0 ]; then
  echo 'Failed to build: react-lib'
  exit 1
else 
  echo 'Successfully build: react-lib'
fi

npm link
if [ $? -ne 0 ]; then
  echo 'Failed to create link: react-lib'
  exit 1
else
  echo 'Successfully created link: react-lib'
fi

cd node_modules/react
npm link
if [ $? -ne 0 ]; then
  echo 'Failed to create link: node_modules/react'
  exit 1
else
  echo 'Successfully created link: node_modules/react'
fi

cd ../../../js-lib
npm link react quantum-visualization
if [ $? -ne 0 ]; then
  echo 'Failed to link react and quantum-visualization to js-lib.'
  exit 1
else
  echo 'Successfully linked react and quantum-visualization to js-lib'
fi

npm run build:prod
if [ $? -ne 0 ]; then
  echo 'Failed to build js-lib'
  exit 1
else
  echo 'Successfully built js-lib'
fi

echo 'Successfully built js-lib and dependencies.' 
echo 'js-lib to be published to microsoft-visualization/index.js artifact."
exit 0