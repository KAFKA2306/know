# OpenAI Codex CLI: 完全ガイド

**OpenAI Codex CLI** は、OpenAI が提供する最先端の推論モデル（o1, o3, o4 シリーズなど）を、開発者のローカルターミナル環境に直接統合するためのオープンソース・コマンドラインインターフェースです。クラウド上の巨大な計算資源と、ローカルのセキュアな開発環境を安全かつ効率的にブリッジし、"Agentic Coding"（エージェント主導型コーディング）を実現します。

本ドキュメントでは、Codex CLI のインストールから高度な設定、プロンプトエンジニアリングの極意、トラブルシューティングに至るまで、あらゆる側面を網羅的に解説します。

---

## 1. 概要と哲学

### 1.1 背景: CLI エージェントの台頭
従来の「AI Coding Assistant」は、主に IDE のプラグイン（Copilot 等）として提供され、コード補完（Autocomplete）やチャット（Chat）を主機能としていました。しかし、これらはあくまで「人間がコードを書くのを助ける」ツールに過ぎませんでした。
Codex CLI はこのパラダイムを転換し、**「AI が主体的にコードを書き、ツールを実行し、検証する」** という **Agentic Workflow** を実現するために設計されました。

### 1.2 設計思想 (Design Philosophy)
- **Local First, Cloud Powered**: コードベースはローカルに保持し、必要なコンテキストのみをセキュアに送信する。
- **Unix Philosophy**: テキストストリームを入出力とし、パイプライン処理 (`|`) で他のツールと連携可能にする。
- **Safe Autonomy**: 「人間参加型（Human-in-the-loop）」の承認プロセスを核とし、AIの自律性と安全性を両立させる。
- **Model Agnostic Interface**: 将来のモデル（GPT-5, o5 等）が登場しても、CLI 自体のインターフェースを変えずに恩恵を受けられる抽象化層を持つ。

---

## 2. インストールと環境構築

### 2.1 システム要件
Codex CLI はクロスプラットフォームで動作しますが、最適なパフォーマンスを得るための推奨環境があります。

| 項目 | 最小要件 | 推奨要件 |
|------|----------|----------|
| **OS** | macOS 12+, Linux (Ubuntu 20.04+), Windows 10 | macOS 14+ (Apple Silicon), Ubuntu 22.04+, Windows 11 (WSL2) |
| **CPU** | x86_64, arm64 | Apple M-series, Modern AMD/Intel |
| **RAM** | 4GB | 8GB以上 (大規模コンテキスト処理用) |
| **Runtime**| Node.js 18+ | Node.js 20 LTS |
| **Network**| 10Mbps+ | 低遅延な光回線 (ストリーミング応答のため) |

### 2.2 インストール方法 (詳細)

#### A. npm によるグローバルインストール (標準)
Node.js 環境が整っている場合、これが最も手軽で更新も容易です。

```bash
# インストール
npm install -g @openai/codex

# バージョン確認
codex --version
# Output: @openai/codex v1.2.3
```

#### B. Homebrew (macOS/Linux)
システム管理されたパッケージとして導入したい場合に使用します。

```bash
brew tap openai/codex
brew install codex

# アップデート
brew upgrade codex
```

#### C. バイナリ直接配置 (CI/CD, 制限環境)
Node.js をインストールできない環境（CIランナーやセキュリティ制限のあるサーバー）では、コンパイル済みのバイナリを使用します。

