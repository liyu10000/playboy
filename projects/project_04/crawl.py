import requests
import csv
from bs4 import BeautifulSoup

url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice={minprice}_{maxprice}"

page = 0
minprice = 2000
maxprice = 4000

csv_file = open("rent_new.csv","w",newline="")
csv_writer = csv.writer(csv_file, delimiter=",")

while True:
	page += 1
	url_page = url.format(page=page,minprice=minprice,maxprice=maxprice)
	print("fetch: " + url_page)
	response = requests.get(url_page)
	html = BeautifulSoup(response.text, "html5lib")
	# get all li elements under class=list
	house_list = html.select("ul.list > li")
	if not house_list or page > 1000:
		break

	for house in house_list:
		house_title = house.select("h2")[0].string
		house_money = house.select(".money")[0].select("b")[0].string
		house_url = "http://bj.58.com/{}".format(house.select("a")[0]["href"])
		csv_writer.writerow([house_title, house_money, house_url])

csv_file.close()