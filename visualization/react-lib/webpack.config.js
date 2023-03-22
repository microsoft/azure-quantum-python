const path = require('path')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const nodeExternals = require('webpack-node-externals');

module.exports = {
    entry: './src/index.ts',
    externals: [nodeExternals()],
    output: {
        path: path.resolve(__dirname, 'dist'),
    },
    plugins: [new CleanWebpackPlugin()],
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/,
                exclude: /node_modules/,
                resolve: {
                    extensions: ['.ts', '.tsx', '.js', '.json'],
                },
                use: 'ts-loader'
            },
            {
                test: /\.css$/,
                use: ['css-loader'],
                exclude: /node_modules/,
            },
        ]
    }
};