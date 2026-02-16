# 型システムと契約

コメントの代わりに型で語る。Pydantic モデルとネイティブ型ヒントによる「契約プログラミング」。

## Python 3.11 型ヒントの体系

### 基本型

```python
name: str = "RuleScribe"
count: int = 42
ratio: float = 0.95
is_active: bool = True
```

### コンテナ型（ビルトイン構文）

```python
tags: list[str] = ["strategy", "card"]
scores: dict[str, int] = {"alice": 100, "bob": 85}
result: tuple[str, int] = ("success", 200)
maybe: str | None = None
```

!!! tip "Python 3.10+ の Union 構文"
    `Optional[str]` ではなく `str | None` を使う。`UP` (pyupgrade) ルールが自動変換する。

### 関数シグネチャ

```python
async def generate_metadata(query: str, context: str | None = None) -> dict[str, object]:
    ...
```

戻り値 `dict[str, object]` は「何でも入る辞書」を意味する。
`ANN` ルールが型ヒントの欠如を検出する。

## Pydantic によるバリデーション

### モデル定義

`rule-scribe-games` の `GeneratedGameMetadata` はデータの「契約」を定義する。

```python
from pydantic import BaseModel

class GeneratedGameMetadata(BaseModel):
    title: str
    title_ja: str | None = None
    title_en: str | None = None
    slug: str
    summary: str
    rules_content: str
    min_players: int | None = None
    max_players: int | None = None
    play_time: str | None = None
    min_age: int | None = None
    published_year: int | None = None
```

**設計判断**:

- 必須フィールド（`title`, `slug`, `summary`, `rules_content`）はデフォルトなし → 欠けると例外
- オプションフィールドは `| None = None` → AI が生成できなくても許容
- コメント不要。型とフィールド名が仕様書そのもの

### バリデーションの実行

```python
validated_data = GeneratedGameMetadata.model_validate(result)
data = validated_data.model_dump()
data = {k: v for k, v in data.items() if k in _ALLOWED_FIELDS}
```

**3段階のフィルタリング**:

1. `model_validate`: 型チェック（不正な型は例外）
2. `model_dump`: Pydantic モデル → 辞書に変換
3. `_ALLOWED_FIELDS`: ホワイトリストでフィールドを制限

## ホワイトリストパターン

```python
_ALLOWED_FIELDS = {"id", "slug", "title", ...}
data = {k: v for k, v in data.items() if k in _ALLOWED_FIELDS}
```

!!! warning "なぜブラックリストではなくホワイトリストか"
    ブラックリスト（`if k not in BLOCKED`）は新しいフィールドが追加されたとき**デフォルトで許可**してしまう。
    ホワイトリストは新しいフィールドを**デフォルトで拒否**する。セキュリティの基本原則。

## `dataclass` vs `Pydantic`

| 特性 | `dataclass` | `Pydantic BaseModel` |
|------|-------------|---------------------|
| バリデーション | なし | 自動 |
| JSON シリアライズ | 手動 | `model_dump_json()` |
| パフォーマンス | 高速 | やや遅い |
| 用途 | 内部データ構造 | API 境界、外部入力 |

**使い分けルール**: 外部データ（API、AI レスポンス）→ Pydantic。内部計算 → dataclass。

## 演習

### 問1: 型エラーを見つけよ

```python
def process_game(data: dict) -> str:
    title = data["title"]
    count = data.get("view_count", "0")
    return f"{title}: {count + 1} views"
```

??? note "解答"
    - `data: dict` → `data: dict[str, object]` （`ANN` ルール違反）
    - `count` は `str` 型（`"0"`）なのに `+ 1` している → `TypeError`
    - 修正: `count = int(data.get("view_count", 0))`

### 問2: Pydantic モデルを設計せよ

以下の JSON を受け取るモデルを定義せよ:

```json
{
  "name": "カタン",
  "players": {"min": 3, "max": 4},
  "duration_minutes": 90,
  "tags": ["strategy", "negotiation"]
}
```

??? note "解答"
    ```python
    from pydantic import BaseModel

    class PlayerRange(BaseModel):
        min: int
        max: int

    class GameInput(BaseModel):
        name: str
        players: PlayerRange
        duration_minutes: int
        tags: list[str]
    ```

## チェックリスト

- [ ] `str | None` と `Optional[str]` の違いを説明できる
- [ ] Pydantic で `model_validate` が失敗するケースを3つ挙げられる
- [ ] ホワイトリストパターンのセキュリティ上の利点を説明できる
- [ ] `dataclass` と `Pydantic` の使い分け基準を持っている
