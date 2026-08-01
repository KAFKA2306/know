# Know — 開発・投資・生活の知識基盤

**公開サイト:** https://kafka2306.github.io/know/

Knowは、開発、AI、金融、生活設計で繰り返し参照する知識を、MkDocsで検索・更新できる形にまとめる個人向けナレッジベースです。

単なるブックマーク集ではなく、情報源、観測事実、計算値、推定、主張、検証、判断を区別し、他のKAFKA2306プロジェクトでも再利用できる共通オントロジーを管理します。

## 主な内容

### 開発・AI

- AIエージェント、オーケストレーション、メモリ、評価、監視
- MCP、CLI、ローカルLLM、開発ツール
- データ構造、HTTP、データベース、型、アーキテクチャ
- WSLや開発環境の設定・トラブル対応

### 金融・生活設計

- NISA、資産配分、配当、税務
- クレジットカード、ポイント、家計管理
- 継続的に使うサービスや参考資料の整理

### 厳選リンク

開発、金融、生活、メディア、学術、ゲームに分類した外部資料を管理します。リンクは追加するだけでなく、重複、リンク切れ、分類のずれを監査します。

## 共通の因果・証拠オントロジー

```text
Entity
  → State
  → Action / Process
  → Observation
  → Estimate
  → Claim
  → Test
  → Evidence
  → Decision
```

主なファイル:

- [因果・証拠中核オントロジー](ontology/causal-evidence-core.yaml)
- [プロジェクト記述スキーマ](ontology/project.schema.json)
- [適用プロジェクト・レジストリ](ontology/projects.yaml)
- 各リポジトリの標準配置: `ontology/project.yaml`

観測事実、外部報告、計算値、モデル推定、予測、仮定、要求、判定を同じ文章として混ぜません。`PASS`、`GO`、公開、採用などの判断には、要求条件、証拠、判定規則を明示します。

## 自動監査

現在は、登録された各プロジェクトの`ontology/project.yaml`を横断して次を確認します。

- レジストリと実ファイルの対応
- 必須フィールドとスキーマ整合性
- 主張、証拠、判断の区分
- リポジトリ間で使う共通語彙の一貫性
- 未登録または参照切れのプロジェクト

監査はGitHub Actionsでも実行します。

## AIエージェントによる保守

- `.agent/workflows/add-knowledge.md` — 新しい知識の追加
- `.agent/workflows/maintain-quality.md` — リンク・分類・重複の監査
- `.agent/workflows/update-content.md` — 既存情報の更新
- `bookmark_manager.py` — ブックマークの検査と整理

## ローカル実行

### 必要環境

- Python 3.11以上
- `uv`
- `go-task`

```bash
git clone https://github.com/KAFKA2306/know.git
cd know
uv sync
task dev
```

ローカル表示:

```text
http://127.0.0.1:8000
```

主なコマンド:

| コマンド | 内容 |
| --- | --- |
| `task dev` | 開発サーバーを起動 |
| `task build` | 静的サイトをビルド |
| `task deploy` | GitHub Pagesへ公開 |
| `task clean` | 一時生成物を削除 |

## 記述方針

- 一次情報を優先する
- 取得日と対象バージョンを残す
- 推測と確認済み事実を分ける
- 古い情報を現在の仕様として断定しない
- 長い説明より、再利用可能な高密度情報を残す

詳細は[記述ルール](docs/rules.md)を参照してください。

**README最終監査:** 2026-08-01
