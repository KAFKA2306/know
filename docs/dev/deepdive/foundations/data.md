# データとは何か

コンピュータが扱うすべての情報の根本を理解する。

## ビットとバイト

コンピュータが理解できるのは **0** と **1** だけ。これを**ビット（bit）**と呼ぶ。

| 単位 | 大きさ | 例 |
|------|--------|-----|
| 1 bit | 0 or 1 | スイッチの ON/OFF |
| 1 byte (8 bits) | 0〜255 | 英字1文字 |
| 1 KB (1,024 bytes) | 約1,000文字 | 短いメール |
| 1 MB (1,024 KB) | 約100万文字 | 写真1枚 |
| 1 GB (1,024 MB) | 約10億文字 | 映画1本 |

## 数値の表現

### 整数（int）

```
10進数: 42
2進数:  0b101010  (= 32 + 8 + 2 = 42)
16進数: 0x2A
```

### 浮動小数点数（float）

```
3.14  →  コンピュータ内部: 符号(1bit) + 指数(11bit) + 仮数(52bit)
```

!!! warning "浮動小数点の罠"
    ```python
    >>> 0.1 + 0.2
    0.30000000000000004
    ```
    金額計算では `Decimal` 型を使う。`auto-invest` プロジェクトではこれが重要。

## 文字の表現（エンコーディング）

文字は「数値と文字の対応表」で表現される。

| エンコーディング | 特徴 | 例 |
|----------------|------|-----|
| ASCII | 英数字のみ、1バイト | `A` = 65 |
| UTF-8 | 全世界の文字、可変長 | `あ` = 3バイト |
| Shift_JIS | 日本語旧規格 | Windows レガシー |

自分のプロジェクトはすべて **UTF-8**。`mkdocs.yml` や `.py` ファイルの日本語が正しく表示されるのはこのおかげ。

```python
"カタン".encode("utf-8")
```

## データ構造

### プリミティブ型（スカラー）

プログラムの最小単位。

```python
name: str = "RuleScribe"     # 文字列
count: int = 42               # 整数
ratio: float = 0.95           # 浮動小数点数
is_active: bool = True        # 真偽値
nothing: None = None           # 値なし
```

### コレクション型

複数のデータをまとめる。

```python
tags: list[str] = ["strategy", "card", "negotiation"]

player_scores: dict[str, int] = {
    "alice": 100,
    "bob": 85,
}

coordinate: tuple[int, int] = (3, 7)

unique_ids: set[str] = {"a1", "b2", "c3"}
```

| 型 | 順序 | 重複 | 変更 | 用途 |
|----|------|------|------|------|
| `list` | あり | 可 | 可 | 汎用的な配列 |
| `tuple` | あり | 可 | 不可 | 固定データ |
| `dict` | あり | キー不可 | 可 | キーバリュー |
| `set` | なし | 不可 | 可 | 一意性の保証 |

### 自分のコードでの実例

`rule-scribe-games` の `_ALLOWED_FIELDS` は**セット**:

```python
_ALLOWED_FIELDS = {"id", "slug", "title", "title_ja", ...}
```

なぜ `set` か？ → `if k in _ALLOWED_FIELDS` の検索が **O(1)**（定数時間）だから。
リストだと **O(n)**（要素数に比例）になる。

## シリアライゼーション（データの保存と通信）

プログラム内のデータ構造を、保存・通信可能な形式に変換すること。

### JSON

最も一般的。人間が読める。

```json
{
  "title": "カタン",
  "players": {"min": 3, "max": 4},
  "tags": ["strategy", "negotiation"]
}
```

自分のプロジェクトでの使用:

- `rule-scribe-games/models.json` — ゲームデータの永続化
- Supabase API のレスポンス
- Gemini API のリクエスト/レスポンス

### YAML

設定ファイルに最適。インデントで構造を表す。

```yaml
app_name: "RuleScribe Games"
version: "0.1.0"
gemini_model: "models/gemini-3-flash-preview"
```

自分のプロジェクトでの使用:

- `config.yaml` — アプリケーション設定
- `mkdocs.yml` — ドキュメントサイト設定
- `Taskfile.yml` — タスクランナー定義

### JSON vs YAML

| 特性 | JSON | YAML |
|------|------|------|
| 構文 | `{}` と `[]` | インデント |
| コメント | 不可 | `#` で可能 |
| 主な用途 | API通信、データ保存 | 設定ファイル |
| 人間の可読性 | 普通 | 高い |

## 演習

### 問1: データ型を当てよ

以下の各値の Python 型は？

```
42          → ?
"hello"     → ?
3.14        → ?
True        → ?
[1, 2, 3]   → ?
{"a": 1}    → ?
None        → ?
(1, "two")  → ?
```

??? note "解答"
    `int`, `str`, `float`, `bool`, `list[int]`, `dict[str, int]`, `None`, `tuple[int, str]`

### 問2: なぜ set を使うか

以下の2つのコードの計算量の違いを説明せよ。

```python
allowed_list = ["id", "slug", "title", "summary"]
allowed_set = {"id", "slug", "title", "summary"}

"title" in allowed_list
"title" in allowed_set
```

??? note "解答"
    - `list`: 先頭から順に検索 → **O(n)**
    - `set`: ハッシュテーブルで直接参照 → **O(1)**
    - 要素数が増えるほどsetの優位性が増す

## チェックリスト

- [ ] 1 byte が何 bit か即答できる
- [ ] UTF-8 で日本語1文字が何バイトか知っている
- [ ] `list`, `dict`, `set`, `tuple` の使い分けを説明できる
- [ ] JSON と YAML の違いを3つ挙げられる
- [ ] 計算量 O(1) と O(n) の意味を説明できる
