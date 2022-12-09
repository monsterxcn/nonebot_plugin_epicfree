import json
from datetime import datetime
from pathlib import Path
from traceback import format_exc
from typing import Dict, List, Literal, Union

from httpx import AsyncClient
from nonebot import get_driver
from nonebot.log import logger
from pytz import timezone

try:
    from nonebot.adapters.onebot.v11 import Message, MessageSegment  # type: ignore
except ImportError:
    from nonebot.adapters.cqhttp import Message, MessageSegment  # type: ignore

resPathParent = getattr(get_driver().config, "resources_dir", None)
if resPathParent and Path(resPathParent).exists():
    resPath = Path(resPathParent) / "epicfree"
else:
    resPath = Path("data/epicfree")
resPath.mkdir(parents=True, exist_ok=True)
cache = resPath / "status.json"


# 写入与读取订阅信息
async def subscribeHelper(
    method: Literal["读取", "启用", "删除"] = "读取", subType: str = "", subject: str = ""
) -> Union[Dict, str]:
    if cache.exists():
        statusDict = json.loads(cache.read_text(encoding="UTF-8"))
    else:
        statusDict = {"群聊": [], "私聊": []}
        cache.write_text(
            json.dumps(statusDict, ensure_ascii=False, indent=2), encoding="UTF-8"
        )
    # 读取时，返回订阅状态字典
    if method == "读取":
        return statusDict
    # 启用订阅时，将新的用户按类别写入至指定数组
    elif method == "启用":
        if subject in statusDict[subType]:
            return f"{subType}{subject} 已经订阅过 Epic 限免游戏资讯了哦！"
        statusDict[subType].append(subject)
    # 删除订阅
    elif method == "删除":
        if subject not in statusDict[subType]:
            return f"{subType}{subject} 未曾订阅过 Epic 限免游戏资讯！"
        statusDict[subType].remove(subject)
    try:
        cache.write_text(
            json.dumps(statusDict, ensure_ascii=False, indent=2), encoding="UTF-8"
        )
        return f"{subType}{subject} Epic 限免游戏资讯订阅已{method}！"
    except Exception as e:
        logger.error(f"写入 Epic 订阅 JSON 错误 {e.__class__.__name__}\n{format_exc()}")
        return f"{subType}{subject} Epic 限免游戏资讯订阅{method}失败惹.."


