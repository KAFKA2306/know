# Git

## 基本コマンド

| コマンド | 説明 |
|---------|------|
| `git status` | 変更状態を確認 |
| `git add -A` | 全ての変更をステージ |
| `git commit -m "msg"` | コミット |
| `git push` | リモートへプッシュ |
| `git pull` | リモートから取得 |
| `git log -n 5` | 直近5件のログ |

## ブランチ操作

| コマンド | 説明 |
|---------|------|
| `git branch` | ブランチ一覧 |
| `git checkout -b feature` | 新規ブランチ作成・切替 |
| `git merge feature` | ブランチをマージ |
| `git branch -d feature` | ブランチ削除 |

## 取り消し操作

| コマンド | 説明 |
|---------|------|
| `git restore <file>` | 変更を破棄 |
| `git restore --staged <file>` | ステージを解除 |
| `git reset --soft HEAD~1` | 直前のコミットを取消（変更は保持） |
| `git reset --hard HEAD~1` | 直前のコミットを完全に取消 |

## リモート操作

| コマンド | 説明 |
|---------|------|
| `git remote -v` | リモート一覧 |
| `git fetch origin` | リモートの情報を取得 |
| `git push -u origin main` | 初回プッシュ（上流設定） |

## スタッシュ

| コマンド | 説明 |
|---------|------|
| `git stash` | 変更を一時退避 |
| `git stash pop` | 退避した変更を復元 |
| `git stash list` | スタッシュ一覧 |

## GitHub CLI (gh)

| コマンド | 説明 |
|---------|------|
| `gh repo clone user/repo` | リポジトリをクローン |
| `gh pr create` | PRを作成 |
| `gh pr list` | PR一覧 |
| `gh run list` | ワークフロー実行一覧 |
| `gh run watch` | ワークフロー実行を監視 |

## .gitignore

```gitignore
# Python
__pycache__/
*.pyc
.venv/

# Node
node_modules/

# IDE
.idea/
.vscode/

# OS
.DS_Store
```

## コミットメッセージ規約

```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント更新
style: フォーマット修正
refactor: リファクタリング
test: テスト追加・修正
chore: ビルド・ツール変更
```
