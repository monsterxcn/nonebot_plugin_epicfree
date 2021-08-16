from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event, Message

from .data_source import *

matcher = on_regex("((E|e)(P|p)(I|i)(C|c))?喜(加一|\+1)", priority=1)


@matcher.handle()
async def handle(bot: Bot, event: Event, state: T_State):
  imfree = await get_Epicfree()
  msg = Message(imfree)
  await matcher.finish(msg)