1. [GitHub Releases](https://github.com/openai/codex/releases) から `codex-linux-x64` などをダウンロード。
2. 実行権限を付与してパスの通った場所に配置。

```bash
chmod +x codex-linux-x64
sudo mv codex-linux-x64 /usr/local/bin/codex
```

### 2.3 シェル補完 (Shell Completion)
コマンド入力の効率化のため、タブ補完を有効にすることを強く推奨します。

**Zsh:**
```bash
codex completion zsh > ~/.zsh/functions/_codex
echo 'fpath=(~/.zsh/functions $fpath)' >> ~/.zshrc
echo 'autoload -U compinit && compinit' >> ~/.zshrc
source ~/.zshrc
```

**Bash:**
```bash
codex completion bash > /etc/bash_completion.d/codex
source /etc/bash_completion.d/codex
```

---

## 3. 認証とプラン管理

Codex CLI のバックエンドには OpenAI の API が使用されます。利用形態に応じて2つの認証方法があります。

### 3.1 ChatGPT アカウント連携 (推奨)
ChatGPT Plus, Team, Enterprise プランのユーザー向け。**API 従量課金なし** で、プランに含まれる利用枠内で CLI を利用できます。

```bash
codex login
```
1. コマンドを実行すると、ブラウザが起動し `https://files.oaiusercontent.com/...` のような認証ページが開きます。
2. "Authorize" をクリックすると、ローカルにトークンが保存されます (`~/.openai/auth.json`)。

**メリット:**
- API Key 管理の手間がない
- ChatGPT の高度なモデル (o1-preview 等) がそのまま使える
- 企業プランの場合、データ学習への利用をオプトアウト設定が引き継がれる

### 3.2 API Key 認証 (開発者向け)
API Key を使用して、トークン単位で課金管理を行いたい場合や、Organization を切り替えて利用する場合に使用します。

```bash
export OPENAI_API_KEY="sk-proj-..."
export OPENAI_ORG_ID="org-..." # オプション
```

`.env` ファイルに記述して読み込ませることも可能です（`codex` コマンド実行時のカレントディレクトリの `.env` が優先されます）。

---

## 4. コア機能と承認モード

Codex CLI の最大の特徴は、AI の行動に対する「人間による制御（Agency Control）」の粒度を調整できる点です。

### 4.1 3つの承認モード (Approval Modes)

起動時に `--approval-mode` フラグで指定するか、設定ファイルでデフォルトを指定できます。

#### 1. Suggest Mode (デフォルト, 安全重視)
- **動作**: AI は「計画」と「変更案」を提示するだけです。
- **実行**: ユーザーが明示的に `y` (Yes) を入力しない限り、ファイルダンプもコマンド実行も行われません。
- **ユースケース**: クリティカルな本番環境、学習目的でのコードレビュー、慎重なリファクタリング。

#### 2. Auto Edit Mode (バランス型)
- **動作**: ファイルの編集（`write_file`, `replace_string`）は自動的に承認されます。
- **制限**: シェルコマンドの実行（`run_command`）、特に不可逆な操作（`rm`, `git push`）や外部通信（`curl`）はユーザーの承認を求めます。
- **ユースケース**: 通常の機能開発、テスト駆動開発 (TDD)。最も推奨されるモードです。

#### 3. Full Auto Mode (自律型)
- **動作**: 全てのアクションが自動承認されます。AI はゴールに到達するか、エラーで停止するまで動き続けます。
- **ユースケース**: 新規プロジェクトの足場作成 (Scaffolding)、完全に分離されたサンドボックス環境での実験、CI/CD パイプライン内での自動修復。
- **危険性**: ファイルの消失や意図しないシステム変更のリスクがあるため、Git 管理下での利用を強く推奨します。

```bash
# モード指定の例
codex --approval-mode full-auto "React + Vite の新規プロジェクトを作成して"
```

---

## 5. プロジェクトコンテキスト (Knowledge Injection)

AI に「ここがどこで、何をするプロジェクトなのか」を教えるための仕組みです。

### 5.1 `AGENTS.md` - エージェントへの指示書
プロジェクトのルートディレクトリに `AGENTS.md` を配置すると、Codex CLI は起動時にこれを読み込み、システムプロンプトに統合します。
このファイルには、プロジェクト固有のルールやコンテキストを記述します。

**`AGENTS.md` の構成例:**

```markdown
# Agent Configurations

## Identity & Tone
- あなたは Google のシニアソフトウェアエンジニアレベルのスキルを持つ Python エキスパートです。
- 回答は簡潔に、コード中心で行ってください。
- 日本語で応答してください。

## Architecture Overview
- **Frontend**: Next.js 14 (App Router), Tailwind CSS
- **Backend**: FastAPI (Python 3.11), SQLAlchemy
- **Database**: PostgreSQL
- **Infrastructure**: AWS (Terraform)

## Coding Standards
- **Python**: PEP 8 準拠。Type Hint は必須。Docstring は Google Style。
- **TypeScript**: Strict mode enabled. `any` 型の使用禁止。
- **Testing**:
    - Backend: `pytest` を使用。カバレッジ 80% 以上維持。
    - Frontend: `vitest` を使用。

## Workflow Rules
1. 変更を加える前に必ずテストを実行し、現状を確認すること。
2. コード変更後はテストを再実行し、リグレッションがないか確認すること。
3. コミットメッセージは [Conventional Commits](https://www.conventionalcommits.org/) に従うこと（例: `feat: add user login`）。
```

### 5.2 自動コンテキスト収集 (RAG)
Codex CLI は、大規模なコードベースを扱うために、簡易的な RAG (Retrieval-Augmented Generation) 機能を内蔵しています。
- `.gitignore` に記載されたファイルは自動的に無視されます。
- 初期起動時にファイルツリーをスキャンし、重要そうなファイル（`README.md`, `package.json`, `pyproject.toml` 等）の要約をメモリに保持します。

---

## 6. コマンドリファレンス (Command Reference)

### 6.1 基本コマンド

| コマンド | 説明 |
|----------|------|
| `codex` | 対話モード (REPL) を開始。 |
| `codex "prompt"` | ワンショット実行。タスク完了後終了。 |
| `codex login` | ChatGPT アカウントでログイン。 |
| `codex logout` | ログアウトし、APIキーを削除。 |
| `codex version` | バージョン情報を表示。 |
| `codex check` | 環境診断（API接続、権限確認）。 |

### 6.2 主要なフラグ (Flags)

| フラグ | 短縮形 | 説明 |
|--------|--------|------|
| `--model <name>` | `-m` | 使用するモデルを指定 (`o1`, `gpt-4o`, `gpt-3.5-turbo`)。デフォルトは最適化されたモデル。 |
| `--file <path>` | `-f` | コンテキストとしてファイルを明示的に読み込む。複数指定可。 |
| `--image <path>` | `-i` | 画像ファイルを読み込む（マルチモーダル）。 |
| `--approval-mode` | `-a` | `suggest` / `auto-edit` / `full-auto` |
| `--verbose` | `-v` | デバッグ用の詳細ログを出力。プロンプトの内容も確認可能。 |
| `--quiet` | `-q` | 余計な出力を抑制。スクリプト実行用。 |
| `--path <dir>` | `-C` | 実行ディレクトリを変更して起動。 |

### 6.3 便利なショートカット

対話モード中には、以下の「スラッシュコマンド」が利用可能です。

- `/clear` または `/reset`: 会話履歴を消去し、コンテキストウィンドウを解放する。トークン節約に有効。
- `/diff`: 現在の未コミットの変更を表示する。
- `/undo`: 直前の AI による変更（ファイル編集）を取り消す。
- `/copy`: 直前の回答コードをクリップボードにコピーする。
- `/exit` または `/quit`: 終了する。

---

## 7. 高度な使用例 (Advanced Scenarios)

### シナリオ1: レガシーコードのリファクタリング

**状況**: テストがなく、ドキュメントもない古い Python スクリプト (`legacy_script.py`) を解析し、最新の Modern Python に書き換えたい。

**手順**:

```bash
# 1. 解析とテスト作成
codex -a auto-edit "legacy_script.py を解析して。まず現在の挙動を保証する単体テストを pytest で作成して。テストファイル名は tests/test_legacy.py にして"

# 2. テストパス確認
# (AI が pytest を実行し、パスすることを確認する)

# 3. リファクタリング実行
codex -a auto-edit "テストが通ることを維持しながら、legacy_script.py を以下の要件でリファクタリングして：
1. クラスベースの設計に変更
2. Type Hint を全関数に追加
3. 変数名をわかりやすく変更 (snake_case)
4. グローバル変数を廃止"

# 4. ドキュメント生成
codex "legacy_script.py の仕様書を MARKDOWN 形式で docs/spec.md に書き出して"
```

### シナリオ2: 画像からの UI 実装 (Design to Code)

**状況**: デザイナーから渡された画面デザイン (`design_mockup.png`) を元に、React コンポーネントを実装したい。

**手順**:

```bash
codex -m gpt-4o --image design_mockup.png \
  "この画像を元に、React + Tailwind CSS でコンポーネントを実装して。
  ファイルは src/components/UserProfile.tsx に保存して。
  アイコンには lucide-react を使用して。"
```

### シナリオ3: エラーログからのバグ修正

```bash
# パイプ入力によるデバッグ
cat /var/log/app/error.log | codex "このスタックトレースを分析し、原因と修正案を教えて。修正案はコードブロックで出力して。"
```

---

## 8. トラブルシューティングとFAQ

### Q1. モデルがファイルを見つけてくれません。
**A.** Codex CLI は `.gitignore` を尊重します。対象ファイルが無視されていないか確認してください。また、明示的に `--file <path>` で渡すことで確実に見せることができます。また、`ls -R` コマンドを実行させてファイル構造を再認識させるのも手です。

### Q2. "Context Window Exceeded" エラーが出ます。
**A.** `/clear` コマンドで履歴をリセットしてください。また、不要なファイルを読み込みすぎている可能性があります。`AGENTS.md` で読み込む範囲を制限するか、具体的なタスクに分割して指示してください。

### Q3. 「シェルコマンドを実行できません」と拒否されます。
**A.** `Suggest Mode` になっている可能性があります。`--approval-mode auto-edit` または `full-auto` を試してください。または、プロンプトで「コマンドを実行して」と強く指示してみてください。

### Q4. 企業内プロキシ環境で使えますか？
**A.** `HTTP_PROXY`, `HTTPS_PROXY` 環境変数を参照します。認証が通らない場合は、自社証明書を `NODE_EXTRA_CA_CERTS` に設定する必要があるかもしれません。

---

## 9. セキュリティとプライバシー

Codex CLI はローカルで動作するため、基本的にはセキュアですが、以下の点に注意してください。

1. **データ送信**: プロンプトに含まれるファイルの内容や指示は、OpenAI API に送信されます。機密情報（パスワード、APIキー、PII）が含まれないように注意してください。`gitleaks` 等のツールと併用することを推奨します。
2. **学習利用**: ChatGPT Enterprise / Team アカウントでログインしている場合、データはモデルの学習に使用されません。Personal Plus プランの場合は設定によります。
3. **サンドボックス**: `Full Auto Mode` は強力ですが、誤って `rm -rf /` のようなコマンドを実行するリスクがゼロではありません（AIは通常拒否しますが）。Docker コンテナや VM 内での実行を推奨します。

---

## 10. まとめ

OpenAI Codex CLI は、開発者の「手」を増やすだけでなく、「脳」の一部を外部化し、並列処理を可能にする強力なツールです。使いこなすための鍵は、**「明確な指示 (Prompting)」「適切なコンテキスト設定 (AGENTS.md)」「自律レベルの制御 (Modes)」** の3点にあります。

これらをマスターすることで、あなたの生産性は 10x にもなり得ます。Happy Coding!
