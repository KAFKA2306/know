# Anthropic Claude Code: 完全ガイド

**Claude Code** は、Anthropic が提供する最先端の**エージェント型コーディングツール**です。これまでブラウザ上のチャットボット (Claude.ai) で行っていた対話を、開発者のネイティブ環境である「ターミナル」に持ち込み、ファイルシステム、Git、そして多様な開発ツールと直接連携させることで、AI との協業レベルを「会話」から「共同作業」へと引き上げます。

Claude Code は、特に **Claude 3.7 Sonnet** モデルの圧倒的な推論能力とコーディング能力を最大限に発揮するようにチューニングされており、複雑なリファクタリング、バグ調査、複数ファイルにまたがる機能実装を得意とします。

---

## 1. 概念と特徴: The "Agentic" Shift

### 1.1 Unix Philosophy への回帰
Claude Code の設計思想は「Unix 哲学」に深く根ざしています。
- **Text Streams**: 標準入力 (stdin) と標準出力 (stdout) を介して、他のコマンドとシームレスに連携できます。
- **Small Tools**: `grep`, `ls`, `git` などの既存の小さなツールを、AI 自身が必要に応じて呼び出し、組み合わせることで大きなタスクを解決します。
- **Composability**: パイプライン処理に対応しており、スクリプトの一部として組み込むことができます。

### 1.2 "ReAct" ループの実装
Claude Code は単なる応答生成器ではなく、**Reasoning + Acting (ReAct)** ループを回す自律エージェントです。ユーザーのゴールを達成するために、以下のような動的な思考プロセスを実行します。

1. **Thought (思考)**: ゴールを達成するために何が必要か、情報が足りているかを考える。
2. **Action (行動)**: ファイルを読む (`view`), 検索する (`grep`), テストする (`run`) などの具体的な行動を選択・実行する。
3. **Observation (観察)**: 行動の結果（コマンドの出力、エラーメッセージ）を受け取る。
4. **Correction (修正)**: 結果が期待と異なる場合、仮説を修正し、次の行動を決定する。

このループにより、「言われたコードを書く」だけでなく、「動くコードになるまで試行錯誤する」ことが可能です。

---

## 2. インストールとセットアップ詳細

### 2.1 必須要件
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10/11 (WSL2 必須)
- **Node.js**: v18.15.0 以上（推奨 v20 LTS）
- **Python**: 3.10 以上 (一部のツール実行に必要)
- **Git**: 2.25 以上
- **Network**: `api.anthropic.com` への HTTPS 接続

### 2.2 インストール手順

#### A. Native Installer (推奨: 最速)
環境依存を解決し、最適なバージョンをインストールします。

```bash
curl -fsSL https://claude.ai/install.sh | bash
```
インストール後、自動的にパスが通され `claude` コマンドが利用可能になります。

#### B. Homebrew (macOSユーザー向け)
管理を一元化したい場合に最適です。

```bash
# Cask としてインストール
brew install --cask claude-code

# 通知機能の有効化 (オプション)
brew install terminal-notifier
```

#### C. npm Global Install (Node開発者向け)

```bash
npm install -g @anthropic-ai/claude-code
```

### 2.3 認証フロー (Authentication)

Claude Code は Anthropic の API を利用します。利用には2つのパスがあります。

1. **Claude Pro / Team / Enterprise サブスクリプション**
   - ブラウザ版 Claude.ai の有料プラン契約者は、追加料金なしで利用可能な場合があります（※プレビュー期間等の条件による）。
   - コマンドを実行:
     ```bash
     claude login
     ```
   - ブラウザが開くので、Claude.ai にログインして認証を許可します。

2. **Anthropic API Console (Credits)**
   - API キーを用いた従量課金モデル。企業での利用や、流量制限を個別に管理したい場合に推奨。
   - API キーを環境変数にセット:
     ```bash
     export ANTHROPIC_API_KEY="sk-ant-..."
     ```

---

## 3. アーキテクチャとコンテキスト管理