# 获取所有 Epic Game Store 促销游戏
# 方法参考：RSSHub /epicgames 路由
# https://github.com/DIYgod/RSSHub/blob/master/lib/routes/epicgames/index.js
async def getEpicGame() -> List:
    async with AsyncClient(proxies={"all://": None}) as client:
        try:
            res = await client.get(
                "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions",
                params={"locale": "zh-CN", "country": "CN", "allowCountries": "CN"},
                headers={
                    "Referer": "https://www.epicgames.com/store/zh-CN/",
                    "Content-Type": "application/json; charset=utf-8",
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                        " (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
                    ),
                },
                timeout=10.0,
            )
            resJson = res.json()
            return resJson["data"]["Catalog"]["searchStore"]["elements"]
        except Exception as e:
            logger.error(f"请求 Epic Store API 错误 {e.__class__.__name__}\n{format_exc()}")
            return []


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def getEpicFree() -> List[MessageSegment]:
    games = await getEpicGame()
    if not games:
        return [
            MessageSegment.node_custom(
                user_id=2854196320,
                nickname="EpicGameStore",
                content=Message("Epic 可能又抽风啦，请稍后再试（"),
            )
        ]
    else:
        logger.debug(
            f"获取到 {len(games)} 个游戏数据：\n{('、'.join(game['title'] for game in games))}"
        )
        gameCnt, msgList = 0, []
        for game in games:
            game_name = game.get("title", "未知")
            try:
                if not game.get("promotions"):
                    continue
                game_promotions = game["promotions"]["promotionalOffers"]
                upcoming_promotions = game["promotions"]["upcomingPromotionalOffers"]
                original_price = game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
                discount_price = game["price"]["totalPrice"]["fmtPrice"]["discountPrice"]
                if not game_promotions:
                    if upcoming_promotions:
                        logger.info(f"跳过即将推出免费游玩的游戏：{game_name}({discount_price})")
                    continue  # 仅返回正在推出免费游玩的游戏
                elif game["price"]["totalPrice"]["fmtPrice"]["discountPrice"] != "0":
                    logger.info(f"跳过促销但不免费的游戏：{game_name}({discount_price})")
                    continue
                # 处理游戏预览图
                for image in game["keyImages"]:
                    # 修复部分游戏无法找到图片
                    # https://github.com/HibiKier/zhenxun_bot/commit/92e60ba141313f5b28f89afdfe813b29f13468c1
                    if image.get("url") and image["type"] in [
                        "Thumbnail",
                        "VaultOpened",
                        "DieselStoreFrontWide",
                        "OfferImageWide",
                    ]:
                        msgList.append(
                            MessageSegment.node_custom(
                                user_id=2854196320,
                                nickname="EpicGameStore",
                                content=Message(MessageSegment.image(image["url"])),
                            )
                        )
                        break
                # 处理游戏发行信息
                game_dev, game_pub = game["seller"]["name"], game["seller"]["name"]
                for pair in game["customAttributes"]:
                    if pair["key"] == "developerName":
                        game_dev = pair["value"]
                    elif pair["key"] == "publisherName":
                        game_pub = pair["value"]
                dev_info = f"{game_dev} 开发" if game_dev != game_pub else ""
                # 处理游戏限免结束时间
                date_rfc3339 = game_promotions[0]["promotionalOffers"][0]["endDate"]
                end_date = (
                    datetime.strptime(date_rfc3339, "%Y-%m-%dT%H:%M:%S.%f%z")
                    .astimezone(timezone("Asia/Shanghai"))
                    .strftime("%m {m} %d {d} %H:%M")
                    .format(m="月", d="日")
                )
                # 处理游戏商城链接（API 返回不包含游戏商店 URL，依经验自行拼接
                if game.get("urlSlug"):
                    game_url = "https://store.epicgames.com/zh-CN/p/{}".format(
                        game["urlSlug"].replace("/home", "")
                    )
                elif game.get("url"):
                    game_url = game["url"]
                else:
                    slugs = (
                        [
                            x["pageSlug"]
                            for x in game.get("offerMappings", [])
                            if x.get("pageType") == "productHome"
                        ]
                        + [
                            x["pageSlug"]
                            for x in game.get("catalogNs", {}).get("mappings", [])
                            if x.get("pageType") == "productHome"
                        ]
                        + [
                            x["value"]
                            for x in game.get("customAttributes", [])
                            if "productSlug" in x.get("key")
                        ]
                    )
                    game_url = "https://store.epicgames.com/zh-CN{}".format(
                        f"/p/{slugs[0]}" if len(slugs) else ""
                    )
                gameCnt += 1
                msgList.extend(
                    [
                        MessageSegment.node_custom(
                            user_id=2854196320,
                            nickname="EpicGameStore",
                            content=Message(MessageSegment.text(game_url)),
                        ),
                        MessageSegment.node_custom(
                            user_id=2854196320,
                            nickname="EpicGameStore",
                            content=Message(
                                (
                                    "{} ({})\n\n{}\n\n游戏由 {}{} 发行，"
                                    "将在 {} 结束免费游玩，戳上方链接领取吧~"
                                ).format(
                                    game_name,
                                    original_price,
                                    game["description"],
                                    dev_info,
                                    game_pub,
                                    end_date,
                                )
                            ),
                        ),
                    ]
                )
            except (AttributeError, IndexError, TypeError):
                logger.debug(f"处理游戏 {game_name} 时遇到应该忽略的错误\n{format_exc()}")
                pass
            except Exception as e:
                logger.error(f"组织 Epic 订阅消息错误 {e.__class__.__name__}\n{format_exc()}")
        # 返回整理为 CQ 码的消息字符串
        msgList.insert(
            0,
            MessageSegment.node_custom(
                user_id=2854196320,
                nickname="EpicGameStore",
                content=Message(f"{gameCnt} 款游戏现在免费！" if gameCnt else "暂未找到正在促销的游戏..."),
            ),
        )
        return msgList
