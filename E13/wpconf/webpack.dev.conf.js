const webpack = require('webpack')
const { merge } = require('webpack-merge')
const baseWebpackConfig = require('./webpack.base.conf.js')

module.exports = merge(baseWebpackConfig, {
  mode: 'development',
  devtool: 'eval-source-map',
  devServer: {
    static: './dist',
    port: 3001,
    hot: true,
    open: true,
  },
  stats: 'summary',
  plugins: [
    new webpack.SourceMapDevToolPlugin({
      filename: '[file].map',
    }),
  ],
})
