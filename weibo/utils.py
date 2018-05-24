import requests

source_url = "http://www.baidu.com"
url = "https://api.weibo.com/2/statuses/share.json"
access_token = "2.00u9_1SDkwujID00481312be3iGYyC"


def post_text(text, source_url=source_url):
    status = text + " " + source_url
    payload = {
        "access_token": access_token,
        "status": status
    }
    r = requests.post(url, data=payload)
    print(r.text)


def post_picture(text, pic, source_url=source_url):
    status = text + " " + source_url
    payload = {
        "access_token": access_token,
        "status": status
    }
    files = {
        "pic": open(pic, "rb")
    }
    r = requests.post(url, data=payload, files=files)
    print(r.text)
