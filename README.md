# GlomaticoのYouTube Music Downloader GUI
YouTube Musicの曲/アルバム/プレイリストをタグ付きで256kbps AAC/128kbps Opus/128kbps AACでダウンロードするためのツールです。

## なぜ直接yt-dlpを使用しないのですか？
このプロジェクトは、yt-dlpを使用してYouTube Musicから曲をダウンロードする仕組みを採用していますが、[YouTube MusicのAPI](https://github.com/sigma67/ytmusicapi)を利用して曲のメタデータを取得するため、正確なタグ情報を取得することができます。これには、トラック番号、カバーアート、歌詞、年などの情報が含まれます。

