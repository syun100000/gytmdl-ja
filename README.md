# Gytmdl GUI -  Graphical YouTube Music Downloader

Gytmdl GUIはYouTube Musicから音楽をダウンロードし、適切なメタデータを付与するためのPython製のGUIツールです。それは音楽のIDに基づいて音楽を検索し、指定された品質でダウンロードし、そして必要なタグ情報を取得して音楽ファイルに適用します。

## 特徴

- YouTube Musicから音楽をダウンロード
- 音楽ファイルにメタデータを付与（アーティスト名、アルバム名、曲名、カバーアートなど）
- YouTubeのCookieを使用してダウンロードの制限を回避
- ファイルのダウンロードと整理を自動化
- GUIを使用して簡単に操作

## インストールと使用方法

### コンパイル
pyinstallerを使用して、GUIアプリケーションをコンパイルすることができます。
```bash
pip install pyinstaller
```

Mac OS
```bash
pyinstaller --windowed --onefile --icon=gytmdl_gui.icns gytmdl_gui.py
```

Windows
```bash
pyinstaller --onefile --icon=gytmdl_gui.ico gytmdl_gui.py
```

アプリケーションが開始されると、GUIが表示されます。適切なパラメータを設定し、音楽のダウンロードを開始します。

URLS.TXTは次の拡張機能を使って簡単に作成できます。
https://github.com/syun100000/GET_URLS
## 注意事項

このツールはYouTubeの利用規約に抵触する可能性があります。自己責任で使用してください。

## ライセンス

MIT License

---

以上が基本的なREADME.mdの内容となります。何か不明な点があれば、お気軽にお問い合わせください。


