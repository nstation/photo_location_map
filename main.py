"""写真位置マップ デスクトップアプリ起動処理。"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

import webview


APP_NAME = "PhotoLocationMap"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".webp"}


def resource_path(filename: str) -> Path:
    """開発時とPyInstallerパッケージ内の両方で素材のパスを返す。"""
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_dir / filename


class AppApi:
    """ネイティブUIとローカル写真読込をJavaScriptへ公開する。"""

    def __init__(self) -> None:
        self.window: webview.Window | None = None
        self.selected_folder: Path | None = None

    def select_folder(self, include_subfolders: bool) -> dict[str, object] | None:
        """ネイティブダイアログを開き、選択フォルダ内の対象写真を返す。"""
        if self.window is None:
            raise RuntimeError("アプリケーションウィンドウが初期化されていません")

        result = self.window.create_file_dialog(webview.FileDialog.FOLDER)
        if not result:
            return None

        folder = Path(result[0]).resolve()
        self.selected_folder = folder
        candidates = folder.rglob("*") if include_subfolders else folder.iterdir()
        files = []

        for path in candidates:
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                try:
                    resolved = path.resolve()
                    resolved.relative_to(folder)
                except (OSError, ValueError):
                    continue
                files.append(resolved.relative_to(folder).as_posix())

        files.sort(key=str.casefold)
        return {"folder_name": folder.name or str(folder), "files": files}

    def read_photo(self, relative_path: str) -> dict[str, str]:
        """直前に選択したフォルダ内の写真をBase64で返す。"""
        if self.selected_folder is None:
            return {"error": "フォルダが選択されていません"}

        try:
            path = (self.selected_folder / relative_path).resolve()
            path.relative_to(self.selected_folder)
            if path.suffix.lower() not in IMAGE_SUFFIXES or not path.is_file():
                raise ValueError("対象外のファイルです")
            mime_type = "image/webp" if path.suffix.lower() == ".webp" else "image/jpeg"
            return {
                "data": base64.b64encode(path.read_bytes()).decode("ascii"),
                "mime_type": mime_type,
            }
        except (OSError, ValueError) as error:
            return {"error": str(error)}


def main() -> None:
    index_path = resource_path("index.html")
    if not index_path.is_file():
        raise FileNotFoundError(f"画面ファイルが見つかりません: {index_path}")

    webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True
    api = AppApi()
    window = webview.create_window(
        APP_NAME,
        url=str(index_path),
        js_api=api,
        width=1440,
        height=900,
        min_size=(1000, 700),
        background_color="#f4f6f9",
    )
    api.window = window
    # ローカルHTTPサーバー経由でHTMLを表示する。
    # file://特有のブラウザ制限を避け、WindowsとmacOSで挙動を揃える。
    webview.start(http_server=True, private_mode=False)


if __name__ == "__main__":
    main()
