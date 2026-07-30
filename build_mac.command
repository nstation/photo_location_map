#!/bin/bash
set -e
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: uvが見つかりません。"
  echo "brew install uv または curl -LsSf https://astral.sh/uv/install.sh | sh を実行してください。"
  exit 1
fi

# Finderやダウンロード元が付与した拡張属性が残っていると、
# PyInstallerのアドホック署名に失敗するためビルド前に除去する。
xattr -cr index.html icon.png main.py

uv run --isolated --no-project --python ">=3.10" \
  --with-requirements requirements.txt build.py

uv cache prune

echo
echo "ビルド完了: dist/PhotoLocationMap.app"
