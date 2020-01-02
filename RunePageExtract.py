from app import *

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


(SelectedRuneName, SelectedRuneImgID) = rune(championName = "Annie")
for a in SelectedRuneName:
    print(a)
for b in SelectedRuneImgID:
    print(b)