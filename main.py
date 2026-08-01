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

    __slots__ = ("_window", "_selected_folder")

    def __init__(self) -> None:
        # pywebviewはjs_apiの公開属性を再帰走査する。Windowを公開属性にすると
        # WebView2のCOMオブジェクトまで走査してUIスレッドを停止させるため、
        # JavaScriptへ公開しない内部状態は必ずアンダースコア付きで保持する。
        self._window: webview.Window | None = None
        self._selected_folder: Path | None = None

    def select_folder(self, include_subfolders: bool) -> dict[str, object] | None:
        """ネイティブダイアログを開き、選択フォルダ内の対象写真を返す。"""
        if self._window is None:
            raise RuntimeError("アプリケーションウィンドウが初期化されていません")

        result = self._window.create_file_dialog(webview.FileDialog.FOLDER)
        if not result:
            return None

        folder = Path(result[0]).resolve()
        self._selected_folder = folder
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
        if self._selected_folder is None:
            return {"error": "フォルダが選択されていません"}

        try:
            path = (self._selected_folder / relative_path).resolve()
            path.relative_to(self._selected_folder)
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
        width=1024,
        height=600,
        min_size=(1024, 580),
        background_color="#f4f6f9",
    )
    api._window = window
    # ローカルHTTPサーバー経由でHTMLを表示する。
    # file://特有のブラウザ制限を避け、WindowsとmacOSで挙動を揃える。
    # このアプリはCookieやlocalStorageを使わない。Windows版WebView2で
    # 永続プロファイルを初めて作成するときの停止を避けるため、終了時に
    # ユーザーデータを破棄するプライベートモードで起動する。
    webview.start(http_server=True, private_mode=True)


if __name__ == "__main__":
    main()
