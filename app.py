from bs4 import BeautifulSoup
from flask import Flask, render_template, request,jsonify
import requests
import sqlite3
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

heroList = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
cssLink = "<link rel='stylesheet' href='http://opgg.dispnt.com/static/champion.css'>" \
          "<link rel='stylesheet' href='https://opgg-static.akamaized.net/css3Mobile/common.css'>"

def rune(championName):
    SelectedRuneName = []
    SelectedRuneImgLink = []
    SelectedRuneImgID = []
    url = "http://www.op.gg/champion/" + championName + "/statistics/"
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    RuneHtml = soup.find('div', {'class': 'rune-setting'})
    SelectedRuneHtml = RuneHtml.find_all(class_='perk-page__item--active')
    for SelectedRune in SelectedRuneHtml:
        SelectedRuneName.append(SelectedRune.find('img')['alt'])
        SelectedRuneImgLink.append(SelectedRune.find('img')['src'])
    for SelectedRune in SelectedRuneImgLink:
        SelectedRuneImgID.append(re.findall(r"\d\d\d\d.png", SelectedRune)[0])
    return SelectedRuneName, SelectedRuneImgID


def brief(championName):
    content = cssLink
    url = 'http://www.op.gg/champion/' + championName + '/statistics/'
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    soup.find('div', {'class': 'ratio-graph'}).decompose()
    content = soup.prettify()
    return content

@app.route('/b4')
def mainBeta():
    db = sqlite3.connect("ChampionNickname.sqlite")
    crsr = db.execute("select * from Name")
    championNickname = dict(crsr.fetchall())
    return render_template("MainBootstrap4.html", heroList=heroList, championNickname = championNickname)

@app.route('/')
def main():
    db = sqlite3.connect("ChampionNickname.sqlite")
    crsr = db.execute("select * from Name")
    championNickname = dict(crsr.fetchall())
    return render_template("Main.html", heroList=heroList, championNickname = championNickname)


@app.route('/rune')
def runeClicked():
    championName = request.args.get('championName')
    (SelectedRuneName, SelectedRuneImgID) = rune(championName=championName)
    return jsonify(SelectedRuneName)


@app.route('/brief')
def briefClicked():
    championName = request.args.get('championName')
    return brief(championName)

@app.route('/item')
def itemClicked():
    return("NOT COMPLETED YET")
    #championName = request.args.get('championName')
    #return item(championName)

if __name__ == '__main__':
    app.run()
