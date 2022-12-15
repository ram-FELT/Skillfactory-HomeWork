const { merge } = require('webpack-merge')
const baseWebpackConfig = require('./webpack.base.conf.js')

module.exports = merge(baseWebpackConfig, {
devServer: {
    static: './src',
  },
  mode: 'production',
  stats: 'none',
})
