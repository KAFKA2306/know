# AGENTS.md (引継書)

このファイルは、本リポジトリ `know` を管理・運用する未来のAIエージェント（および人間）のための引継書です。

## リポジトリの目的
- **Multi-Knowledge Base**: 開発(Dev)と生活(Life)に関する知識を集約する。
- **Source of Truth**: 常に最新かつ正確な情報を保つ。

## 運用ルール (Constitution)
すべての操作は **`.agent/workflows/writing-rules.md`** に従ってください。
- **公式ドキュメント至上主義**: 一次情報を必ず参照する。
- **シンプルイズベスト**: 冗長な記述は削除する。
- **正確性**: 曖昧な推測を書かない。

## ワークフロー (Workflows)
作業を開始する前に、以下の対応するワークフローを確認してください。

| 目的 | 参照ファイル | コマンド例 |
| :--- | :--- | :--- |
| **新規知識の追加** | [add-knowledge.md](.agent/workflows/add-knowledge.md) | `/add-knowledge` |
| **品質維持・メンテ** | [maintain-quality.md](.agent/workflows/maintain-quality.md) | `/maintain-quality` |
| **既存情報の更新** | [update-content.md](.agent/workflows/update-content.md) | `/update-content` |

## 技術スタック & コマンド

- **環境**: Python 3.11, `uv`, `mkdocs-material`
- **必須コマンド**:

```bash
# 開発サーバー起動 (プレビュー)
task dev

# ビルド検証 (リンク切れチェック)
uv run mkdocs build
```

## 申し送り事項
- `mkdocs.yml` の `validation` 設定により、リンク切れはビルド時に検出されます。変更時は必ずビルドを通してください。
- 記事の更新時は、単なる追記ではなく「Destructive Rewrite (破壊的書き直し)」を恐れずに行い、常に記事をシンプルに保ってください。
