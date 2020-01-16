from RunePageExtract import *
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import requests
import sqlite3


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

heroList = requests.post("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}


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
    return render_template("MainBootstrap4.html", heroList=heroList, championNickname=championNickname)

@app.route('/rune')
def runeClicked():
    championName = request.args.get('championName')
    (selectedRuneNames, selectedRuneImgIDs) = rune(championName=championName)
    selectedMainRune = runelist(selectedRuneImgIDs[1])
    selectedSubRune = runelist(selectedRuneImgIDs[4])
    return render_template("rune.html", mainRune=selectedMainRune, subRune=selectedSubRune, selectedRumeImgIDs=selectedRuneImgIDs, runetext=selectedRuneNames)
    # return jsonify(SelectedRuneName)
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

@app.route('/item')
def itemClicked():
    return("NOT COMPLETED YET")
    #championName = request.args.get('championName')
    #return item(championName)

if __name__ == '__main__':
    app.run()
