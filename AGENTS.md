---
type: policy
description: "Knowで記事、検証、GitHub Pagesを維持するためのリポジトリ固有の規則。"
tags:
  - know/operations
---

# Know の作業規約

目的は[公開Know](https://kafka2306.github.io/know/)で過去の知識を検索し、出典・時点・判断・再確認条件を確認できること。

- 最新の [Kafstyler](https://github.com/KAFKA2306/kafstyler) の `reconceptualize`・`canonicalize`・`decommission`・`disprove`・`adjudicate` を、該当する工程で適用する。適用先の契約はこのリポジトリの正本を優先する。
- 記事の正本は`docs/**/*.md`、記事の型は`ontology/knowledge.schema.json`。書き方と出典・確認記録は[記事と出典のルール](docs/rules.md)に置く。Obsidian/OKFの交換用生成物を第二の正本にしない。
- `task dev`で確認し、変更前に`task build`でschema検証とMkDocs strict buildを通す。`main`への反映後はGitHub Actionsの公開成功とサイト上の対象経路を確認する。
- Pages公開は`main`からのActionsだけを使う。`mkdocs gh-deploy`で別の配布ブランチを作らない。
- 外部リンクの一時的な遮断・タイムアウトを「404で削除済み」と同一視しない。記事やブックマークを削除する前に利用経路と根拠を確認する。
- 外部オントロジー監査では取得不能なmanifestを失敗のまま記録する。知識・配布用サンプル・データを削除する場合は公開URLと参照先への影響を先に調べる。
- 完了時は差分・公開検査・未完了をIssueに記録する。変更の履歴は閉じたIssueとコミットを参照し、古い指示を別ファイルへ複製しない。
