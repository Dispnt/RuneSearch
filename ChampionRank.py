from bs4 import BeautifulSoup
import requests
import json

header = {
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
url = "https://www.op.gg/champion/statistics"

sourcecode = requests.get(url,headers=header).text
soup = BeautifulSoup(sourcecode, "html.parser")

topRank=[]
jungleRank =[]
midRank = []
adcRank=[]
supportRank = []

top = soup.find("tbody",class_="tabItem champion-trend-tier-TOP")
jungle = soup.find("tbody",class_="tabItem champion-trend-tier-JUNGLE")
mid = soup.find("tbody",class_="tabItem champion-trend-tier-MID")
adc = soup.find("tbody",class_="tabItem champion-trend-tier-ADC")
support = soup.find("tbody",class_="tabItem champion-trend-tier-SUPPORT")


for i in top.find_all("div",class_="champion-index-table__name"):
    topRank.append(i.get_text())
for i in jungle.find_all("div",class_="champion-index-table__name"):
    jungleRank.append(i.get_text())
for i in mid.find_all("div",class_="champion-index-table__name"):
    midRank.append(i.get_text())
for i in adc.find_all("div",class_="champion-index-table__name"):
    adcRank.append(i.get_text())
for i in support.find_all("div",class_="champion-index-table__name"):
    supportRank.append(i.get_text())

lists = ['topRank', 'jungleRank', 'midRank','adcRank','supportRank']

data = {listname: globals()[listname] for listname in lists}

print(json.dumps(data))