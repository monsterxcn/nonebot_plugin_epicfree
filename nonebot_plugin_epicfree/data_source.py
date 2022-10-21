import json
import os
from datetime import datetime
from pathlib import Path
from traceback import format_exc
from typing import Dict, List, Literal, Union

from httpx import AsyncClient
from nonebot import get_driver
from nonebot.log import logger

try:
    resPath = Path(get_driver().config.resources_dir) / "epicfree"
    assert os.path.exists(resPath)
    cache = resPath / "status.json"
except (AttributeError, AssertionError):
    resPath = Path() / "data" / "epicfree"
    if not os.path.exists(resPath):
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
    epic_url = (
        "https://store-site-backend-static-ipv4.ak.epicgames.com"
        "/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN"
    )
    headers = {
        "Referer": "https://www.epicgames.com/store/zh-CN/",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
        ),
    }
    async with AsyncClient(proxies={"all://": None}) as client:
        try:
            res = await client.get(epic_url, headers=headers, timeout=10.0)
            resJson = res.json()
            games = resJson["data"]["Catalog"]["searchStore"]["elements"]
            # with open(f"{resPath}epicfree/api.json", "w", encoding="utf-8") as f:
            #     json.dump(games, f, ensure_ascii=False, indent=2)
            return games
        except Exception as e:
            logger.error(f"请求 Epic Store API 错误 {type(e)}：{e}")
            return []


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def getEpicFree() -> str:
    games = await getEpicGame()
    if not games:
        return "Epic 可能又抽风啦，请稍后再试（"
    else:
        logger.debug(f"获取到游戏：{('、'.join(game['title'] for game in games))}")
        msgList = []
        for game in games:
            game_name = ""
            try:
                game_name = game["title"]
                game_corp = game["seller"]["name"]
                game_price = game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
                game_promotions = game["promotions"]["promotionalOffers"]
                upcoming_promotions = game["promotions"]["upcomingPromotionalOffers"]
                game_thumbnail, game_dev, game_pub = None, game_corp, game_corp
                if not game_promotions and upcoming_promotions:
                    logger.info(f"即将推出免费游玩的游戏：{game_name}({game_price})")
                    continue  # 促销即将上线，跳过
                else:
                    for image in game["keyImages"]:
                        # 修复部分游戏无法找到图片
                        # https://github.com/HibiKier/zhenxun_bot/commit/92e60ba141313f5b28f89afdfe813b29f13468c1
                        if (
                            image.get("url")
                            and not game_thumbnail
                            and image["type"]
                            in [
                                "Thumbnail",
                                "VaultOpened",
                                "DieselStoreFrontWide",
                                "OfferImageWide",
                            ]
                        ):
                            game_thumbnail = image["url"]
                            break
                    for pair in game["customAttributes"]:
                        if pair["key"] == "developerName":
                            game_dev = pair["value"]
                        elif pair["key"] == "publisherName":
                            game_pub = pair["value"]
                    game_desp = game["description"]
                    date_iso = game_promotions[0]["promotionalOffers"][0]["endDate"][:-1]
                    end_date = datetime.fromisoformat(date_iso).strftime("%b.%d %H:%M")
                    # API 返回不包含游戏商店 URL，此处自行拼接，可能出现少数游戏 404 请反馈
                    if game.get("productSlug"):
                        game_url = "https://store.epicgames.com/zh-CN/p/{}".format(
                            game["productSlug"].replace("/home", "")
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
                    msgList.append(
                        (
                            "{}FREE now :: {} ({})\n\n{}\n\n{}，"
                            "将在 UTC 时间 {} 结束免费游玩，戳链接领取吧~\n{}"
                        ).format(
                            (
                                f"[CQ:image,file={game_thumbnail}]\n\n"
                                if game_thumbnail
                                else ""
                            ),
                            game_name,
                            game_price,
                            game_desp,
                            (
                                f"游戏由 {game_pub} 发行"
                                if game_dev == game_pub
                                else f"游戏由 {game_dev} 开发、{game_pub} 发行"
                            ),
                            end_date,
                            game_url,
                        )
                    )
            except (AttributeError, IndexError, TypeError):
                logger.debug(f"处理游戏 {game_name} 时遇到应该忽略的错误\n{format_exc()}")
                pass
            except Exception as e:
                logger.error(f"组织 Epic 订阅消息错误 {type(e)}\n{format_exc()}")
        # 返回整理为 CQ 码的消息字符串
        msg = "\n\n---\n\n".join(msgList) if len(msgList) else "暂未找到正在促销的游戏..."
        return msg
