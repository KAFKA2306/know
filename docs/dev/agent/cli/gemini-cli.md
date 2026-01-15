# Google Gemini CLI: 完全ガイド

**Gemini CLI** (`@google/gemini-cli`) は、Google が提供する最新のマルチモーダル AI モデル "Gemini" (Gemini 2.5 / 3.0 Pro, Flash) を、開発者のターミナルワークフローに直接統合するためのオープンソース・ツールキットです。
Google の強みである **検索 (Search Grounding)**、**マルチモーダル理解 (Multimodal)**、**巨大なコンテキストウィンドウ (1M+ Tokens)** をコマンドラインから手軽に、かつパワフルに活用できるように設計されています。

---

## 1. 概要: なぜ Gemini CLI なのか

### 1.1 "Vibe Coding" と "Grounding"
Gemini CLI は、近年提唱されている "Vibe Coding"（雰囲気や自然言語でざっくり指示してコードを書かせるスタイル）に最適化されています。しかし、単にコードを生成するだけではありません。
Google Search Grounding 機能により、**「今、世界で起きていること」** や **「最新のライブラリの破壊的変更」** をリアルタイムに検索・学習してから回答します。これにより、従来の LLM の弱点であった「知識のカットオフ（古い情報しか知らない）」や「ハルシネーション（嘘）」を劇的に改善しています。

### 1.2 マルチモーダルネイティブ
Gemini モデルは最初からマルチモーダルとして学習されています。Gemini CLI はこの特性を活かし、テキストだけでなく、画像、音声、動画、PDF、CSV など、あらゆる形式のファイルをパイプや引数として受け取り、解析・コード化することができます。

---

## 2. インストールと環境構築

### 2.1 システム要件
- **Runtime**: Node.js 18.0.0 以上 (20.x 推奨)
- **OS**: Cross-platform (macOS, Linux, Windows)
- **Terminal**: UTF-8 対応のターミナル (iTerm2, VSCode Terminal, Windows Terminal 等)

### 2.2 インストールオプション

#### A. npx (インストール不要・推奨)
最新版を常に利用したい場合、インストールせずに `npx` 経由で実行するのが最も手軽です。

```bash
npx @google/gemini-cli
```

#### B. npm Global Install (常用向け)
頻繁に利用する場合、グローバルインストールして `gemini` コマンドとして登録します。

```bash
npm install -g @google/gemini-cli

# バージョン確認
gemini --version
```

#### C. Homebrew (macOS)

```bash
brew install gemini-cli
```

### 2.3 認証設定 (Authentication)

Gemini CLI は複数のバックエンドに対応しています。利用シーンに合わせて選択してください。

#### 1. Google アカウント (OAuth) - 個人開発者向け
個人の Google アカウントでログインするだけで利用できます。
**特典**: Gemini API の **Free Tier** (無料枠) が適用されます。
- **レート制限**: 15 RPM (Requests Per Minute), 1,500 RPD (Requests Per Day) ※執筆時点
- **モデル**: Gemini 2.5 Flash / Pro (一部制限あり)

```bash
gemini auth login
```
ブラウザが開くので、Google アカウントでログインし、「Allow」をクリックします。認証情報はローカルのセキュアストレージに保存されます。

