from bs4 import BeautifulSoup
import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; R8207 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36; OP.GG Mobile Android (4.8.0); X-DEVICE-WIDTH=540',
    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}

def rune(championName):
    SelectedRuneName = {}
    SelectedRuneImgLink = []
    SelectedRuneImgID = []
    url = "http://www.op.gg/champion/" + championName + "/statistics/"
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    RuneHtml = soup.find('div', {'class': 'rune-setting'})
    SelectedRuneHtml = RuneHtml.find_all(class_='perk-page__item--active')
    key_and_count = [1,1]
    for SelectedRune in SelectedRuneHtml:
        if key_and_count[1]<=6:
            SelectedRuneName.setdefault(key_and_count[0], []).append(SelectedRune.find('img')['alt'])
        else:
            key_and_count = [key_and_count[0] + 1,1]
            SelectedRuneName.setdefault(key_and_count[0], []).append(SelectedRune.find('img')['alt'])
        key_and_count[1]=key_and_count[1] + 1
        SelectedRuneImgLink.append(SelectedRune.find('img')['src'])
    for SelectedRune in SelectedRuneImgLink:
        SelectedRuneImgID.append(re.findall(r"\d\d\d\d.png", SelectedRune)[0])
    return SelectedRuneName, SelectedRuneImgID



#(SelectedRuneName, SelectedRuneImgID) = rune(championName = "Annie")
# print(SelectedRuneName)