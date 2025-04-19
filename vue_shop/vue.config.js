// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })
const { defineConfig } = require("@vue/cli-service");
const AutoImport = require("unplugin-auto-import/webpack").default;
const Components = require("unplugin-vue-components/webpack").default;
const { ElementPlusResolver } = require("unplugin-vue-components/resolvers");
const webpack = require("webpack");

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
        __VUE_PROD_DEVTOOLS__: 'false'
      }),
    ],
  },
});
// npm cache clean --force
// npm install vue@3.2.45 --save
// rm -rf node_modules
// rm package-lock.json
// npm install



