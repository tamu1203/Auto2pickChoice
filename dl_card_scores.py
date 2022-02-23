import time
import requests
from bs4 import BeautifulSoup


def dl_card_scores(craft_num):
    forest = 'https://shadowverse.gamewith.jp/article/show/36076'
    sword = 'https://shadowverse.gamewith.jp/article/show/36082'
    rune = 'https://shadowverse.gamewith.jp/article/show/36081'
    dragon = 'https://shadowverse.gamewith.jp/article/show/36080'
    shadow = 'https://shadowverse.gamewith.jp/article/show/36079'
    blood = 'https://shadowverse.gamewith.jp/article/show/36078'
    haven = 'https://shadowverse.gamewith.jp/article/show/36077'
    portal = 'https://shadowverse.gamewith.jp/article/show/83018'
    urls = [forest, sword, rune, dragon, shadow, blood, haven, portal]

    r = requests.get(urls[craft_num])
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table', class_='sorttable')
    rows = []
    for table in tables:
        rows.extend(table.find_all('tr'))

    card_scores = {}
    for row in rows:
        dictRow = []
        for cell in row.find_all(['td', 'th']):
            dictRow.append(cell.get_text())
        if dictRow[0] != '名前\n':
            try:
                card_score = float(dictRow[2].replace('点', ''))
            except ValueError:
                continue
            card_name = dictRow[0].replace('\n', '')
            card_scores[card_name] = card_score
    time.sleep(1)
    return card_scores


def main():
    print(dl_card_scores())


if __name__ == '__main__':
    main()
