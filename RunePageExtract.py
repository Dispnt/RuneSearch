from bs4 import BeautifulSoup
import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}

resoveImg = [["8437", "8439", "8465"],
             ["8446", "8463", "8401"],
             ["8429", "8444", "8473"],
             ["8451", "8453", "8242"]]  # 坚决绿

inspirationImg = [["8351", "8360", "8358"],
                  ["8306", "8304", "8313"],
                  ["8321", "8316", "8345"],
                  ["8347", "8410", "8352"]]  # 启迪蓝

sorceryImg = [["8214", "8229", "8230"],
              ["8224", "8226", "8275"],
              ["8210", "8234", "8233"],
              ["8237", "8232", "8236"]]  # 巫术紫

dominationImg = [["8112", "8124", "8128", "9923"],
                 ["8126", "8139", "8143"],
                 ["8136", "8120", "8138"],
                 ["8135", "8134", "8105", "8106"]]  # 主宰红

precisionImg = [["8005", "8008", "8021", "8010"],
                ["9101", "9111", "8009"],
                ["9104", "9105", "9103"],
                ["8014", "8017", "8299"]]  # 精密黄


def rune(championName):
    SelectedRuneName = {}
    SelectedRuneImgLink = []
    SelectedRuneImgID = []
    url = "http://www.op.gg/champion/" + championName + "/statistics/"
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    RuneHtml = soup.find('div', {'class': 'rune-setting'})
    SelectedRuneHtml = RuneHtml.find_all(class_='perk-page__item--active')
    key_and_count = [1, 1]
    for SelectedRune in SelectedRuneHtml:
        if key_and_count[1] <= 6:
            SelectedRuneName.setdefault(key_and_count[0], []).append(SelectedRune.find('img')['alt'])
        else:
            key_and_count = [key_and_count[0] + 1, 1]
            SelectedRuneName.setdefault(key_and_count[0], []).append(SelectedRune.find('img')['alt'])
        key_and_count[1] = key_and_count[1] + 1
        SelectedRuneImgLink.append(SelectedRune.find('img')['src'])
    for SelectedRune in SelectedRuneImgLink:
        if len(SelectedRuneImgID) <= 6:
            SelectedRuneImgID.append(re.findall(r"\d\d\d\d", SelectedRune)[0])
    return SelectedRuneName, SelectedRuneImgID


def runelist(selectedRuneImgIDs, row=1):
    if selectedRuneImgIDs in resoveImg[row]:
        return resoveImg
    elif selectedRuneImgIDs in inspirationImg[row]:
        return inspirationImg
    elif selectedRuneImgIDs in sorceryImg[row]:
        return sorceryImg
    elif selectedRuneImgIDs in dominationImg[row]:
        return dominationImg
    elif selectedRuneImgIDs in precisionImg[row]:
        return precisionImg
    else:
        return runelist(selectedRuneImgIDs, 2)

# (SelectedRuneNames, SelectedRuneImgIDs) = rune(championName = "Galio")
# print(SelectedRuneNames)
# {1: ['电刑', '恶意中伤', '眼球收集器', '无情猎手', '迅捷', '风暴聚集'], 2: ['电刑', '恶意中伤', '眼球收集器', '无情猎手', '迅捷', '风暴聚集'], 3: ['电刑', '血之滋味', '眼球收集器', '无情猎手', '完美时机', '星界洞悉'], 4: ['电刑', '恶意中伤', '眼球收集器', '无情猎手', '完美时机', '饼干配送']}
# print(SelectedRuneImgIDs)
# SelectedRuneImgID1 = ['8128', '8124', '8138', '8105', '8234', '8236', '8112', '8126', '8138', '8105', '8234', '8236','8112', '8139', '8138', '8105', '8313', '8347', '8112', '8126', '8138', '8105', '8313', '8345']
# print(len(resoveImg[0]))
