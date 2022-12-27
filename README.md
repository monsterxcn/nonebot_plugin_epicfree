<h1 align="center">NoneBot Plugin EpicFree</h1></br>


<p align="center">🤖 用于获取 Epic 限免游戏资讯的 NoneBot2 插件</p></br>


<p align="center">
  <a href="https://github.com/monsterxcn/nonebot_plugin_epicfree/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/monsterxcn/nonebot_plugin_epicfree/publish.yml?branch=main&style=flat-square" alt="actions">
  </a>
  <a href="https://raw.githubusercontent.com/monsterxcn/nonebot_plugin_epicfree/master/LICENSE">
    <img src="https://img.shields.io/github/license/monsterxcn/nonebot_plugin_epicfree?style=flat-square" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot_plugin_epicfree">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_epicfree?style=flat-square" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=flat-square" alt="python"><br />
</p></br>


**安装方法**


使用以下命令之一快速安装（若配置了 PyPI 镜像，你可能无法及时检索到插件最新版本）：


``` zsh
nb plugin install nonebot_plugin_epicfree

pip install --upgrade nonebot_plugin_epicfree
```


重启 Bot 即可体验此插件。


<details><summary><i>关于 NoneBot2 及相关依赖版本</i></summary></br>


在已淘汰的 NoneBot2 适配器 [nonebot-adapter-cqhttp](https://pypi.org/project/nonebot-adapter-cqhttp/) 下，切记不要使用 `pip` 或 `nb_cli` 安装此插件。通过拷贝文件夹 `nonebot_plugin_epicfree` 至 NoneBot2 插件目录、手动安装 `nonebot-plugin-apscheduler` 和 `httpx` 依赖的方式仍可正常启用此插件。在未来某个版本会完全移除该适配器支持，请尽快升级至 [nonebot-adapter-onebot](https://pypi.org/project/nonebot-adapter-onebot/)。


</details>


<details><summary><i>关于 go-cqhttp 版本</i></summary></br>


插件发送消息依赖 [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的合并转发接口，如需启用私聊响应请务必安装 [v1.0.0-rc2](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-rc2) 以上版本的 go-cqhttp。


</details>


**使用方法**


```python
# nonebot_plugin_epicfree/__init__.py#L27
epic_matcher = on_regex(r"^(epic)?喜(加|\+|＋)(一|1)$", priority=2, flags=IGNORECASE)

# nonebot_plugin_epicfree/__init__.py#L39
sub_matcher = on_regex(r"^喜(加|\+|＋)(一|1)(私聊)?订阅(删除|取消)?$", priority=1)
```


 - 发送「喜加一」查找限免游戏
 - 发送「喜加一订阅」订阅游戏资讯
 - 发送「喜加一订阅删除」取消订阅游戏资讯


*\* 插件响应基于正则匹配，所以，甚至「EpIc喜+1」这样的指令都可用！*


**环境变量**


```
RESOURCES_DIR="/data/bot/resources"
EPIC_SCHEDULER="8 8 8"
```


限免游戏资讯订阅功能默认在机器人根目录下 `/data/epicfree` 文件夹内生成配置文件。定义 `RESOURCES_DIR` 环境变量即可指定用于存放订阅配置的文件夹，填写包含 `epicfree` 文件夹的 **父级文件夹** 路径即可。如果是 Windows 系统应写成类似 `D:/path/to/resources_dir` 的格式。

限免游戏资讯订阅默认 08:08:08 发送（如果当天的游戏已经推送过则不产生推送），定义 `EPIC_SCHEDULER` 环境变量即可指定推送时间，该配置的三个数字依次代表 `hour` `minute` `second`。


**特别鸣谢**


[@nonebot/nonebot2](https://github.com/nonebot/nonebot2/) | [@Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) | [@DIYgod/RSSHub](https://github.com/DIYgod/RSSHub) | [@SD4RK/epicstore_api](https://github.com/SD4RK/epicstore_api)


> 作者是 NoneBot2 新手，代码写的较为粗糙，欢迎提出修改意见或加入此插件开发！溜了溜了...
