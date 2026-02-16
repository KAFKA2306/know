---
description: 新しい知識を追加するためのフロー
---

# 知識追加ワークフロー

// turbo-all

## 1. カテゴリ判定

| カテゴリ | 対象 |
|---------|------|
| `dev/` | 技術・開発 |
| `dev/agent/` | LLM Agent |
| `dev/deepdive/` | 学習コンテンツ |
| `life/` | 生活・税金 |
| `bookmarks/` | ブックマーク集 |

## 2. ファイル作成

```bash
mkdir -p docs/<category>/
touch docs/<category>/<topic>.md
```

## 3. テンプレート

```markdown
# タイトル

概要（1-2文）

## 本質

この技術が解決する問題

## 基本

- 要点1
- 要点2
- 要点3

## 参照

- [公式ドキュメント](URL)
```

## 4. mkdocs.yml 更新

`nav:` に追加。パスが存在することを確認。

## 5. 検証 & デプロイ

```bash
task check
```

```bash
task git MESSAGE="docs: add <topic>"
```
