# Google Antigravity: 完全ガイド

**Google Antigravity** は、Google が提唱する次世代のソフトウェア開発パラダイム **"Agent-First Development"** (エージェントファースト開発) を具現化するためにゼロから設計された、**AIネイティブ統合開発環境 (IDE)** です。

既存の IDE (VS Code, IntelliJ) に AI プラグインを追加するアプローチとは根本的に異なり、Antigravity は「AI エージェントが主たる作業者であり、人間は監督者（Supervisor）である」という思想のもとに構築されています。開発者は自らコードを書く時間よりも、エージェントに指示を出し、生成された成果物（Artifacts）をレビューし、アーキテクチャを決定することに時間を費やすようになります。

---

## 1. 概念: The Agent-First Paradigm

### 1.1 従来の開発 vs Antigravity
- **従来**: 人間がエディタを開き、思考し、タイプし、エラーが出たら修正する。AI は「補完」や「チャット」でそれを助けるだけ。
- **Antigravity**: 人間は「タスク」を定義する。自律エージェントが計画を立て、エディタを操作し、ターミナルを叩き、ブラウザで動作確認を行う。人間はそのプロセスを監視し、最終結果を承認する。

### 1.2 "Mission Control" (ミッションコントロール)
Antigravity のメインインターフェースは、コードエディタではなく **Agent Manager**（通称 Mission Control）です。ここでは、複数のエージェントを並列に起動し、それぞれに異なるタスク（機能実装、バグ修正、リファクタリング、テスト作成）を割り当て、その進捗を一元管理します。

---

## 2. アーキテクチャとコンポーネント

Antigravity は、大きく分けて以下の4つのコアコンポーネントで構成されています。

### 2.1 Autonomous Agents (自律エージェント)
システムの主役です。Gemini 3 Pro / Deep Think モデルを脳として持ち、以下の能力を有します。
- **Perception (知覚)**: プロジェクト全体のファイル構造、依存関係、Git の履歴、現在の開いているファイル、カーソル位置などをリアルタイムに認識。
- **Planning (計画)**: 複雑なタスクを「調査」「設計」「実装」「検証」といったサブタスクに分解し、実行計画 (Implementation Plan) を立案。
- **Tool Use (道具の使用)**: ファイル編集、シェルコマンド実行、ブラウザ操作、LSP (Language Server Protocol) の呼び出しなどを自律的に行う。

### 2.2 The Editor (AI-Native Editor)
Visual Studio Code (VS Code) をベースにフォークされていますが、以下の点が AI 向けに改造されています。
- **Stream Editing**: エージェントが超高速でコードを生成・編集するための専用パイプライン。人間が見ていなくてもバックグラウンドで編集が進む。
- **Semantic Indexing**: プロジェクト全体をベクトル化し、エージェントが「あの認証ロジックどこだっけ？」を一瞬で検索できるようにする常駐インデックス。
- **Diff View**: エージェントによる変更を人間が瞬時に理解し、Accept/Reject を判断するための高度な差分表示 UI。

### 2.3 Browser Subagent (ブラウザサブエージェント)
Antigravity には、Chromium ベースのヘッドレス（またはヘッドあり）ブラウザが統合されています。
エージェントはこれを操作して、以下のタスクを実行できます。
- **E2E Testing**: ローカルサーバーを立ち上げ、実際にボタンをクリックし、遷移を確認する。
- **User Simulation**: 「ユーザーとして新規登録フローを通す」といったシナリオを実行。
- **Visual Debugging**: 画面のスクリーンショットを撮り、CSS 崩れや配置ミスを画像認識で特定する。

### 2.4 Artifacts System (成果物システム)
エージェントとのコミュニケーションは、チャットのテキストだけでなく、構造化された「成果物」を通じて行われます。
- **Plan Artifact**: 「これからこういう手順で実装します」という計画書。
- **Task Artifact**: 進捗管理のためのチェックリスト。
- **Preview Artifact**: 実装中の画面プレビューや、動作検証の録画ビデオ。

### 2.5 Custom Skills & Agents
Antigravity は拡張性も極めて高く、`.antigravity/` ディレクトリでエージェントの能力を拡張できます。

- **Custom Skills**: Python や TypeScript で書かれた関数を `skills/` に配置すると、エージェントのツールボックスに自動追加されます。
    - 例: `skills/query_bigquery.py` を置けば、エージェントが「BigQuery から先月の売上データを取ってきて」という指示を実行できるようになります。
- **Agent Personas**: `agents/` に定義ファイル (YAML) を置くことで、特定の役割を持ったエージェント（例: `QA-Engineer`, `Security-Auditor`）を作成し、Mission Control から呼び出せるようになります。

---

## 3. インストールとセットアップ

Antigravity は現在、**Public Preview** (招待制/ウェイティングリスト) ステータスです。

### 3.1 エディション
1. **Antigravity Web**: ブラウザ上で動作するフルクラウド IDE。環境構築不要で、Google の強力なコンピュートリソースを利用可能。
2. **Antigravity Desktop**: macOS, Windows, Linux 向けのネイティブアプリ。ローカルのリソースとファイルシステムを利用できる。

### 3.2 必須要件 (Desktop版)
- **OS**: macOS 13+, Windows 11, Linux (Debian/Ubuntu)
- **RAM**: 16GB 以上推奨 (ローカルで Agent を動作させるわけではないが、IDE 自体がリッチなため)
- **Account**: Google Cloud Platform (GCP) が有効な Google アカウント。

