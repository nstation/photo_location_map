# 写真位置マップ

JPEG・WebP写真のEXIF GPS情報を読み取り、撮影場所をOpenStreetMapに表示する
Windows／macOS対応デスクトップアプリです。ユーザーインターフェースは
`index.html`で実装し、pywebviewのネイティブWebView内に表示します。
ネイティブウィンドウのタイトルと配布ファイル名には`PhotoLocationMap`を使用し、
画面内には「写真位置マップ」と表示します。

## 主な機能

- 写真フォルダ、JPEG・WebPファイルの選択
- 写真一覧へのドラッグ＆ドロップ
- サブフォルダを含む100件以上の写真読み込み
- 一覧へのサムネイル、撮影日時、GPS状態の表示
- 選択済み写真の再クリック、またはボタンによるEXIF情報表示
- OpenStreetMapでの撮影位置表示
- Googleマップの外部ブラウザ表示

## 対応環境

- Windows 10／11（64bit）
- macOS 12以降
- uv（ソース実行・ビルド時のみ。Python 3.10以降を自動管理）
- インターネット接続（地図、Leaflet、EXIF解析ライブラリの読み込みに使用）

WindowsではMicrosoft Edge WebView2 Runtimeを使用します。Windows 10／11には通常
インストールされています。macOSでは標準のWebKitを使用します。

## 開発環境の準備

ソース実行とビルドにはuvを使用します。プロジェクト内に`.venv`は作成しません。
uvが管理するPythonと一時隔離環境へ`requirements.txt`の依存関係をインストールします。

Windows：

```bat
winget install --id Astral-sh.uv
```

macOS：

```bash
brew install uv
```

## ソースから起動

### Windows

```powershell
cd photo_location_map
uv run --isolated --no-project --python ">=3.10" --with-requirements requirements.txt main.py
```

### macOS

```bash
cd photo_location_map
uv run --isolated --no-project --python ">=3.10" --with-requirements requirements.txt main.py
```

## アプリのビルド

PyInstallerはクロスコンパイルに対応していません。Windows版はWindows上で、
Mac版はMac上でそれぞれビルドしてください。

### Windows版

`build_windows.bat`をダブルクリックするか、コマンドプロンプトで実行します。

```bat
build_windows.bat
```

出力：

```text
dist\PhotoLocationMap.exe
```

### Mac版

初回のみ実行権限を付け、その後スクリプトを実行します。

```bash
chmod +x build_mac.command
./build_mac.command
```

出力：

```text
dist/PhotoLocationMap.app
```

ビルド時にローカル実行用のアドホック署名を付与します。日本語を含むバンドル名で
署名が失敗する環境があるため、実ファイル名は`PhotoLocationMap.app`です。
ネイティブウィンドウのタイトルは`PhotoLocationMap`です。

別のMacへ配布する場合は、Apple Developer IDによる正式なコード署名と公証を
推奨します。アドホック署名のみのアプリは、Gatekeeperによって初回起動を
止められる場合があります。

Windows／macOSのビルドスクリプトは、ビルド成功後に`uv cache prune`を実行し、
不要なキャッシュと一時環境を整理します。再利用可能なパッケージキャッシュは
残る場合があります。すべて削除する場合は`uv cache clean`を実行してください。

## フォルダ構成

```text
photo_location_map/
├── index.html           アプリ画面・写真処理
├── icon.png            画面とアプリのアイコン
├── main.py             デスクトップアプリ起動処理
├── build.py            OS判定とPyInstallerビルド
├── build_windows.bat   Windows用ビルドスクリプト
├── build_mac.command   macOS用ビルドスクリプト
├── requirements.txt    uvが読み込むPython依存パッケージ
├── 仕様.md             アプリ仕様
└── README.md           このファイル
```

## 使用方法

1. アプリを起動します。
2. 「フォルダを選択」「ファイルを選択」を押すか、写真一覧へ写真をD&Dします。
3. 一覧の未選択写真をクリックします。
4. GPS情報があれば撮影位置へ地図マーカーが移動します。
5. 選択中の同じ写真をもう一度クリックすると、マーカーを移動せずEXIF情報を表示します。
6. 「EXIF情報を表示」ボタンから開くこともできます。

## 制限事項

- 対応画像はJPEG（`.jpg`、`.jpeg`）とWebP（`.webp`）です。
- 地図およびCDNライブラリの読み込みにはインターネット接続が必要です。
- 写真は地図サービスへ送信しません。ブラウザ内でEXIFを解析します。
- Windows版とMac版の実行ファイルは、各OS上で個別に作成します。
- ビルドスクリプトの実行にはuvが必要です。配布アプリの利用者には不要です。
