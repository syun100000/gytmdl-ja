# GlomaticoのYouTube Music Downloader
YouTube Musicの曲/アルバム/プレイリストをタグ付きで256kbps AAC/128kbps Opus/128kbps AACでダウンロードするためのツールです。

## なぜ直接yt-dlpを使用しないのですか？
このプロジェクトは、yt-dlpを使用してYouTube Musicから曲をダウンロードする仕組みを採用していますが、[YouTube MusicのAPI](https://github.com/sigma67/ytmusicapi)を利用して曲のメタデータを取得するため、正確なタグ情報を取得することができます。これには、トラック番号、カバーアート、歌詞、年などの情報が含まれます。

## セットアップ（現在このセットアップは無効）
1. Python 3.8以上をインストールします。
2. pipを使用してgytmdlをインストールします。
    ```
    pip install gytmdl
    ```
3. FFMPEGをPATHに追加します。ここから入手できます: https://ffmpeg.org/download.html
    * Windowsの場合は、`ffmpeg.exe`ファイルをPATHに追加する代わりに、スクリプトを実行するフォルダに移動させることもできます。
4. (オプション) cookies.txtを取得します。
    * cookies.txtを使用することで、エイジ制限のあるトラックやプライベートプレイリスト、256kbps AACでの曲のダウンロードが可能になります。プレミアムユーザーの場合は、`--itag 141`引数を使用してダウンロードできます。Google Chromeの拡張機能を使用して、YouTube Musicのウェブサイトにログインした状態でcookiesをエクスポートすることができます。拡張機能はこちらから入手してください: https://chrome.google.com/webstore/detail/gdocmgbfkjnnpapoeobnolbbkoibbcif。エクスポートする際には、`cookies.txt`として同じフォルダに保存してください。

## 使用方法
```
usage: gytmdl [-h] [-u [URLS_TXT]] [-t TEMP_PATH] [-f FINAL_PATH] [-c COOKIES_LOCATION] [-i {141,251,140}] [-o]
                   [-s] [-e] [-v]
                   [<url> ...]

YouTube Musicの曲/アルバム/プレイリストをタグ付きでダウンロードするツール

positional arguments:
  <url>                 YouTube Musicの曲/アルバム/プレイリストのURL(s)（デフォルト: None）

options:
  -h, --help            ヘルプメッセージを表示して終了します
  -u [URLS_TXT], --urls-txt [URLS_TXT]
                        テキストファイルからURLを読み込みます（デフォ

ルト: None）
  -t TEMP_PATH, --temp-path TEMP_PATH
                        一時フォルダのパス（デフォルト: temp）
  -f FINAL_PATH, --final-path FINAL_PATH
                        最終的な保存先フォルダのパス（デフォルト: YouTube Music）
  -c COOKIES_LOCATION, --cookies-location COOKIES_LOCATION
                        Cookiesの場所（デフォルト: cookies.txt）
  -i {141,251,140}, --itag {141,251,140}
                        itag（品質）を指定します。141（256kbps AAC、Cookiesが必要）、251（128kbps Opus）、140（128kbps AAC）のいずれかを指定できます（デフォルト: 140）
  -o, --overwrite       既存のファイルを上書きします（デフォルト: False）
  -s, --skip-cleanup    クリーンアップをスキップします（デフォルト: False）
  -e, --print-exceptions
                        例外を表示します（デフォルト: False）
  -v, --version         プログラムのバージョン番号を表示して終了します
```
