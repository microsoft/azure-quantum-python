module.exports = function (api) {
    api.cache(true);
    
    const presets = [ "@babel/preset-env", "@babel/preset-react" ];
    const generatorOpts ={"compact" : true};

    return {
      presets,
      generatorOpts
    };
  }