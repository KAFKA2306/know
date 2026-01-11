---
description: 新しい知識を追加するためのフロー
---

# 知識追加ワークフロー

## ディレクトリ構造

```
docs/
├── dev/           # 開発・技術
│   └── agent/     # LLM Agent関連
│       ├── data-storage/
│       ├── evaluation/
│       ├── memory/
│       ├── observability/
│       └── orchestration/
├── life/          # 生活・趣味
└── work/          # 仕事・キャリア
```

## フロー

### 1. カテゴリ判定

| カテゴリ | 対象 |
|---------|------|
| `dev/` | 技術・開発関連 |
| `dev/agent/` | LLM Agent関連 |
| `life/` | 生活・趣味・健康 |
| `work/` | 仕事術・キャリア |

### 2. ファイル作成

**既存カテゴリの場合:**
```bash
# 例: dev/agent/orchestration に新ツール追加
touch docs/dev/agent/orchestration/new-tool.md
```

**新サブカテゴリの場合:**
```bash
mkdir -p docs/dev/new-category
touch docs/dev/new-category/index.md
touch docs/dev/new-category/topic.md
```

### 3. テンプレート使用

```markdown
# タイトル

概要（1-2文）

## 本質

この技術が解決する問題

## 基本

- 要点1
- 要点2
- 要点3

## 使い方

コード例（必要な場合）

## 参照

- [公式ドキュメント](URL)
```

### 4. mkdocs.yml更新

`nav:`に追加:

```yaml
nav:
  - カテゴリ:
    - path/to/new-file.md
```

### 5. 確認 & デプロイ

```bash
# ローカル確認
task serve

# デプロイ
git add .
git commit -m "docs: add <topic>"
git push
```

## ルール

1. **公式ソース参照** - 一次情報源を使用
2. **日本語記述** - 技術用語は英語可
3. **シンプル** - 短く・箇条書き活用
4. **正確性** - 曖昧表現禁止
5. **出典明記** - 公式リンク必須