Claude Code が「賢い」と感じられる最大の理由は、そのコンテキスト管理の仕組みにあります。

### 3.1 プロジェクトコンテキスト (`CLAUDE.md`)
AI にプロジェクトの全体像を教えるための「説明書」。プロジェクトルートに配置します。Claude Code は起動時にこのファイルを読み、メモリに常駐させます。

**推奨される `CLAUDE.md` の構造:**

```markdown
# Claude Code Guidelines

## Environment
- OS: Ubuntu 22.04 (in Docker)
- Node: 20.11.0
- DB: PostgreSQL 16

## Key Commands
| Action | Command |
|--------|---------|
| Build  | `npm run build` |
| Test   | `npm test` (Unit), `npm run test:e2e` (E2E) |
| Lint   | `npm run lint` |
| DB Mig | `prisma migrate dev` |

## Architecture Decisions
- **State Mngt**: Redux Toolkit を使用。Context API は小規模な場合のみ。
- **Styling**: Tailwind CSS。カスタムクラスは `src/styles` に定義。
- **API**: GraphQL (Apollo Server)。REST は使用しない。

## Common Pitfalls
- `Date` 型は直接扱わず、必ず `date-fns` を経由すること。
- 非同期処理のエラーハンドリングはミドルウェアに委譲すること。
```

### 3.2 自動コンテキスト探索
`CLAUDE.md` がない場合でも、Claude Code は自律的に探索を行います。
- `find . -maxdepth 2 -not -path '*/.*'` を実行し、ファイル構造を把握。
- `package.json` や `Cargo.toml` を読み、依存関係を理解。
- `.gitignore` を読み、無視すべきファイルを学習。

### 3.3 コンテキストウィンドウの管理 (/compact)
会話が長くなると、トークン上限（現在は約200kトークン）に近づきます。動作が遅くなったり、コストが嵩む原因になります。
Claude Code は **`/compact`** コマンドを提供しています。

- **動作**: これまでの会話履歴（思考プロセスやツールの出力）を要約し、重要な決定事項と現状だけを残してメモリを圧縮します。
- **効果**: トークン使用量を 1/10 程度に削減し、セッションを長く維持できます。
- **自動化**: 設定により、一定トークンを超えたら自動で compact するようにも構成可能です。

---

## 4. MCP (Model Context Protocol) 連携

Claude Code は、Anthropic が提唱する **Model Context Protocol (MCP)** のクライアントとして動作します。これにより、ローカルファイル以外の「外部コンテキスト」を AI に提供できます。

### 4.1 MCP とは
AI モデルと外部データソース（GitHub, Slack, Database, Google Drive 等）を接続するための標準プロトコルです。
従来は「各ツールごとのプラグイン」が必要でしたが、MCP により統一的なインターフェースで接続可能になりました。

### 4.2 設定方法
`~/.claude/claude_mcp_config.json` にサーバー情報を記述します。

