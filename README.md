<h1 align="center">Nonebot Plugin EpicFree</h1></br>


<p align="center">🤖 用于获取 Epic 限免游戏资讯的 Nonebot2 插件</p></br>


<p align="center">
  <a href="https://github.com/monsterxcn/nonebot_plugin_epicfree/actions">
    <img src="https://img.shields.io/github/workflow/status/monsterxcn/Typecho-Theme-VOID/Build?style=flat-square" alt="actions">
  </a>
  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot_plugin_epicfree/master/LICENSE">
    <img src="https://img.shields.io/github/license/monsterxcn/nonebot_plugin_epicfree?style=flat-square" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_epicfree">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_epicfree?style=flat-square" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7.0+-blue?style=flat-square" alt="python"><br />
</p></br>


**安装方法**


``` zsh
nb plugin install nonebot_plugin_epicfree
# or
pip install --upgrade nonebot_plugin_epicfree
```


在 Nonebot2 入口文件（例如 `bot.py`）增加：


``` python
nonebot.load_plugin("nonebot_plugin_epicfree")
```


**指令详解**


```python
# nonebot_plugin_epicfree/nonebot_plugin_epicfree/__init__.py#L7
matcher = on_regex("((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)")
```


基于正则匹配，所以，甚至 `EpIc喜+1` 这样的指令都可用！（

如果你觉得不顺眼也可以自己参考 Nonebot2 文档修改下。


**特别鸣谢**

[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@DIYgod/RSSHub](https://github.com/DIYgod/RSSHub) | [@SD4RK/epicstore_api](https://github.com/SD4RK/epicstore_api)