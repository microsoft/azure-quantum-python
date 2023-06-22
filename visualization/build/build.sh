#!/bin/bash
# Use flag buildJsLibOnly to only build js-lib

if [ "$1" == "buildJsLibOnly" ]; then
  cd ../js-lib
  npm link react quantum-visualization
  if [ $? -eq 0 ]; then
    echo 'Successfully linked react and quantum-visualization'
  fi
  npm run build
  if [ $? -eq 0 ]; then
    echo 'Successfully built js-lib'
 exit 0
  fi
 else 

cd ../react-lib
npm install
if [ $? -eq 0 ]; then
  echo 'Successfully installed react-lib'
fi
npm run build
if [ $? -eq 0 ]; then
  echo 'Successfully built react-lib'
fi
npm link
if [ $? -eq 0 ]; then
  echo 'Successfully linked react-lib'
fi
cd node_modules/react
npm link
if [ $? -eq 0 ]; then
  echo 'Successfully linked node_modules/react'
fi
cd ../../../js-lib
npm link react quantum-visualization
if [ $? -eq 0 ]; then
  echo 'Successfully linked react and quantum-visualization'
fi
npm run build
if [ $? -eq 0 ]; then
  echo 'Successfully built js-lib'
fi
echo 'Successfully built js-li and dependencies.' && exit 0
fi