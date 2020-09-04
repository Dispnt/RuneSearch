import datetime
from RunePageExtract import *
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import sqlite3


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

heroList = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
lastUpdateDate = datetime.datetime.now()

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
def stringtodatetime(Datestr):
    datetime.datetime.strptime(Datestr,'%Y-%m-%d %H:%M')

@app.route('/update')
def update_heroList():
    global heroList,lastUpdateDate
    newUpdateDate = datetime.datetime.now()
    if(lastUpdateDate.day - newUpdateDate.day >=3):
        heroList = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
        lastUpdateDate = newUpdateDate
    else:
        return redirect(url_for("main"))

def brief(championName):
    url = 'http://www.op.gg/champion/' + championName + '/statistics/'
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    soup.find('div', {'class': 'ratio-graph'}).decompose()
    content = soup.prettify()
    return content

@app.route('/')
def main():
    db = sqlite3.connect("ChampionNickname.sqlite")
    crsr = db.execute("select * from Name")
    championNickname = dict(crsr.fetchall())

    return render_template("MainBootstrap4.html", heroList=heroList,lastUpdateDate=lastUpdateDate.strftime('%Y-%m-%d %H:%M'),championNickname=championNickname)

@app.route('/rune')
def runeClicked():
    championName = request.args.get('championName')
    (selectedRuneNames, selectedRuneImgIDs) = rune(championName=championName)
    MainRune1 = runeType(selectedRuneImgIDs[1][1])
    SubRune1 = runeType(selectedRuneImgIDs[1][4])

    MainRune2 = runeType(selectedRuneImgIDs[4][1])
    SubRune2 = runeType(selectedRuneImgIDs[4][4])

    return render_template("rune.html", mainRune1=MainRune1, subRune1=SubRune1, mainRune2=MainRune2, subRune2=SubRune2,
                           selectedRumeImgIDs=selectedRuneImgIDs, runetext=selectedRuneNames)


# {"1":["8112","8126","8138","8105","8234","8236"],
# "2":["8112","8126","8138","8105","8234","8236"],
# "3":["8112","8139","8138","8105","8313","8347"],
# "4":["8112","8139","8138","8105","8313","8321"]}
# {
# "1":["电刑","恶意中伤","眼球收集器","无情猎手","迅捷","风暴聚集"],
# "2":["电刑","恶意中伤","眼球收集器","无情猎手","迅捷","风暴聚集"],
# "3":["电刑","血之滋味","眼球收集器","无情猎手","完美时机","星界洞悉"],
# "4":["电刑","恶意中伤","眼球收集器","无情猎手","完美时机","饼干配送"]
# }

@app.route('/brief')
def briefClicked():
    championName = request.args.get('championName')
    return brief(championName)


if __name__ == '__main__':
    app.run()
