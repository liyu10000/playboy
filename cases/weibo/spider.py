import requests
import random
import bs4


def get_weather(city):
    cities = {"Beijing": "101010100", "Shanghai": "101020100", "Shenzhen": "101280601", "Guangzhou": "101280101"}
    if city not in cities:
        return
    weather_url = "http://www.weather.com.cn/data/sk/" + cities[city] + ".html"
    r = requests.get(weather_url)
    r.encoding = "utf-8"
    weather_info = "weather: " + r.json()["weatherinfo"]["city"] + "\n" \
                   + "温度: " + r.json()["weatherinfo"]["temp"] + "度\n" \
                   + "湿度: " + r.json()["weatherinfo"]["SD"] + "\n" \
                   + r.json()["weatherinfo"]["WD"] + ": " + r.json()["weatherinfo"]["WS"] + "\n"
    item = (weather_info, weather_url)
    return item


def get_miaopai():
    miaopai_url = "http://www.miaopai.com/miaopai/index_api?cateid=2002&per=50&page=1"
    r = requests.get(miaopai_url)
    r.encoding = "utf-8"
    json_text = r.json()
    count = len(json_text["result"])
    if count == 0:
        return
    i = random.randint(0, count-1)
    scid = json_text["result"][i]["channel"]["scid"]
    url = "http://www.miaopai.com/show/%s.htm" % scid
    title = "miaopai: " + json_text["result"][i]["channel"]["ext"]["_t"]
    item = (title, url)
    return item


def get_cnblog():
    cnblog_url = "http://www.cnblogs.com"
    r = requests.get(cnblog_url)
    r.encoding = "utf-8"
    html = r.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    items = soup.find_all(attrs={"class": "post_item_body"})
    count = len(items)
    if count == 0:
        return
    i = random.randint(0, count-1)
    title = "cnblog: " + items[i].a.string.strip()
    url = items[i].a.get("href")
    item = (title, url)
    return item


def get_cnbeta():
    cnbeta_url = "http://www.cnbeta.com"
    r = requests.get(cnbeta_url)
    r.encoding = "utf-8"
    html = r.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    items_area = soup.find(attrs={"class": "items-area"})
    items = items_area.find_all(attrs={"class": "item"})
    count = len(items)
    if count == 0:
        return
    i = random.randint(0, count-1)
    title = "cnbeta: " + items[i].a.string.strip()
    url = items[i].a.get("href")
    item = (title, url)
    return item
