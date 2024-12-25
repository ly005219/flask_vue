## 1：在debug里面点新建json文件之前点开要debug的文件manager.py，在选择flask即可

```json
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask_shop",
      "type": "debugpy",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "manager.py",
        "FLASK_DEBUG": "1"
      },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true,
      "autoStartBrowser": false, //是否自动打开浏览器
      "justMyCode": true //false时可以调试第三方模块的代码，不只有自己的代码,一般设置为true，不然debug的时候会走到第三方模块的代码，导致调试不方便会很久
    }
  ]
}
```

