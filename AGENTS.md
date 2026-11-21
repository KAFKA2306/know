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
task deploy      # GitHub Pages デプロイ
```

## Kafstyler schema適用

- データ設計の手順は [Kafstyler canonicalize](https://github.com/KAFKA2306/kafstyler/blob/74542d01665cdd1e97ab41a00d6055593f07140d/skills/canonicalize/SKILL.md) を参照する。作業対象の正本は `docs/**/*.md`、構造の正本は `ontology/knowledge.schema.json`。
- 記事・索引を作成または変更するときは `type`・`description`・`tags` を保つ。出典・確認は `sources`・`verified` で区別し、確認していない情報を検証済みにしない。
- `task build` の前に `uv run python scripts/validate_knowledge_schema.py` で検証する。交換用OKF v0.3は `--export-okf` で派生生成し、公開用MkDocsの索引ファイルを改名しない。

## コンテンツルール

| ルール | 説明 |
|--------|------|
| 公式ドキュメント至上主義 | 一次情報を必ず参照。二次情報（ブログ等）は参考程度 |
| 日本語記述 | 専門用語は英語可（Agent, RAG, MCP等） |
| Destructive Rewrite | 追記より破壊的書き直しを優先。常にシンプルに |
| 正確性最優先 | 「〜らしい」「〜かも」で断定しない。未確認の点は未確認と明記する |
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

## Outcome-first task interpretation (Altitude / Depth / Range / Speed)

- **Altitude:** Interpret a task as a verifiable user outcome, not only the named intermediate step. Infer the smallest justified acceptance criteria from the request and current repository state; do not silently expand scope or override explicit instructions.
- **Depth:** Use primary/current evidence and real domain tools and methods. Verify the actual postcondition independently of agent self-report, preferably on the exact changed revision or target runtime.
- **Range:** Combine code, data, tests, runtime/UI, and domain expertise when that materially improves the outcome, while respecting canonical owners and avoiding duplicate systems.
- **Speed:** Complete authorized read-only and reversible work through implementation, focused checks, and read-back without unnecessary approval loops. Bound retries and stop at the proven outcome.
- These principles never bypass repository-specific security, privacy, permission, publication, spending, destructive-action, or release boundaries. State verified results and any remaining `UNVERIFIED` layers.
