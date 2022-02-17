# Auto2pickChoicer
 シャドウバースの2pickのデッキ作成を自動化するプロジェクトです。

 (シャドウバース公式サイト https://shadowverse.jp/)

 現時点では、2pickの画像選択画面のカードデータを取得する段階まで完成しました。

 どちらを選ぶかの戦略部分の実装に時間がかかると判断したため、一旦公開します。

# DEMO
以下の画面のカード情報(カード名・カードID・レアリティ・効果等)を取得できます。
 ![Test Image 1](pictures/portal_craft/1.jpg)
# Features
 
 pickleでキャッシュすることで処理速度を0.5倍に短縮しました。

 また、可読性の高いコードを意識しました。
 
# Requirement
以下のリポジトリは、このプログラムで使用するjsonとimageをダウンロードするためのものです。
## Repository
 shadowverse-portal https://github.com/tamu1203/shadowverse-portal
## Module
 opencv-contrib-python

 opencv-python

 tqdm

# Installation/Setup
```bash
git clone https://github.com/tamu1203/shadowverse-portal
git clone https://github.com/tamu1203/Auto2pickChoice
pip install opencv-contrib-python
pip install opencv-python
pip install tqdm
```
## shadowverse-portal
```bash
python create_json.py
python dl_card_imgs.py json_ja/all.json
```
ダウンロードされたcard_imgsフォルダをAuto2pickChoice/pictures以下にコピーする。

ダウンロードされたjson_jaフォルダをAuto2pickChoice直下にコピーする。
## Auto2pickChoice
```bash
python descripter_cash.py
python present_cards.py
```

# Note
 Usageは上から順に作業を行って下さい。
 
# License
"Auto2pickChoice" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).