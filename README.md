# Know

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) で構築された個人のナレッジベースおよびブックマークマネージャーです。

## コンテンツ

- **[Bookmarks](docs/bookmarks/index.md)**: AI, Dev, Finance, Game, Life, Media, Academic などの厳選リソース集。
- **[Dev](docs/dev/index.md)**: 技術ナレッジベース (AI Agent, WSL)。
- **[Life](docs/life/index.md)**: 生活・個人管理 (税金, 投資)。

## セットアップ

このプロジェクトでは、依存関係の管理に [`uv`](https://docs.astral.sh/uv/)、タスクランナーとして [`task`](https://taskfile.dev/) を使用しています。

### 前提条件

- Python 3.12以上
- [uv](https://github.com/astral-sh/uv)
- [Task](https://taskfile.dev/installation/)

### インストール

```bash
git clone https://github.com/KAFKA2306/know.git
cd know
uv sync
```

## 使い方

### ローカルでの実行

ライブリロード対応の開発サーバーを起動します:

```bash
task dev
# または uv を直接使用
uv run mkdocs serve
```

ブラウザで [http://127.0.0.1:8000](http://127.0.0.1:8000) を開いてください。

### ビルド

静的サイトをビルドします:

```bash
task build
```

## デプロイ

`main` ブランチへのプッシュ時に、GitHub Actions 経由で GitHub Pages に自動デプロイされます。
URL: [https://KAFKA2306.github.io/know/](https://KAFKA2306.github.io/know/)