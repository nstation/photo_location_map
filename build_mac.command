#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python3" ]; then
  python3 -m venv .venv
fi

".venv/bin/python3" -m pip install --upgrade pip
".venv/bin/python3" -m pip install -r requirements.txt

# Finderやダウンロード元が付与した拡張属性が残っていると、
# PyInstallerのアドホック署名に失敗するためビルド前に除去する。
xattr -cr .venv index.html icon.png main.py

".venv/bin/python3" build.py

echo
echo "ビルド完了: dist/PhotoLocationMap.app"
