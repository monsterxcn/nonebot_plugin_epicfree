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
  <img src="https://img.shields.io/badge/python-3.7.3+-blue?style=flat-square" alt="python"><br />
</p></br>


**安装方法**


使用以下命令之一快速安装（若配置了 PyPI 镜像，你可能无法及时检索到插件最新版本）：


``` zsh
nb plugin install nonebot_plugin_epicfree

pip install --upgrade nonebot_plugin_epicfree
```


重启 Bot 即可体验此插件。


<details><summary><i>关于依赖版本</i></summary></br>


以上述方式安装本插件时，可能由于版本差异引起报错，对于新手推荐在安装插件前先存留当前环境依赖版本，以便后续恢复：


```bash
# 备份当前的依赖版本
pip3 freeze > requirements.txt

# 尝试安装 nonebot_plugin_epicfree

# 若安装出错，可尝试恢复之前备份的依赖版本
pip3 install -r requirements.txt
```


若实在无法使用，可以自行将仓库内 `nonebot_plugin_epicfree` 文件夹复制到 Nonebot2 机器人插件目录下，确保安装过 `nonebot_plugin_apscheduler`，重启 bot 即可！


> 建议学习使用 **Python 虚拟环境**。


</details>


<details><summary><i>单独加载此插件</i></summary></br>


在 Nonebot2 入口文件（例如 `bot.py`）增加：


``` python
nonebot.load_plugin("nonebot_plugin_epicfree")
```


</details>


**使用方法**


```python
# nonebot_plugin_epicfree/__init__.py#L20
epicMatcher = on_regex("((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)")

# nonebot_plugin_epicfree/__init__.py#L27
epicSubMatcher = on_regex("喜(加一|\+1)(私聊)?订阅")
```


发送「Epic喜加一」查找游戏，群组内发送「喜加一订阅」订阅限免游戏资讯。基于正则匹配，所以，甚至「EpIc喜+1」这样的指令都可用！（

限免游戏资讯订阅默认每周六 08:08:08 发送，如需自定义请在 `.env` 中添加格式如下的配置：


```
epic_scheduler="sat 8 8 8"
```


**特别鸣谢**


[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@DIYgod/RSSHub](https://github.com/DIYgod/RSSHub) | [@SD4RK/epicstore_api](https://github.com/SD4RK/epicstore_api)


> 作者是 Nonebot 新手，代码写的较为粗糙，欢迎提出修改意见或加入此插件开发！溜了溜了...