"""現在のOS向けに写真位置マップをパッケージ化する。"""

from __future__ import annotations

import platform
from pathlib import Path

import PyInstaller.__main__


DISPLAY_NAME = "写真位置マップ"
APP_NAME = "PhotoLocationMap"
PROJECT_DIR = Path(__file__).resolve().parent


def main() -> None:
    system = platform.system()
    if system not in {"Windows", "Darwin"}:
        raise SystemExit("ビルド対応OSはWindowsまたはmacOSです。")

    for required in ("main.py", "index.html", "icon.png"):
        if not (PROJECT_DIR / required).is_file():
            raise SystemExit(f"必要なファイルが見つかりません: {required}")

    output_dir = PROJECT_DIR / "dist"
    work_dir = PROJECT_DIR / "build"
    spec_dir = PROJECT_DIR / "build-spec"
    spec_dir.mkdir(exist_ok=True)

    args = [
        str(PROJECT_DIR / "main.py"),
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--icon",
        str(PROJECT_DIR / "icon.png"),
        "--add-data",
        f"{PROJECT_DIR / 'index.html'}:.",
        "--add-data",
        f"{PROJECT_DIR / 'icon.png'}:.",
        "--distpath",
        str(output_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(spec_dir),
        "--collect-all",
        "webview",
    ]

    if system == "Windows":
        args.append("--onefile")
    else:
        args.extend(
            [
                "--onedir",
                "--osx-bundle-identifier",
                "net.nfeed.photo-location-map",
            ]
        )

    PyInstaller.__main__.run(args)

    result = (
        output_dir / f"{APP_NAME}.exe"
        if system == "Windows"
        else output_dir / f"{APP_NAME}.app"
    )
    if result.exists():
        print(f"{DISPLAY_NAME} ビルド完了: {result}")
    else:
        raise SystemExit("ビルドは終了しましたが、出力ファイルを確認できませんでした。")


if __name__ == "__main__":
    main()
