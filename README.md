# Auto2pickChoicer
シャドウバースの2pickのカード選択画面からカード情報を取得するプログラム。
現時点では2pickの画像選択画面のカードデータを取得する段階まで完成した。
どちらを選ぶかの戦略部分の実装に時間がかかると判断したため、一旦公開します。

# DEMO
 
"hoge"の魅力が直感的に伝えわるデモ動画や図解を載せる
 
# Features
 

 
# Requirement
## Repository
shadowverse-portal https://github.com/tamu1203/shadowverse-portal
## Module
opencv-contrib-python
opencv-python
tqdm

# Installation
```bash
git clone https://github.com/tamu1203/shadowverse-portal
git clone https://github.com/tamu1203/Auto2pickChoice
pip install opencv-contrib-python
pip install opencv-python
pip install tqdm
```

# Usage
## shadowverse-portal
```bash
python create_json.py
python dl_card_imgs.py json_ja/all.json
```
ダウンロードされたcard_imgsフォルダをAuto2pickChoice/pictures/にコピーする。
ダウンロードされたjson_jaフォルダをAuto2pickChoice直下にコピーする。
## Auto2pickChoice
```bash
python descripter_cash.py
python present_cards.py
```

# Note
先にdescripter_cash.pyを実行して下さい
 
# License
"Auto2pickChoice" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).