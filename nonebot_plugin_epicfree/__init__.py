from traceback import format_exc
from typing import Dict

from nonebot import get_bot, get_driver, on_regex
from nonebot.exception import FinishedException
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot_plugin_apscheduler import scheduler

try:
    from nonebot.adapters.onebot.v11 import Bot, Event, Message  # type: ignore
    from nonebot.adapters.onebot.v11.event import (  # type: ignore
        GroupMessageEvent,
        MessageEvent,
    )
except ImportError:
    from nonebot.adapters.cqhttp import Bot, Event, Message  # type: ignore
    from nonebot.adapters.cqhttp.event import GroupMessageEvent, MessageEvent  # type: ignore

from .data_source import getEpicFree, subscribeHelper

epicScheduler = str(getattr(get_driver().config, "epic_scheduler", "5 8 8 8"))
day_of_week, hour, minute, second = epicScheduler.split(" ")


epicMatcher = on_regex(r"((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)", priority=2)


@epicMatcher.handle()
async def onceHandle(bot: Bot, event: Event):
    imfree = await getEpicFree()
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(group_id=event.group_id, messages=imfree)  # type: ignore
    else:
        await bot.send_private_forward_msg(user_id=event.user_id, messages=imfree)  # type: ignore


epicSubMatcher = on_regex(r"喜(加一|\+1)(私聊)?订阅(删除|取消)?", priority=1)


@epicSubMatcher.handle()
async def subHandle(bot: Bot, event: MessageEvent, state: T_State):
    msg = event.get_plaintext()
    state["action"] = "删除" if any(s in msg for s in ["删除", "取消"]) else "启用"
    if isinstance(event, GroupMessageEvent):
        if event.sender.role not in ["admin", "owner"] or "私聊" in msg:
            # 普通群员只会启用私聊订阅
            state["subType"] = "私聊"
        else:
            # 管理员用户询问需要私聊订阅还是群聊订阅
            pass
    else:
        state["subType"] = "私聊"


@epicSubMatcher.got(
    "subType", prompt=Message.template("回复「私聊」{action}私聊订阅，回复其他内容{action}群聊订阅：")
)
async def subEpic(bot: Bot, event: MessageEvent, state: T_State):
    if any("私聊" in i for i in [event.get_plaintext().strip(), state["subType"]]):
        state["targetId"] = event.get_user_id()
        state["subType"] = "私聊"
    else:
        state["targetId"] = str(event.group_id)  # type: ignore
        state["subType"] = "群聊"
    msg = await subscribeHelper(state["action"], state["subType"], state["targetId"])
    await epicSubMatcher.finish(str(msg))


@scheduler.scheduled_job(
    "cron", day_of_week=day_of_week, hour=hour, minute=minute, second=second
)
async def weeklyEpic():
    bot = get_bot()
    whoSubscribe = await subscribeHelper()
    msgList = await getEpicFree()
    try:
        assert isinstance(whoSubscribe, Dict)
        for group in whoSubscribe["群聊"]:
            await bot.send_group_forward_msg(group_id=group, messages=msgList)
        for private in whoSubscribe["私聊"]:
            await bot.send_private_forward_msg(user_id=private, messages=msgList)
    except FinishedException:
        pass
    except Exception as e:
        logger.error(f"Epic 限免游戏资讯定时任务出错 {e.__class__.__name__}：{format_exc()}")