#### 2. API Key (Google AI Studio) - ヘビーユーザー向け
[Google AI Studio](https://aistudio.google.com/) で API キーを発行して利用します。Pay-as-you-go (従量課金) プランを利用したい場合や、CI/CD 環境での利用に適しています。

```bash
# 環境変数にセット
export GEMINI_API_KEY="AIzaSy..."

# または config に保存
gemini config set apiKey "AIzaSy..."
```

#### 3. Vertex AI (Google Cloud) - エンタープライズ向け
企業で Google Cloud Platform (GCP) を利用している場合、Vertex AI API を経由することで、企業のデータガバナンスポリシー（VPC SC、CMEK、ログ監査など）を適用できます。

```bash
# gcloud コマンドで認証
gcloud auth login
gcloud config set project <YOUR_PROJECT_ID>

# バックエンドを Vertex AI に切り替え
gemini config set backend vertex-ai
gemini config set region us-central1
```

---

## 3. コア機能詳細

### 3.1 Grounding with Google Search (検索連携)
Gemini CLI のキラー機能です。回答を生成する前に Google 検索を実行し、その結果をモデルに「事実」として与えます。

**使用例:**
```bash
gemini "Next.js 14 の Server Actions で、フォームバリデーションを行う最新のベストプラクティスコードを書いて。Zod を使って。" --grounding
```

**内部動作:**
1. プロンプトから検索クエリを生成 (例: "Next.js 14 Server Actions Zod validation best practices")
2. Google Search API を叩き、上位の検索結果（公式ドキュメントや主要な技術ブログ）を取得
3. 取得したテキストをコンテキストに追加してプロンプト再構築
4. 回答生成（情報源のリンクを脚注に追加）

この機能により、「1年前の知識で書かれた古いコード」ではなく、「昨日リリースされた新機能を使ったコード」が出力されます。

### 3.2 マルチモーダル入力 (Multimodal Input)

**画像 (Vision):**
UI のスクリーンショットからコードを生成したり、エラー画面のスクショから原因を特定したりできます。

```bash
# ローカルファイル
gemini "このデザインを HTML/Tailwind CSS で実装して" --image ./design/mockup.png

# URL指定
gemini "このグラフは何を表している？" --image https://example.com/chart.jpg
```

**PDF / ドキュメント:**
長い仕様書や論文を読み込ませることができます。

```bash
gemini "この仕様書に基づき、API の OpenAPI (Swagger) 定義ファイルを作成して" --file ./specs/api_v2.pdf
```

**動画 / 音声:**
会議の録画データなどを処理することも可能です（モデルの制限による）。

### 3.3 コンテキスト管理と `GEMINI.md`

プロジェクト固有の知識を固定化するために、`GEMINI.md` をプロジェクトルートに配置します。

**`GEMINI.md` テンプレート:**

```markdown
# Gemini Context

## Project Info
- Name: My EC Site
- Stack: Vue 3, Nuxt 3, Supabase

## Coding Style
- Use Composition API with `<script setup>`
- Use TypeScript interfaces, not types
- Comment in Japanese

## Preferred Libraries
- UI: PrimeVue
- State: Pinia
- Test: Vitest
```

CLI は起動時にこのファイルを読み込み、すべての対話の System Instruction として利用します。これにより、毎回「Vue 3 で書いて」と言わなくても、自動的に Vue 3 のコードが生成されます。

---

## 4. GitHub Actions 連携 (CI/CD Automation)

Gemini CLI は対話利用だけでなく、自動化ツールとしても優秀です。Google は公式の GitHub Action `google-github-actions/run-gemini-cli` を提供しています。

### シナリオ: 自動コードレビュー

Pull Request が作成された際に、変更差分を Gemini に読ませ、レビューコメントを自動投稿させるワークフローです。

**.github/workflows/gemini-review.yml**

```yaml
name: Gemini Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Gemini Review
        uses: google-github-actions/run-gemini-cli@v1
        with:
          # PRの差分を取得してプロンプトに埋め込む
          prompt: |
            あなたはシニアエンジニアです。以下のコード変更をレビューしてください。
            致命的なバグ、セキュリティリスク、パフォーマンスの問題があれば指摘してください。
            nitpick（些細な指摘）は不要です。
            
            DIFF:
            ${{ github.event.pull_request.diff_url }}
          api_key: ${{ secrets.GEMINI_API_KEY }}
        id: gemini

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: process.env.GEMINI_OUTPUT
            })
        env:
          GEMINI_OUTPUT: ${{ steps.gemini.outputs.response }}
```

このワークフローにより、人間がレビューする前に AI が一次チェックを行い、明らかなミスを指摘してくれます。

---

## 5. コマンドリファレンス完全版

### Global Commands

| コマンド | 引数/フラグ | 説明 |
|----------|-------------|------|
| `gemini` | `[prompt]` | 対話モード、またはワンショット実行します。 |
| `gemini auth` | `login`, `logout` | 認証情報を管理します。 |
| `gemini config` | `list`, `set`, `get` | 設定の確認と変更を行います。 |
| `gemini context` | `init`, `clear` | `GEMINI.md` の生成や、一時メモリのクリアを行います。 |
| `gemini update` | - | CLI 自体を最新版にアップデートします。 |

### Flags (実行オプション)

| フラグ | 説明 |
|--------|------|
| `--model <name>` | 使用するモデルを指定 (例: `gemini-1.5-pro-latest`) |
| `--grounding` | Google Search Grounding を有効化 (APIコスト増の可能性あり) |
| `--image <src>`| 画像入力。パスまたはURLを指定 (複数可) |
| `--file <src>` | ファイル入力。テキスト、PDF、コード等を読み込む |
| `--system <txt>`| システムプロンプトを一時的に上書き/追加 |
| `--tmperature` | 生成のランダム性を調整 (0.0 - 1.0) |
| `--json` | 出力を JSON 形式に強制 (スクリプト連携用) |
| `--no-stream` | ストリーミング出力を無効化し、完了まで待機 |

---

## 6. ユースケース別レシピ

### レシピ1: ライブラリのマイグレーション支援
「古い React クラスコンポーネントを、最新の Hooks (関数コンポーネント) に書き換える」

```bash
# フォルダ内の全ファイルを対象にする例（シェル機能利用）
for f in src/components/*.js; do
  gemini "以下のファイルを React Hooks に書き換えて。型定義も追加して。" --file "$f" > "${f%.js}.tsx"
done
```

### レシピ2: デザイン画像からのプロトタイプ生成
「ホワイトボードの落書きから、動く HTML/JS を作る」

```bash
gemini "このホワイトボードの図を元に、TODOアプリのプロトタイプを作って。Local Storage に保存する機能をつけて。" \
  --image whiteboard.jpg \
  --grounding # 最新のCSSフレームワークのトレンドを加味させる
```

### レシピ3: 英語ドキュメントの要約と翻訳
「海外の最新技術論文 (PDF) を日本語で3行で解説してもらう」

```bash
gemini "この論文の革新的な点はどこ？ 日本語で3つの箇条書きにして" --file paper.pdf
```

---

## 7. トラブルシューティング

### Q. `Quota exceeded` エラーが出ます。
**A.** 無料枠 (Free Tier) の制限 (60 RPM) を超えました。少し待つか、Google AI Studio で課金設定を行い、API Key 利用に切り替えてください。

### Q. 回答が途中で切れます。
**A.** デフォルトの出力トークン制限に達した可能性があります（モデルにより異なる）。`--max-output-tokens 8192` などのフラグで上限を引き上げてください。

### Q. ファイルを読み込めません。
**A.** 対応していないフォーマットか、ファイルサイズが大きすぎます (通常 20MB 程度まで)。テキストファイルであれば分割して渡すか、PDF に変換して渡すとうまくいくことがあります。

---

## 8. まとめ

Gemini CLI は、Google の AI 技術の結晶を手元のターミナルに凝縮したツールです。
特に **Google Search Grounding** は、他のコーディングエージェントにはない強力な武器です。「最新の情報」に基づいたコーディングを行いたい場合、Gemini CLI は最強の選択肢となるでしょう。

まずは `npx @google/gemini-cli` で、その "Grounding" の威力を体感してください。
