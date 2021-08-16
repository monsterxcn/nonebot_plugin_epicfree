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


可以使用以下两命令快速安装，但请注意可能引起的依赖版本冲突。

如果 `pip` 配置了 PyPI 镜像（推荐清华大学 PyPI 镜像），你可能无法及时检索到插件最新版本。


``` zsh
nb plugin install nonebot_plugin_epicfree
# or
pip install --upgrade nonebot_plugin_epicfree
```


<details><summary> **关于依赖版本** </summary></br>


以上述方式安装本插件时，可能由于版本差异引起报错，对于新手推荐在安装插件前先存留当前环境依赖版本，以便后续恢复：


```bash
# 备份当前的依赖版本
pip3 freeze > requirements.txt

# 尝试安装 nonebot_plugin_epicfree

# 安装备份的依赖版本
pip3 install -r requirements.txt
```


如果安装前未存留备份，可以在 **安装完本插件后**，使用 `pip3 install --upgrade nb-cli` 按最新版本 `nb-cli` 的依赖重新安装，实测不影响此插件使用。

建议使用 **Python 虚拟环境**。


</details>


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