const TerserWebpackPlugin = require('terser-webpack-plugin')

const path = require('path')

const PATHS = {
  src: path.join(__dirname, '../src/'),
  dist: path.join(__dirname, '../dist/'),
  build: path.join(__dirname, './build/'),
  assets: 'assets/',
}

module.exports = {
  externals: {
    paths: PATHS,
  },
  entry: './src/index.js',
  output: {
    filename: 'js/[name].js',
  },
  plugins: [
    new TerserWebpackPlugin(),
  ],
  optimization: {
    minimizer: [new TerserWebpackPlugin({})],
  },

}
