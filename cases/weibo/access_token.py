# https://www.itengli.com/python_weibo/
import requests

url_get_token = "https://api.weibo.com/oauth2/access_token"
#构建POST参数
payload = {
"client_id":"2877552850",
"client_secret":"ec5bc37de51e528e1e6b7165400d8153",
"grant_type":"authorization_code",
"code":"7e63ff9aec4287a55905422796481b34",
"redirect_uri":"https://api.weibo.com/oauth2/default.html"
}

#POST请求
r = requests.post(url_get_token,data=payload)
#输出响应信息
print(r.text)

# redirect page: https://api.weibo.com/oauth2/default.html
# {"access_token":"2.00u9_1SDkwujID00481312be3iGYyC",
#  "remind_in":"157679999",
#  "expires_in":157679999,
#  "uid":"3019213932",
#  "isRealName":"true"}
