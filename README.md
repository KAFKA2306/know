# Know

[![CI / Pages](https://github.com/KAFKA2306/know/actions/workflows/ci.yml/badge.svg)](https://github.com/KAFKA2306/know/actions/workflows/ci.yml)

公開サイト: https://kafka2306.github.io/know/

開発、金融、生活、研究の知識を検索し、判断・根拠・確認時点・再確認条件を読めるようにするナレッジベース。

## 使う

- [研究判断](https://kafka2306.github.io/know/research/): 仮説と一次資料、反証条件
- [開発](https://kafka2306.github.io/know/dev/): 技術・AIエージェント・WSL
- [生活](https://kafka2306.github.io/know/life/): 税務・金融
- [ブックマーク](https://kafka2306.github.io/know/bookmarks/): 分類した外部リンク
- [Evidence Contract 導入ガイド](docs/services/evidence-contract-integration.md): 他のリポジトリで根拠付きの判断を検査するサンプル

観測事実、推定、仮説、判断を同一視しない。古い情報は再確認し、記事に書かれた「検証済み」を機械的な形式検査だけで保証しない。

## 正本

- 記事: [docs/](docs/)。MkDocs の各 Markdown が正本。
- 記事の契約: [knowledge.schema.json](ontology/knowledge.schema.json)。
- 因果・証拠オントロジー: [causal-evidence-core.yaml](ontology/causal-evidence-core.yaml)。
- プロジェクト記述の契約と登録: [project.schema.json](ontology/project.schema.json)、[projects.yaml](ontology/projects.yaml)。
- 配布用の最小例: [Evidence Contract starter](templates/evidence-contract-starter/)。

知識記事の記述、出典ID、訂正、OKF v0.3への派生出力は[記事と出典のルール](docs/rules.md)を参照する。データ設計には [Kafstyler canonicalize](https://github.com/KAFKA2306/kafstyler/blob/74542d01665cdd1e97ab41a00d6055593f07140d/skills/canonicalize/SKILL.md) を使う。

## 開発と公開

```bash
git clone https://github.com/KAFKA2306/know.git
cd know
uv sync
task dev
task build
```

- `task dev`: ローカル確認用サーバー
- `task build`: 記事schema検査とMkDocs厳格ビルド
- `main` にpush: GitHub Actionsで検証してPagesへ公開

CIでは記事schema、配布用Evidence Contract validatorの代表的な正常・異常例、公開サイトのstrict buildを一回だけ確認する。配布用スターター自身にも導入先のCI例がある。

## 外部プロジェクトの監査

`python scripts/audit_project_ontologies.py` は登録された外部リポジトリのmanifestとREADMEを取得するため、ネットワークと参照先の権限が必要。GitHub Actionsでは[手動監査](https://github.com/KAFKA2306/know/actions/workflows/ontology-audit.yml)として実行する。取得できないmanifestはエラーとして残し、監査成功やプロジェクトの消滅を推測しない。

## 整理方針

完了済みの作業経緯はGit履歴・Issueへ置き、運用中の手順は`AGENTS.md`、記事の書き方は`docs/rules.md`へ集約する。未計測の成果は数値や空の台帳を増やして成果扱いしない。