### 3.3 認証
起動時に Google アカウントでのサインインが求められます。
企業利用の場合、IAM ポリシーに基づき、Antigravity がアクセスできるリポジトリやリソースを制限することが可能です。

---

## 4. 実践ワークフロー: 機能実装の全貌

「ECサイトにショッピングカート機能を追加する」というタスクを例に、Antigravity でのワークフローを解説します。

### Step 1: Goal Setting (目標設定)
Mission Control 画面で、新しいエージェント "Feature-Cart" を召喚し、指示を出します。

> **User**: 「商品詳細ページに『カートに入れる』ボタンを追加し、ヘッダーのカートアイコンにバッジで点数を表示するようにして。状態管理は Pinia を使って。」

### Step 2: Planning & Research (調査と計画)
エージェントはまずコードベースをスキャンし、現状の Pinia ストアや商品ページのコンポーネント構成を把握します。そして **Implementation Plan Artifact** を生成し、人間に提示します。

> **Agent**: 「以下の計画を立てました。
> 1. `stores/cart.ts` を作成し、カート状態ロジックを実装。
> 2. `components/ProductDetail.vue` にボタン追加。
> 3. `components/Header.vue` にバッジ表示ロジック追加。
> 4. ブラウザテストで動作確認。
> これで進めて良いですか？」

> **User**: 「OK。ただし、カートに入れた時はトースト通知も出して。」

エージェントは計画を修正し、実行フェーズに入ります。

### Step 3: Execution (実装)
エージェントはエディタを操作し、猛烈なスピードでコーディングを開始します。
- `stores/cart.ts` を作成...
- `Header.vue` を修正...
- 途中で TypeScript の型エラーが発生。エージェントは自律的に `tsc` を実行してエラー内容を確認し、型定義を修正します。これが「自律修復」です。

### Step 4: Verification (検証)
コーディングが完了すると、エージェントはブラウザサブエージェントを起動します。
1. ローカル開発サーバー (`npm run dev`) を起動。
2. `http://localhost:3000/product/1` にアクセス。
3. 「カートに入れる」ボタンをクリック。
4. トースト通知が表示されたか、ヘッダーのバッジが増えたかを確認（DOM解析 + 画像認識）。

エージェントは検証の様子を録画し、**Verification Video Artifact** としてレポートします。

### Step 5: Review & Merge (レビューとマージ)
人間はレポートとビデオを見て、問題なければコードの差分 (Diff) を最終確認します。
「Merge」ボタンを押すと、Git コミットとプッシュが行われます。

---

## 5. 高度な機能

### 5.1 Project Memory (プロジェクトメモリ)
Antigravity は、過去のエージェントの活動を記憶しています。「先週の実装で、認証周りのバグをどうやって直したっけ？」と聞けば、過去のコンテキストから回答を引き出せます。
また、`AGENTS.md` などの設定ファイルを通じて、チーム固有の知識（「うちはこのライブラリ禁止」等）を持続的に学習させることができます。

### 5.2 Parallel Agents (並列エージェント)
一人の開発者が複数のエージェントを同時に使うことができます。
- **Agent A**: 新機能の実装（メインタスク）
- **Agent B**: 裏でライブラリのアップデートと移行検証
- **Agent C**: ドキュメントの整備と翻訳

これらを Mission Control で並行して走らせることで、生産性を数倍に引き上げます。

### 5.3 Cross-File Refactoring
「プロジェクト内のすべての `var` を `const` に変え、古いロギング関数を新しいものに置換する」
このような単純だが広範囲にわたる修正は、Antigravity の得意分野です。数千ファイル規模でも、エージェントは諦めずに最後までやり遂げます。

---

## 6. Gemini CLI との使い分け

Google は Antigravity と [Gemini CLI](gemini-cli.md) という2つのツールを提供していますが、役割は明確に異なります。

| 特徴 | Google Antigravity | Gemini CLI |
|------|--------------------|------------|
| **形態** | **IDE (統合開発環境)** | **CLI ツール** |
| **主用途** | 複雑な機能開発、E2Eテスト、並列タスク | スクリプト生成、ログ解析、ワンショット修正 |
| **コンテキスト** | プロジェクト全体、Git履歴、実行時メモリ | カレントディレクトリ、渡されたファイル |
| **UI** | リッチなGUI、動画プレビュー | テキストのみ |
| **起動** | 重厚（アプリ起動） | 瞬時（コマンド叩くだけ） |

**結論**: 日々のガッツリした開発は Antigravity で行い、ターミナル作業中や CI パイプラインでの自動化には Gemini CLI を使う、という併用が最強のスタイルです。

---

## 7. まとめ

Google Antigravity は、IDE の再発明です。それは「文字を打つ道具」から「意図を形にする工場」への進化です。
エージェントファースト開発に慣れると、もう以前の「手入力」スタイルの開発には戻れないかもしれません。AI をパートナーではなく、**有能な部下**として指揮する新しい開発体験へようこそ。

---

## 参照
- [Antigravity Official Site](https://antigravity.google/)
- [Waitlist Registration](https://antigravity.google/waitlist)
- [Example Workflows](https://antigravity.google/docs/workflows)
