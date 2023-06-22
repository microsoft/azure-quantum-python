const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = {
    entry: './src/index.ts',
    output: {
        path: path.resolve(__dirname, 'dist'),
        libraryTarget: 'commonjs'
    },
    plugins: [new CleanWebpackPlugin()],
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                exclude: /node_modules/,
                resolve: {
                    extensions: ['.ts', '.tsx', '.js', '.jsx', '.json'],
                },
                use: 'ts-loader'
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    { loader: "css-loader", options: { sourceMap: true } },
                  ],
                exclude: /node_modules/,
            }
        ]
    },
    externals: {
      'react': 'react',
    }
};