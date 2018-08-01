# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdctkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -c          城际
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
import sys
import datetime
from docopt import docopt
import requests
import json
from prettytable import PrettyTable
from stations import stations

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    if not arguments["<from>"] in stations or not arguments["<to>"] in stations:
        print("stations not recognized.")
        sys.exit()
    try:
        datetime.datetime.strptime(arguments["<date>"], "%Y-%m-%d")
    except ValueError:
        print("invalid datetime.")
        sys.exit()
    # print(arguments)
    return arguments

def get_ticket_info(arguments):
    # get url based on user input
    # url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-07-30&leftTicketDTO.from_station=GZQ&leftTicketDTO.to_station=SZQ&purpose_codes=ADULT"
    from_station = stations[arguments["<from>"]]
    to_station = stations[arguments["<to>"]]
    train_date = arguments["<date>"]
    purpose_codes = "ADULT"
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}".format(train_date, from_station, to_station, purpose_codes)

    # send request and parse html
    res = requests.get(url)
    try:
        data = json.loads(res.text)
    except:
        print("no lines found.")
        sys.exit()
    data = data["data"]
    stations_derivative = data["map"]
    result = data["result"]
    
    # generate ticket table
    ticket_classes = ""
    for key,value in arguments.items():
        if key.startswith("-") and value:
            ticket_classes += key[1]
    ticket_classes = ticket_classes.upper()
    tickets = PrettyTable()
    # # full tokens
    # tickets.field_names = ["hash0","预订","hash1","车次","车站1","车站2","车站3","车站4","出发时间","到达时间","历时","N","hash2","日期","num1","Q","num2","num3","num4","num5","status1","status2","status3","status4","status5","status6","status7","status8","status9","status10","status11","status12","status13","status14","hash3","hash4","0_1"]
    tickets.field_names = ["车次","出发站","到达站","出发时间","到达时间","历时","商务座特等座","一等座","二等座","软卧","硬卧","硬座","无座"]
    for ticket in result:
        tokens = ticket.split("|")
        if tokens[3][0] in ticket_classes:
            from_station_status = stations_derivative[tokens[6]] + (" (始)" if tokens[4] == tokens[6] else " (过)")
            to_station_status = stations_derivative[tokens[7]] + (" (终)" if tokens[5] == tokens[7] else " (过)")
            tickets.add_row([tokens[3],from_station_status,to_station_status,tokens[8],tokens[9],tokens[10],tokens[32],tokens[31],tokens[30],tokens[23],tokens[28],tokens[29],tokens[26]])
    print(tickets)


if __name__ == '__main__':
    arguments = cli()
    get_ticket_info(arguments)
