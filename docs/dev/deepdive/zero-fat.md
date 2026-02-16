# Zero-Fat 設計論

「不純物ゼロ」の設計思想。コードから冗長性を徹底排除し、成功パスのロジックだけを残す。

## コア原則

| 原則 | 意味 | 禁止されるもの |
|------|------|---------------|
| **Silent Operator** | コードは自己記述的であれ | コメント、Docstring |
| **Fail Fast** | 予期せぬ事象は即座にクラッシュ | `try-catch`, `try-except` |
| **Zero-Fat** | 未使用コードを徹底削除 | リトライ、タイムアウト、デッドコード |

## Ruff ルールの解読

ルート `pyproject.toml` で定義された Ruff ルールの意味を理解する。

```python
select = [
    "E",     # pycodestyle errors — PEP 8 準拠
    "F",     # pyflakes — 未使用 import、未定義変数
    "B",     # flake8-bugbear — よくあるバグパターン
    "I",     # isort — import の並び順
    "N",     # pep8-naming — 命名規則
    "UP",    # pyupgrade — 古い構文の自動更新
    "PL",    # pylint — コード品質
    "SIM",   # flake8-simplify — 条件式の簡略化
    "ANN",   # flake8-annotations — 型アノテーション必須
    "ERA",   # eradicate — コメントアウトされたコード検出
    "T20",   # flake8-print — print文の検出
    "RET",   # flake8-return — return文の最適化
    "ARG",   # flake8-unused-arguments — 未使用引数
    "PTH",   # flake8-use-pathlib — os.path → pathlib
    "PIE",   # flake8-pie — 不要な構文
    "RUF",   # Ruff固有 — 追加のベストプラクティス
]
```

!!! warning "特に重要なルール"
    - **ERA**: コメントアウトされたコードを「死」として検出する。Zero-Fat の核心。
    - **ANN**: 型ヒントの欠如を許さない。コメントの代わりに型で意図を伝える。
    - **T20**: `print` デバッグを許さない。ロガーを使うか、削除する。

## 実例分析: `game_service.py`

`rule-scribe-games/app/services/game_service.py` から Zero-Fat パターンを学ぶ。

### パターン 1: ホワイトリスト定数

```python
_ALLOWED_FIELDS = {
    "id", "slug", "title", "title_ja", "title_en",
    "description", "summary", "rules_content",
    "structured_data", "source_url", "affiliate_urls",
    "view_count", "search_count", "data_version",
    "is_official", "min_players", "max_players",
    "play_time", "min_age", "published_year",
    "image_url", "official_url", "bgg_url", "bga_url",
    "amazon_url", "audio_url", "created_at", "updated_at",
}
```

**なぜこう書くか**: コメントなしで「何が許可されているか」を定数自体が表現する。
変数名 `_ALLOWED_FIELDS` が自己記述的。セットのイミュータビリティがバリデーションの意図を暗示する。

### パターン 2: 早期リターンによる Fail Fast

```python
async def update_game_content(self, slug: str, fill_missing_only: bool = False) -> dict[str, object]:
    game = await supabase.get_by_slug(slug)
    if not game:
        return {}
    ctx = f"{game.get('title')}: {game.get('summary')}"
    result = await generate_metadata(str(game.get("title")), ctx)
    merged = _merge_fields(game, result, fill_missing_only)
    merged["id"], merged["slug"] = game["id"], slug
    merged["data_version"] = int(game.get("data_version", 0) or 0) + 1
    out = await supabase.upsert(merged)
    return out[0] if out else {}
```

**観察ポイント**:

- `try-except` が一切ない。`supabase.get_by_slug` が失敗すれば例外が伝播してクラッシュする。
- `if not game: return {}` は唯一の分岐。成功パスが直線的に読める。
- 各変数は一度だけ代入され、パイプラインのように流れる。

## 演習: リファクタリング

以下のコードを Zero-Fat 原則に従ってリファクタリングせよ。

### Before

```python
def get_user_data(user_id: int):
    """ユーザーデータを取得する関数"""
    try:
        # データベースからユーザーを検索
        user = db.find_user(user_id)
        if user is None:
            print(f"User {user_id} not found")  # デバッグ用
            return None
        
        # ユーザー名を整形
        name = user.name.strip()
        # メールアドレスを小文字に
        email = user.email.lower()
        
        return {"name": name, "email": email}
    except Exception as e:
        print(f"Error: {e}")
        # return None  # 旧実装
        return None
```

### After

```python
def get_user_data(user_id: int) -> dict[str, str] | None:
    user = db.find_user(user_id)
    if user is None:
        return None
    return {"name": user.name.strip(), "email": user.email.lower()}
```

**削除されたもの**:
Docstring (1行) + コメント (4行) + try-except (3行) + print (2行) + デッドコード (1行) = **11行 → 4行**

## チェックリスト

- [ ] `ERA` ルールの意味を説明できる
- [ ] 自分のコードで `try-except` を使っている箇所を特定し、削除の可否を判断できる
- [ ] 「コメントを書くべき場面」と「変数名で表現すべき場面」を区別できる
- [ ] `ruff check . --fix` をプロジェクトに適用し、結果を解釈できる
