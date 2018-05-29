#coding:utf-8
#https://blog.csdn.net/baidu_26678247/article/details/75086587
import requests
from bs4 import BeautifulSoup
import re
import os


req_url_base = "https://www.qu.la/book/"   #小说主地址（笔趣阁）
id = 115                                   #佛本是道
req_url = req_url_base + str(id)

# id specific: req_header can be got following the header link
req_header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "UM_distinctid=163ab086d7a65d-0c46c3f281729f-39614807-1fa400-163ab086d7b828; CNZZDATA1261736110=1924441053-1527578746-https%253A%252F%252Fwww.google.com.hk%252F%7C1527578746; tanwanhf_10487=1; tanwanpf_10483=1; cscpvrich8662_fidx=1; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1527582847; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1527582847",
    "Host": "www.qu.la",
    "Referer": "https://www.google.com.hk/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

res = requests.get(req_url, params=req_header)
soups = BeautifulSoup(res.text, "html.parser")
title = soups.select("#wrapper .box_con #maininfo #info h1")[0].text
info = soups.select("#wrapper .box_con #maininfo #info p")
author = info[0].text
last_update_time = info[2].text
last_update_name = info[3].text
intro = soups.select("#wrapper .box_con #maininfo #intro")[0].text
print("title: " + title)
pages = soups.select("#wrapper .box_con #list dl dd a")

save_path = "../res/" + title
if not os.path.exists(save_path):
    os.mkdir(save_path)
for page in pages:
    page_index = page["href"].split(".")[0]
    r = requests.get(req_url+"/"+page_index+".html", params=req_header)
    soup = BeautifulSoup(r.text, "html.parser")
    page_name = soup.select("#wrapper .content_read .box_con .bookname h1")[0].text
    page_text = soup.select("#wrapper .content_read .box_con #content")[0]
    for ss in page_text.select("script"):
        ss.decompose()
    page_text = re.sub("\s+", "\r\n\t", page_text.text).strip("\r\n")

    try:
        file = open(save_path+"/"+page_name+".txt", "ab+")
    except:
        forbid = r"[\/\\\:\*\?\"\<\>\|]"  # cannot be used in file names
        page_name = re.sub(forbid, " ", page_name)
        file = open(save_path + "/" + page_name + ".txt", "ab+")
    file.write(("\r" + page_name + "\r\n").encode("UTF-8"))
    file.write(page_text.encode("UTF-8"))
    file.close()
    print("downloaded: " + page_name)

