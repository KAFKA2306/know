---
description: ナレッジ記事作成の基本ルール
type: reference
tags:
  - know/rules
---

# Know プロジェクト 執筆ルール

## 絶対ルール

1. **公式ドキュメントを必ず参照する**
   - 公式サイト・GitHubリポジトリを一次情報源とする
   - 二次情報（ブログ・Qiita等）は参考程度

2. **日本語で書く**
   - 言語は日本語
   - 専門用語は英語のまま可（例: Agent, RAG, Vector DB）

3. **シンプルに書く**
   - 無駄な装飾を避ける
   - 1文は短く
   - 箇条書きを活用

4. **正しく書く（正確性最優先）**
   - 曖昧な表現を避ける
   - 「〜らしい」「〜かも」は禁止
   - 分からないことは書かない

5. **出典を明記する**
   - 公式ドキュメントへのリンクを必ず含める
   - バージョン情報があれば記載

## Kafstylerのデータ設計とschema

- 正本は `docs/**/*.md`。1ファイルが1記事または1索引。URLと既存の見出しは維持する。
- 全ページのYAML frontmatterに `type`、日本語の `description`、1件以上の `tags` を付ける。型は [`knowledge.schema.json`](../ontology/knowledge.schema.json) に従う。
- 検証済みの意味に使う `verified` は、原典を独立に照合した記録がある場合だけ記す。`sources` のIDと `resource` を本文脚注 `[^id]` に対応させる。未確認の推定を事実扱いしない。
- 文章の正本はMkDocsページのまま維持する。交換用のOKF v0.3バンドルは検証器から生成する。MkDocsの `index.md` は交換先で `overview.md` にして、OKFの予約済み `index.md` と衝突させない。
- 実行: `uv run python scripts/validate_knowledge_schema.py`。交換用生成: `uv run python scripts/validate_knowledge_schema.py --export-okf /tmp/know-okf`（出力先は空ディレクトリ）。
- 参照したKafstylerは [`canonicalize`](https://github.com/KAFKA2306/kafstyler/blob/74542d01665cdd1e97ab41a00d6055593f07140d/skills/canonicalize/SKILL.md)。自動検査は出典の内容の正誤を保証しない。

## テンプレート

```markdown
---
tags:
  - タグ1
  - タグ2
---

# タイトル

概要（1-2文）

## 本質

この技術/ツールが解決する問題

## 基本

- 要点1
- 要点2
- 要点3

## 参照

- [公式ドキュメント](URL)
```

## タグ運用ルール

| カテゴリ | タグ例 |
|---------|--------|
| 技術領域 | `agent`, `rag`, `llm`, `vector-db` |
| ライフ | `tax`, `health`, `finance` |
| ステータス | `wip`, `deprecated` |

## 新規ドキュメント追加チェックリスト

- [ ] frontmatter に `type`、`description`、`tags` を記載した
- [ ] sources と本文脚注の対応、未確認情報の扱いを確認した
- [ ] `uv run python scripts/validate_knowledge_schema.py` が通った
- [ ] 公式ドキュメントへのリンクを含めた
- [ ] `mkdocs.yml` の `nav` に追加した（必要な場合）
- [ ] ローカルで `uv run mkdocs build --strict` が通る
