---
type: reference
description: "Knowの知識ページを追加・改稿するときのメタデータと出典の規約。"
tags:
  - know/rules
---

# 記事と出典のルール

知識は `docs/**/*.md` を正本とする。公開URLを保ち、同じ主張の出典と確認時点を別ファイルに重複保存しない。

## 記事の契約

- 全記事に YAML frontmatter の `type`、日本語の `description`、1件以上の `tags` を置く。[JSON Schema](https://github.com/KAFKA2306/know/blob/main/ontology/knowledge.schema.json) が正本。
- 事実、推定、仮説、判断を区別する。根拠のない断定はしない。確認できない場合は「未確認」と明記する。
- 原典のURL、対象期間、参照版を示す。原典を実際に独立照合した場合にのみ `verified.by` と `verified.at` を記す。
- `sources` には安定した `id` と `resource` を記載し、本文の同じIDの脚注 `[^id]` と結ぶ。
- 古くなった記事には再確認条件を記す。廃止する記事は旧URLと後継へのリンクを維持する。
- 説明は日本語で、結論・根拠・条件を短く書く。公式資料を優先し、版の変化が速い情報は更新時に再照合する。

## テンプレート

```markdown
---
type: knowledge
description: 判断に必要な事実と再確認条件を整理する記事。
tags:
  - know/dev
sources:
  - id: primary
    resource: https://docs.github.com/
---

# 記事のタイトル

## 判断

何を、どの条件で判断できるか。

## 根拠

確認した事実と未確認の点を分ける。[^primary]

## 再確認条件

どの出来事、公開版、観測値が変わったら見直すか。

[^primary]: [GitHub Docs](https://docs.github.com/)
```

## 確認

```bash
task build
```

`task build` は全記事のスキーマ検証と MkDocs strict build を実行する。GitHub の `main` 更新後は CI が公開する。外部リンクのHTTP失敗だけで記事を一括削除しない。

知識の交換が必要なときだけ `uv run python scripts/validate_knowledge_schema.py --export-okf /tmp/know-okf` を実行する。OKF v0.3は生成物であり、別の正本を増やさない。
