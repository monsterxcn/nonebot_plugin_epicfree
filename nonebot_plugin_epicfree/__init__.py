import sys

from nonebot import get_driver, get_bot
from nonebot.exception import FinishedException
from nonebot.log import logger
from nonebot.typing import T_State

try:
  from nonebot.plugin import on_regex, require
  from nonebot.adapters.onebot.v11 import (Bot, Event, GroupMessageEvent,
                                           Message, MessageEvent)
except ImportError:
  from nonebot import on_regex, require
  from nonebot.adapters.cqhttp import Bot, Event, Message
  from nonebot.adapters.cqhttp.event import GroupMessageEvent, MessageEvent

from .data_source import getEpicFree, subscribeHelper

try:
  epicScheduler = get_driver().config.epic_scheduler
  assert epicScheduler is not None
except (AttributeError, AssertionError):
  epicScheduler = "5 8 8 8"
day_of_week, hour, minute, second = epicScheduler.split(" ")


epicMatcher = on_regex("((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)", priority=2)
@epicMatcher.handle()
async def onceHandle(bot: Bot, event: Event):
  imfree = await getEpicFree()
  await epicMatcher.finish(Message(imfree))


epicSubMatcher = on_regex("喜(加一|\+1)(私聊)?订阅", priority=1)
@epicSubMatcher.handle()
async def subHandle(bot: Bot, event: MessageEvent, state: T_State):
  if isinstance(event, GroupMessageEvent):
    if event.sender.role not in ["admin", "owner"] or "私聊" in event.get_plaintext():
      # 普通群员只会启用私聊订阅
      # state["targetId"] = event.get_user_id()
      state["subType"] = "私聊"
    else:
      # 管理员用户询问需要私聊订阅还是群聊订阅
      pass
  else:
    state["subType"] = "私聊"


@epicSubMatcher.got("subType", prompt="默认启用群聊订阅，如需私聊订阅请回复「私聊」")
async def subEpic(bot: Bot, event: MessageEvent, state: T_State):
  if "私聊" in state["subType"]:
    state["targetId"] = event.get_user_id()
    state["subType"] = "私聊"
  else:
    state["targetId"] = str(event.group_id)
    state["subType"] = "群聊"
  msg = await subscribeHelper("w", state["subType"], state["targetId"])
  await epicSubMatcher.finish(msg)


scheduler = require("nonebot_plugin_apscheduler").scheduler
@scheduler.scheduled_job("cron", day_of_week=day_of_week, hour=hour, minute=minute, second=second)
async def weeklyEpic():
  bot = get_bot()
  whoSubscribe = await subscribeHelper()
  imfree = await getEpicFree()
  try:
    for group in whoSubscribe["群聊"]:
      await bot.send_group_msg(group_id=group, message=Message(imfree))
    for private in whoSubscribe["私聊"]:
      await bot.send_private_msg(user_id=private, message=Message(imfree))
  except FinishedException:
    pass
  except Exception as e:
    logger.error("Epic 限免游戏资讯定时任务出错：" + str(sys.exc_info()[0]) + "\n" + str(e))
