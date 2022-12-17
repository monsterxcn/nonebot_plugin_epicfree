import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_epicfree",
    version="0.2.4",
    author="monsterxcn",
    author_email="monsterxcn@gmail.com",
    description="EpicGameStore free games promotions plugin for NoneBot2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monsterxcn/nonebot_plugin_epicfree",
    project_urls={
        "Bug Tracker": "https://github.com/monsterxcn/nonebot_plugin_epicfree/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["nonebot_plugin_epicfree"],
    python_requires=">=3.8,<4.0",
    install_requires=[
        "nonebot2>=2.0.0b3",
        "httpx>=0.20.0,<1.0.0",
        "nonebot-adapter-onebot>=2.0.0b1",
        "nonebot-plugin-apscheduler>=0.1.0",
        "pytz"
    ],
)