**例: GitHub と PostgreSQL を接続する設定**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp/postgres", "postgresql://user:pass@localhost:5432/db"]
    }
  }
}
```

### 4.3 利用シナリオ
設定後、Claude Code を再起動すると、以下のような指示が可能になります。

- **GitHub**: 「現在オープンになっている『バグ』ラベル付きの Issue をリストアップして、そのうち優先度が高いものを修正して」
- **Database**: 「users テーブルのスキーマを確認し、last_login カラムを追加するマイグレーションファイルを作成して」

---

## 5. コマンドリファレンス (Slash Commands)

対話プロンプト内で使用可能なコマンド群です。

| コマンド | 説明 | 詳細 |
|----------|------|------|
| `/help` | ヘルプ表示 | 利用可能なコマンドとショートカットを表示。 |
| `/clear` | リセット | コンテキストを完全に消去し、初期状態に戻す。タスク切り替え時に必須。 |
| `/compact`| 履歴圧縮 | 重要な情報を保持しつつ履歴を要約し、トークンを節約する。 |
| `/config` | 設定管理 | 現在の設定値を表示・変更する。 |
| `/cost` | コスト確認 | 現在のセッションで使用したトークン量と推定コストを表示。 |
| `/doctor` | 診断 | ネットワーク、認証、MCPサーバーの接続状況などを診断する。 |
| `/bug` | バグレポート | 発生した問題を含む状態でバグレポートを作成する。 |
| `/init` | 初期化 | `CLAUDE.md` のテンプレートを現在のディレクトリに作成する。 |
| `/pr` | PR作成支援 | 現在の変更内容を解析し、Pull Request のタイトルと説明文を生成する。 |
| `/review` | コードレビュー | 現在のステージングされている変更 (`git diff --cached`) をレビューする。 |

---

## 6. 実践的ワークフロー (Advanced Workflows)

### 6.1 TDD (テスト駆動開発) の完全自動化

**目標**: 新しいユーティリティ関数 `parseDate` を実装する。まずはテストから書く。

1. **指示**:
   ```bash
   claude "src/utils/date.ts に parseDate 関数を追加したい。まずはすべてのエッジケース（無効な日付、フォーマット違い）を網羅したテストケースを src/utils/date.test.ts に作成して。まだ実装はしなくていい。"
   ```
2. **AI動作**: 既存のテストファイルの書き方を学習し、テストコードを作成。
3. **確認**: `npm test` を実行させ、テストが失敗することを確認（Red）。
4. **実装指示**:
   ```bash
   claude "テストが通るように実装を行って。date-fns ライブラリを使用して。"
   ```
5. **AI動作**: 実装を行い、再度テストを実行。
6. **完了**: テストが通れば（Green）、タスク完了。

### 6.2 複数ファイルにまたがる大規模リファクタリング

**目標**: プロジェクト全体の CSS を、生の CSS Modules から Tailwind CSS に移行する。

1. **準備**: `CLAUDE.md` に移行ルール（クラス名の変換規則など）を追記。
2. **指示**:
   ```bash
   claude "src/components/Button ディレクトリ内のコンポーネントを Tailwind CSS に書き換えて。CSSファイルは削除し、tsxファイルにクラスを直接書いて。1つずつ順番にやって。"
   ```
3. **対話的実行**: Claude は1ファイルずつ修正・確認を求めてくる。
4. **一括承認**: 信頼できると感じたら `auto-approve` モードに切り替えて一気に進めることも可能（リスクあり）。

### 6.3 エラー調査と自動修正 (Debug Loop)

**目標**: 本番環境で発生した謎のエラーを修正する。

1. **ログ流し込み**:
   ```bash
   cat server.log | claude "この 'Connection reset' エラーの原因を特定し、再発防止策を実装して"
   ```
2. **推論**: Claude はログのタイムスタンプとスタックトレースを読み、DB接続プールのタイムアウト設定が怪しいと推論。
3. **検証**: DB設定ファイル (`ormconfig.ts`) を読み、タイムアウト値を確認。
4. **修正**: 設定値を変更し、負荷テストスクリプトを作成して実行提案。

---

## 7. 高度なカスタマイズ: Configuration Directory (`.claude/`)

Claude Code の真骨頂は、プロジェクト固有の `.claude/` ディレクトリによる拡張性にあります。単なる設定ファイル (`config.json`) を超えて、エージェントの振る舞い、能力 (Skills)、役割 (Agents) を自由に定義できます。

### 7.1 ディレクトリ構造

```text
.claude/
├── config.json       # 基本設定
├── rules/            # ルール定義 (旧 CLAUDE.md の分割・高度化)
│   ├── basic.md      # 基本的なコーディング規約
│   └── test.md       # テスト作成時の特記事項
├── skills/           # カスタムスキル (外部ツール連携)
│   ├── linear.py     # チケット管理システム連携スクリプト
│   └── deploy.sh     # デプロイスクリプト
├── agents/           # カスタムエージェント定義
│   ├── reviewer.yml  # レビュー特化エージェント
│   └── architect.yml # 設計特化エージェント
└── commands/         # カスタムスラッシュコマンド
    └── deploy.sh     # /deploy で呼び出せるコマンド
