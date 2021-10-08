import json
import sys
from datetime import datetime

import nonebot
from httpx import AsyncClient
from nonebot.log import logger


resPath = nonebot.get_driver().config.resources_dir
if not resPath:
  raise ValueError(f"请在环境变量中添加 resources_dir 参数")


# 写入与读取订阅信息
# method="w" 写入时返回新增订阅结果字符串
# method="r" 读取时返回订阅状态字典
async def subscribeHelper(method="r", subType="", subject=""):
  try:
    with open(f"{resPath}epicfree/status.json", "r", encoding="UTF-8") as f:
      statusDict = json.load(f)
      f.close()
  except FileNotFoundError:
    statusDict = {"群聊": [], "私聊": []}
    with open(f"{resPath}epicfree/status.json", "w", encoding="UTF-8") as f:
      json.dump(statusDict, f, ensure_ascii=False, indent=2)
      f.close()
  except Exception as e:
    logger.error("获取 Epic 订阅 JSON 错误：" + str(sys.exc_info()[0]) + "\n" + str(e))
  # 读取时，返回订阅状态字典
  if method != "w":
    return statusDict
  # 写入时，将新的用户按类别写入至指定数组
  try:
    if subject in statusDict[subType]:
      return f"{subType}已经订阅过 Epic 限免游戏资讯了哦！"
    statusDict[subType].append(subject)
    with open(f"{resPath}epicfree/status.json", "w", encoding="UTF-8") as f:
      json.dump(statusDict, f, ensure_ascii=False, indent=2)
      f.close()
    return f"{subType}订阅 Epic 限免游戏资讯成功！"
  except Exception as e:
    logger.error("获取 Epic 订阅 JSON 错误：" + str(sys.exc_info()[0]) + "\n" + str(e))
    return f"{subType}订阅 Epic 限免游戏资讯失败惹.."


# 获取所有 Epic Game Store 促销游戏
# 方法参考：RSSHub /epicgames 路由
# https://github.com/DIYgod/RSSHub/blob/master/lib/routes/epicgames/index.js
async def getEpicGame():
  epic_url = "https://www.epicgames.com/store/backend/graphql-proxy"
  headers = {
    "Referer": "https://www.epicgames.com/store/zh-CN/",
    "Content-Type": "application/json; charset=utf-8",
  }
  data = {
    "query":
    "query searchStoreQuery($allowCountries: String, $category: String, $count: Int, $country: String!, $keywords: String, $locale: String, $namespace: String, $sortBy: String, $sortDir: String, $start: Int, $tag: String, $withPrice: Boolean = false, $withPromotions: Boolean = false) {\n Catalog {\n searchStore(allowCountries: $allowCountries, category: $category, count: $count, country: $country, keywords: $keywords, locale: $locale, namespace: $namespace, sortBy: $sortBy, sortDir: $sortDir, start: $start, tag: $tag) {\n elements {\n title\n id\n namespace\n description\n effectiveDate\n keyImages {\n type\n url\n }\n seller {\n id\n name\n }\n productSlug\n urlSlug\n url\n items {\n id\n namespace\n }\n customAttributes {\n key\n value\n }\n categories {\n path\n }\n price(country: $country) @include(if: $withPrice) {\n totalPrice {\n discountPrice\n originalPrice\n voucherDiscount\n discount\n currencyCode\n currencyInfo {\n decimals\n }\n fmtPrice(locale: $locale) {\n originalPrice\n discountPrice\n intermediatePrice\n }\n }\n lineOffers {\n appliedRules {\n id\n endDate\n discountSetting {\n discountType\n }\n }\n }\n }\n promotions(category: $category) @include(if: $withPromotions) {\n promotionalOffers {\n promotionalOffers {\n startDate\n endDate\n discountSetting {\n discountType\n discountPercentage\n }\n }\n }\n upcomingPromotionalOffers {\n promotionalOffers {\n startDate\n endDate\n discountSetting {\n discountType\n discountPercentage\n }\n }\n }\n }\n }\n paging {\n count\n total\n }\n }\n }\n}\n",
    "variables": {
      "allowCountries": "CN",
      "category": "freegames",
      "count": 1000,
      "country": "CN",
      "locale": "zh-CN",
      "sortBy": "effectiveDate",
      "sortDir": "asc",
      "withPrice": True,
      "withPromotions": True
    }
  }
  async with AsyncClient(headers=headers) as client:
    try:
      res = await client.post(epic_url, json=data, timeout=10.0)
      resJson = res.json()
      games = resJson["data"]["Catalog"]["searchStore"]["elements"]
      return games
    except Exception as e:
      logger.error("请求 Epic Store API 错误：" + str(sys.exc_info()[0]) + "\n" + str(e))
      return None


