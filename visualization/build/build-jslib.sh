#!/bin/bash
# assume working directory to be "visualization/build"

cd ../react-lib
npm install
if [ $? -eq 0 ]; then
  echo 'Successfully install: react-lib'
fi

npm run build
if [ $? -eq 0 ]; then
  echo 'Successfully build: react-lib'
fi

npm link
if [ $? -eq 0 ]; then
  echo 'Successfully created link: react-lib'
fi

cd node_modules/react
npm link
if [ $? -eq 0 ]; then
  echo 'Successfully created link: node_modules/react'
fi

cd ../../../js-lib
npm link react quantum-visualization
if [ $? -eq 0 ]; then
  echo 'Successfully linked react and quantum-visualization to js-lib.'
fi

npm run build
if [ $? -eq 0 ]; then
  echo 'Successfully built js-lib'
fi

echo 'Successfully built js-lib and dependencies.' && exit 0
fi