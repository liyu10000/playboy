# useful links
# https://www.cnblogs.com/feixuelove1009/p/5955332.html
# http://open.weibo.com/apps/2877552850/info/basic
# https://api.weibo.com/oauth2/default.html?code=7e63ff9aec4287a55905422796481b34
#
# https://www.itengli.com/python_weibo/
# http://www.bkjia.com/Pythonjc/1124014.html
# http://www.cnblogs.com/5long/p/4766909.html
# https://gist.github.com/mrluanma/3621775
# https://github.com/chaolongzhang/sinaWeibo/blob/master/spider/cnbeta.py
# https://lz5z.com/Python%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1%E7%9A%84%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F/
import utils
import spider
import time
import random


def auto_run(n):
    while True:
        i = random.randint(0, 2)
        if i == 0:
            item = spider.get_miaopai()
        elif i == 1:
            item = spider.get_cnblog()
        else:
            item = spider.get_cnbeta()
        if item:
            utils.post_text(text=item[0], source_url=item[1])
            time.sleep(n)


if __name__ == "__main__":
    # utils.post_text(text="A new post.")
    # utils.post_picture(text="A new post", pic="./res/river.jpg")
    # item = spider.get_weather(city="Guangzhou")
    # utils.post_text(text=item[0], source_url=item[1])
    # item = spider.get_miaopai()
    # utils.post_text(text=item[0], source_url=item[1])
    # item = spider.get_cnblog()
    # utils.post_text(text=item[0], source_url=item[1])
    # item = spider.get_cnbeta()
    # utils.post_text(text=item[0], source_url=item[1])
    auto_run(1800)
