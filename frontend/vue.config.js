const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  publicPath: '/static/src/vue/dist/', // Should be STATIC_URL + path/to/build
  outputDir: '../backend/static/src/vue/dist/', // Output to a directory in STATICFILES_DIRS
  filenameHashing: false,
  runtimeCompiler: true,
  devServer: {
    writeToDisk: true,
  },
  transpileDependencies: [
    'vuetify'
  ],

  chainWebpack: config => {
    config.optimization.splitChunks(false)

    config.plugin('BundleTracker').use(BundleTracker, [
      {
        filename: './webpack-stats.json'
      }
    ])

    config.resolve.alias.set('__STATIC__', 'static')

    config.devServer
      .public('http://127.0.0.1:8080')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['\*'] })
  }
}
