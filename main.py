"""写真位置マップ デスクトップアプリ起動処理。"""

from __future__ import annotations

import sys
from pathlib import Path

import webview


APP_NAME = "写真位置マップ"


def resource_path(filename: str) -> Path:
    """開発時とPyInstallerパッケージ内の両方で素材のパスを返す。"""
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_dir / filename


def main() -> None:
    index_path = resource_path("index.html")
    if not index_path.is_file():
        raise FileNotFoundError(f"画面ファイルが見つかりません: {index_path}")

    webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True
    webview.create_window(
        APP_NAME,
        url=str(index_path),
        width=1440,
        height=900,
        min_size=(1000, 700),
        background_color="#f4f6f9",
    )
    # ローカルHTTPサーバー経由でHTMLを表示する。
    # file://特有のブラウザ制限を避け、WindowsとmacOSで挙動を揃える。
    webview.start(http_server=True, private_mode=False)


if __name__ == "__main__":
    main()