```

### 7.2 Custom Skills (`.claude/skills/`)
Claude に「新しい能力」を与えるためのスクリプト置き場です。
ここにある実行可能ファイルは、自動的に Claude のツールとして認識され、必要に応じて呼び出されます。

**例: `.claude/skills/fetch_ticket.py`**
```python
#!/usr/bin/env python3
"""
Description: Linear のチケット情報を取得するスキル
Usage: fetch_ticket.py <ticket_id>
"""
import sys
# ... (APIを叩く処理)
print(f"Ticket: {sys.argv[1]} - Title: Fix Login Bug")
```
Claude はファイルの冒頭コメント (Description/Usage) を読み取り、「チケットの内容を確認して」と言われた時にこのスクリプトを自律的に実行します。

### 7.3 Custom Agents (`.claude/agents/`)
特定のタスクに特化した「専門家エージェント」を定義します。
システムプロンプト、使用可能なスキル、参照すべきルールをプリセットとして保存できます。

**例: `.claude/agents/reviewer.yml`**
```yaml
name: Reviewer
description: コードレビューを行う厳格なエージェント
model: claude-3-7-sonnet
temperature: 0.1
system_prompt: |
  あなたはシニアエンジニアです。
  セキュリティ、パフォーマンス、可読性の観点から厳しくレビューしてください。
  肯定的なコメントは不要です。問題点のみを列挙してください。
skills:
  - git_diff
  - run_linter
rules:
  - rules/security.md
```

使用時: `claude --agent reviewer`

### 7.4 Rules (`.claude/rules/`)
`CLAUDE.md` が肥大化した場合、このディレクトリに分割して管理できます。
ファイル名自体がカテゴリとして認識され、コンテキストに応じて適切なルールが参照されます。

---

## 8. 設定とカスタマイズ (`config.json`)

`~/.claude/config.json` で詳細な挙動を制御できます。

```json
{
  "autoApprove": {
    "enabled": true,
    "allowedCommands": ["ls", "cat", "grep", "find", "git status"],
    "maxEdits": 5
  },
  "theme": "dark",
  "notifications": {
    "enabled": true,
    "thresholdSeconds": 30
  },
  "telemetry": {
    "enabled": false
  },
  "preferredModel": "claude-3-7-sonnet-20250219"
}
```

- **autoApprove**: 安全な読み取り系コマンドは自動承認し、書き込み系のみ確認するように設定すると、作業テンポが格段に向上します。
- **notifications**: 長いテストやビルドが終わった際にシステム通知（デスクトップ通知）を送る設定です。

---

## 8. セキュリティとベストプラクティス

1. **機密情報の扱い**: プロンプトに AWS キーやパスワードを直接書かないこと。`env` コマンドで環境変数を全部表示させないこと。Claude Code は `.env` ファイルの中身をうっかり読まないよう配慮されていますが、人間側でも注意が必要です。
2. **Ignore設定**: `.gitignore` に含まれていないが、AI に読ませたくないファイル（巨大なデータセットや秘匿ドキュメント）がある場合、`.claudeignore` ファイルを作成して除外設定を行ってください。
3. **Review**: AI が生成したコード、特にセキュリティに関わる部分（認証、決済、暗号化）は、必ず人間が詳細にレビューしてください。Claude は優秀ですが、脆弱性を作り込む可能性はゼロではありません。

---

## 9. まとめ

Claude Code は、開発者から「単純作業」を奪い、「意思決定」に集中させるためのツールです。
コマンドラインという、開発者が最も長く過ごす場所に AI を住まわせることで、コンテキストスイッチを減らし、Flow 状態を維持したまま開発を進めることができます。

まずはインストールし、`CLAUDE.md` を書き、小さなバグ修正から任せてみてください。すぐに、もうこれ無しの開発には戻れなくなるでしょう。
