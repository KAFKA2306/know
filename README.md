# Know

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) で構築された個人のナレッジベースおよびブックマークマネージャーです。

## コンテンツ

- **[Bookmarks](docs/bookmarks/index.md)**: AI, Dev, Finance, Game, Life, Media, Academic などの厳選リソース集。
- **[Dev](docs/dev/index.md)**: 技術ナレッジベース (AI Agent, WSL)。
- **[Life](docs/life/index.md)**: 生活・個人管理 (税金, 投資)。

## セットアップ

### 前提条件

- Python 3.11以上
- [uv](https://docs.astral.sh/uv/)
- [Task](https://taskfile.dev/installation/)

### インストール

```bash
git clone https://github.com/KAFKA2306/know.git
cd know
uv sync
```

## 使い方

```bash
task dev      # ローカル開発サーバー (http://127.0.0.1:8000)
task build    # 静的サイトビルド
task deploy   # GitHub Pages デプロイ
```

## デプロイ

`main` ブランチへのプッシュ時に GitHub Pages に自動デプロイされます。

**URL**: [https://KAFKA2306.github.io/know/](https://KAFKA2306.github.io/know/)