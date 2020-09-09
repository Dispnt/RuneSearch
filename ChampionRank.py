from bs4 import BeautifulSoup
import requests
import json

header = {
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
url = "https://www.op.gg/champion/statistics"

sourcecode = requests.get(url, headers=header).text
soup = BeautifulSoup(sourcecode, "html.parser")

Top = []
Jungle = []
Mid = []
Adc = []
Support = []

topHtml = soup.find("tbody", class_="tabItem champion-trend-tier-TOP")
jungleHtml = soup.find("tbody", class_="tabItem champion-trend-tier-JUNGLE")
midHtml = soup.find("tbody", class_="tabItem champion-trend-tier-MID")
adcHtml = soup.find("tbody", class_="tabItem champion-trend-tier-ADC")
supportHtml = soup.find("tbody", class_="tabItem champion-trend-tier-SUPPORT")

for championName in topHtml.find_all("div", class_="champion-index-table__name"):
    Top.append(championName.get_text())
for championName in jungleHtml.find_all("div", class_="champion-index-table__name"):
    Jungle.append(championName.get_text())
for championName in midHtml.find_all("div", class_="champion-index-table__name"):
    Mid.append(championName.get_text())
for championName in adcHtml.find_all("div", class_="champion-index-table__name"):
    Adc.append(championName.get_text())
for championName in supportHtml.find_all("div", class_="champion-index-table__name"):
    Support.append(championName.get_text())

posList = ["Top", "Jungle", "Mid", "Adc", "Support"]

data = {pos: globals()[pos] for pos in posList}

print(json.dumps(data))
