from bs4 import BeautifulSoup
import requests
import json
from flask import jsonify

header = {
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
url = "https://www.op.gg/champion/statistics"

topRank = []
jungleRank = []
midRank = []
adcRank = []
supportRank = []


def championRank():
    sourcecode = requests.get(url).text
    soup = BeautifulSoup(sourcecode, "html.parser")

    topHtml = soup.find("tbody", class_="tabItem champion-trend-tier-TOP")
    jungleHtml = soup.find("tbody", class_="tabItem champion-trend-tier-JUNGLE")
    midHtml = soup.find("tbody", class_="tabItem champion-trend-tier-MID")
    adcHtml = soup.find("tbody", class_="tabItem champion-trend-tier-ADC")
    supportHtml = soup.find("tbody", class_="tabItem champion-trend-tier-SUPPORT")

    for championName in topHtml.find_all("div", class_="champion-index-table__name"):
        topRank.append(championName.get_text())
    for championName in jungleHtml.find_all("div", class_="champion-index-table__name"):
        jungleRank.append(championName.get_text())
    for championName in midHtml.find_all("div", class_="champion-index-table__name"):
        midRank.append(championName.get_text())
    for championName in adcHtml.find_all("div", class_="champion-index-table__name"):
        adcRank.append(championName.get_text())
    for championName in supportHtml.find_all("div", class_="champion-index-table__name"):
        supportRank.append(championName.get_text())

    posList = ["topRank", "jungleRank", "midRank", "adcRank", "supportRank"]

    data = {pos: globals()[pos] for pos in posList}

    return topRank, jungleRank, midRank, adcRank, supportRank