# 获取 Epic Game Store 免费游戏信息
# 处理免费游戏的信息方法借鉴 pip 包 epicstore_api 示例	
# https://github.com/SD4RK/epicstore_api/blob/master/examples/free_games_example.py
async def getEpicFree():
  games = await getEpicGame()
  if not games:
    return "Epic 可能又抽风啦，请稍后再试（"
  else:
    msg = ""
    for game in games:
      game_name = game["title"]
      game_corp = game["seller"]["name"]
      game_price = game["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
      # 赋初值以避免 local variable referenced before assignment
      game_dev, game_pub, game_thumbnail = (None, None, None)
      try:
        game_promotions = game["promotions"]["promotionalOffers"]
        upcoming_promotions = game["promotions"]["upcomingPromotionalOffers"]
        if not game_promotions and upcoming_promotions:
          # 促销暂未上线，但即将上线
          promotion_data = upcoming_promotions[0]["promotionalOffers"][0]
          start_date_iso, end_date_iso = (promotion_data["startDate"][:-1],
                                          promotion_data["endDate"][:-1])
          # 删除字符串中最后一个 "Z" 使 Python datetime 可处理此时间
          start_date = datetime.fromisoformat(start_date_iso).strftime(
            "%b.%d %H:%M")
          end_date = datetime.fromisoformat(end_date_iso).strftime("%b.%d %H:%M")
          msg += "\n由 {} 公司发行的游戏 {} ({}) 在 UTC 时间 {} 即将推出免费游玩，预计截至 {}。".format(
            game_corp, game_name, game_price, start_date, end_date)
        else:
          for image in game["keyImages"]:
            if image["type"] == "Thumbnail":
              game_thumbnail = image["url"]
          for pair in game["customAttributes"]:
            if pair["key"] == "developerName":
              game_dev = pair["value"]
            if pair["key"] == "publisherName":
              game_pub = pair["value"]
          # 如 game["customAttributes"] 未找到则均使用 game_corp 值
          game_dev = game_dev if game_dev != None else game_corp
          game_pub = game_pub if game_pub != None else game_corp
          game_desp = game["description"]
          end_date_iso = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"][:-1]
          end_date = datetime.fromisoformat(end_date_iso).strftime("%b.%d %H:%M")
          # API 返回不包含游戏商店 URL，此处自行拼接，可能出现少数游戏 404 请反馈
          game_url_part = (game["productSlug"].replace("/home", "")) if ("/home" in game["productSlug"]) else game["productSlug"]
          game_url = "https://www.epicgames.com/store/zh-CN/p/{}".format(game_url_part)
          msg += "[CQ:image,file={}]\n\nFREE now :: {} ({})\n{}\n此游戏由 {} 开发、{} 发行，将在 UTC 时间 {} 结束免费游玩，戳链接速度加入你的游戏库吧~\n{}\n".format(
            game_thumbnail, game_name, game_price, game_desp, game_dev, game_pub, end_date, game_url)
      except TypeError:
        pass
      except Exception as e:
        logger.error("组织 Epic 订阅消息错误：" + str(sys.exc_info()[0]) + "\n" + str(e))
    # 返回整理为 CQ 码的消息字符串
    return msg
