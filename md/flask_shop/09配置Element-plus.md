## 1：配置Element-plus

1.1安装Element-plus   

yarn add element-plus

如果他在此系统禁止运行这个脚本的话，我们在powershell用管理员运行Set-ExecutionPolicy RemoteSigned，让他改变策略，按y回车，在去下载

1.2：组件的按需加载，先安装下面

yarn add unplugin-vue-components unplugin-auto-

1.3在vue.config.js直接覆盖原来代码

```javascript

const { defineConfig } = require('@vue/cli-service')
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')


module.exports = defineConfig({
 transpileDependencies: true,
 configureWebpack: {
  plugins: [
   AutoImport({
    resolvers: [ElementPlusResolver()]
    }),
   Components({
    resolvers: [ElementPlusResolver()]
    })
   ]
  }
})

```

```javascript
// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })
const { defineConfig } = require("@vue/cli-service");
const AutoImport = require("unplugin-auto-import/webpack").default;
const Components = require("unplugin-vue-components/webpack").default;
const { ElementPlusResolver } = require("unplugin-vue-components/resolvers");

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
    ],
  },
});
// npm cache clean --force
// npm install vue@3.2.45 --save
// rm -rf node_modules
// rm package-lock.json
// npm install




```

下面这种写法是支持的