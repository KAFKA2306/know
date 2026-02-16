# AGENTS.md (引継書)

**`know` リポジトリの唯一の真実**

> [!IMPORTANT]
> グローバルルール [.agent/AGENTS.md](file:///home/kafka/projects/.agent/AGENTS.md) を継承。差分のみ記載。

## 目的

Multi-Knowledge Base。開発(Dev)・生活(Life)の知識を集約し、常に最新かつ正確に保つ。

## 技術スタック

| 要素 | 値 |
|------|-----|
| プラットフォーム | MkDocs Material |
| 環境管理 | uv, Python 3.11+ |
| タスクランナー | Taskfile.yml |
| デプロイ | GitHub Pages (GitHub Actions) |

## コマンド（Taskfile 経由必須）

```bash
task dev         # ローカルプレビュー
task build       # --strict ビルド検証
task check       # リンク切れ + 鮮度チェック
task deploy      # GitHub Pages デプロイ
task git MESSAGE="docs: ..." # add + commit + push
```

## コンテンツルール

| ルール | 説明 |
|--------|------|
| 公式ドキュメント至上主義 | 一次情報を必ず参照。二次情報（ブログ等）は参考程度 |
| 日本語記述 | 専門用語は英語可（Agent, RAG, MCP等） |
| Destructive Rewrite | 追記より破壊的書き直しを優先。常にシンプルに |
| 正確性最優先 | 「〜らしい」「〜かも」禁止。不明なら書かない |
| 出典必須 | 公式リンク + バージョン情報を記載 |

## ワークフロー

| コマンド | 目的 |
|---------|------|
| `/add-knowledge` | 新規知識の追加 |
| `/maintain-quality` | 品質維持・リンク切れ修正 |
| `/update-content` | 既存コンテンツの更新 |
| `/writing-rules` | 執筆ルール参照 |

## 構造

```
docs/
├── dev/           # 開発・技術
│   ├── agent/     # LLM Agent
│   ├── deepdive/  # 学習コンテンツ
│   └── wsl/       # WSL
├── bookmarks/     # ブックマーク集
└── life/          # 生活・税金
```

## 禁止事項

- `uv run mkdocs` の直接実行（`task build` を使う）
- `mkdocs.yml` の `nav:` に存在しないファイルパスの記載
- コンテンツの追記のみの更新（必ず全体を見直す）
