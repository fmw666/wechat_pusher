import json
import random
from time import time, localtime
from typing import Dict
from requests import get, post
from bs4 import BeautifulSoup
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os


weekday_map = {
    "Monday": "周一",
    "Tuesday": "周二",
    "Wednesday": "周三",
    "Thursday": "周四",
    "Friday": "周五",
    "Saturday": "周六",
    "Sunday": "周日"
}


def get_color() -> str:
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token() -> str:
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()["access_token"]
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token


def get_time_zone() -> Dict:
    base_url = "https://www.timeapi.io/api/Time/current/zone?timeZone="
    zones = ["Europe/London", "Asia/Shanghai"]
    results = {}
    for zone in zones:
        url = base_url + zone
        content = json.loads(get(url).content)
        results[zone] = f"{content.get('time')} {content.get('date')} {weekday_map[content.get('dayOfWeek')]}"

    return results


def get_uk_weather() -> Dict:
    # 获取 格拉斯哥 天气
    url = "https://weather.com/zh-CN/weather/today/l/5a88f118aa4d4ed2e88e87e88f8a8986b20bbbbe8f0beabe18b7237697887197"
    html = get(url).text
    bsObj = BeautifulSoup(html, "html.parser")

    current_temp = bsObj.select(".CurrentConditions--tempValue--MHmYY")[0].text
    weather = bsObj.select(".CurrentConditions--phraseValue--mZC_p")[0].text
    weather_range = bsObj.select(".CurrentConditions--tempHiLoValue--3T1DG")[0].text
    return {
        "current_temp": current_temp,
        "weather": weather,
        "weather_range": weather_range
    }


def get_weather() -> Dict:
    # 获取 深圳 天气
    url = "https://weather.com/zh-CN/weather/today/l/4945e1616a82b28a995f412bf561340d96d0d1941d2980e107c9fd4bf73be75e"
    html = get(url).text
    bsObj = BeautifulSoup(html, "html.parser")

    current_temp = bsObj.select(".CurrentConditions--tempValue--MHmYY")[0].text
    weather = bsObj.select(".CurrentConditions--phraseValue--mZC_p")[0].text
    weather_range = bsObj.select(".CurrentConditions--tempHiLoValue--3T1DG")[0].text
    return {
        "current_temp": current_temp,
        "weather": weather,
        "weather_range": weather_range
    }
    # # 城市id
    # try:
    #     city_id = cityinfo.cityInfo[province][city]["AREAID"]
    # except KeyError:
    #     print("推送消息失败，请检查省份或城市是否正确")
    #     os.system("pause")
    #     sys.exit(1)
    # # city_id = 101280101
    # # 毫秒级时间戳
    # t = (int(round(time() * 1000)))
    # headers = {
    #     "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    #                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    # }
    # url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    # response = get(url, headers=headers)
    # response.encoding = "utf-8"
    # response_data = response.text.split(";")[0].split("=")[-1]
    # response_json = eval(response_data)
    # # print(response_json)
    # weatherinfo = response_json["weatherinfo"]
    # # 天气
    # weather = weatherinfo["weather"]
    # # 最高气温
    # temp = weatherinfo["temp"]
    # # 最低气温
    # tempn = weatherinfo["tempn"]
    # return {
    #     "city": city,
    #     "weather": weather,
    #     "max_temperature": temp,
    #     "min_temperature": tempn
    # }


def get_birthday(birthday, year, today) -> str:
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_ciba() -> Dict:
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return {
        "note_en": note_en,
        "note_ch": note_ch
    }


def send_message(to_user, access_token, time_zones, uk_weather, zh_weather, note):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取日子的日期格式
    love_date = datetime.strptime(config["love_date"], "%Y-%m-%d").date()
    separate_date = datetime.strptime(config["separate_date"], "%Y-%m-%d").date()
    meet_date = datetime.strptime(config["meet_date"], "%Y-%m-%d").date()
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    separate_days = str(today.__sub__(separate_date)).split(" ")[0]
    meet_days = str(meet_date.__sub__(today)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "timezone": {
                "value": time_zones.get('Asia/Shanghai')
            },
            "uk_timezone": {
                "value": time_zones.get('Europe/London')
            },
            "uk_city": {
                "value": "格拉斯哥 · 苏格兰 · 英国",
                "color": "#3CB371"
            },
            "uk_temperature": {
                "value": uk_weather.get("current_temp"),
                "color": "#4169E1"
            },
            "uk_weather": {
                "value": uk_weather.get("weather"),
                "color": "#4169E1"
            },
            "uk_weather_range": {
                "value": uk_weather.get("weather_range"),
                "color": "#4169E1"
            },
            "city": {
                "value": "深圳 · 广东 · 中国",
                "color": "#3CB371"
            },
            "weather": {
                "value": zh_weather.get("weather"),
                "color": "#4169E1"
            },
            "temperature": {
                "value": zh_weather.get("current_temp"),
                "color": "#4169E1"
            },
            "weather_range": {
                "value": zh_weather.get("weather_range"),
                "color": "#4169E1"
            },
            "love_date": {
                "value": config["love_date"]
            },
            "love_day": {
                "value": love_days,
                "color": "#EB524D"
            },
            "separate": {
                "value": f"距离上次相遇已经 {separate_days} 天 😭"
            },
            "meet": {
                "value": f"距离下次相遇还剩 {meet_days} 天 😘😘"
            },
            "note_en": {
                "value": note.get("note_en"),
                "color": "#00BFFF"
            },
            "note_ch": {
                "value": note.get("note_ch"),
                "color": "#F0C832"
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = f"今天{value['name']}生日哦，祝{value['name']}生日快乐！"
        else:
            birthday_data = f"{value['name']}生日还有 {birth_day} 天"
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": "#9400D3"}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.json", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.json文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 获取时区信息
    time_zones = get_time_zone()
    # 传入省份和市获取天气信息（默认格拉斯哥和成都）
    uk_weather = get_uk_weather()
    zh_weather = get_weather()
    # 获取词霸每日金句
    note = get_ciba()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, time_zones, uk_weather, zh_weather, note)
    os.system("pause")
