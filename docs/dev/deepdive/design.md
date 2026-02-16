# デザイントークン & UI エンジニアリング

「見た目の美しさ」を設計可能・再利用可能にする技術。

## デザイントークンとは

デザインの「変数」。色やフォントを一箇所で定義し、全体で使い回す。

```
デザイントークン = デザインの設定ファイル
```

### なぜ必要か

| アプローチ | 問題 |
|-----------|------|
| 色を直書き `color: #005CB9` | 変更時に全ファイルを探して置換 |
| 変数化 `color: var(--color-primary)` | 1箇所変えれば全体に反映 |

## CSS Variables（カスタムプロパティ）

### 定義と使用

```css
:root {
  --color-primary: 210, 100%, 36%;
  --color-accent: 184, 100%, 34%;
  --bg-dark: #0b1221;
  --text-main: #eef2ff;
  --font-main: 'Zen Maru Gothic', sans-serif;
}

body {
  background-color: var(--bg-dark);
  color: var(--text-main);
  font-family: var(--font-main);
}
```

`:root` = HTML 文書全体のルート。ここに定義した変数はどこからでも参照可能。

### HSL カラーモデル

自分のプロジェクトでは **HSL** で色を定義する:

```
HSL = Hue（色相）, Saturation（彩度）, Lightness（明度）
```

| 成分 | 範囲 | 意味 |
|------|------|------|
| H (色相) | 0°〜360° | 色の種類（0=赤, 120=緑, 240=青） |
| S (彩度) | 0%〜100% | 鮮やかさ（0=灰色, 100=純色） |
| L (明度) | 0%〜100% | 明るさ（0=黒, 50=純色, 100=白） |

```css
--color-primary: 210, 100%, 36%;  /* Digital Blue */
--color-accent: 184, 100%, 34%;   /* Serendie Teal */
```

!!! tip "なぜ HSL か"
    **RGB**: `#005CB9` → 何色か直感的にわからない
    **HSL**: `210, 100%, 36%` → 「色相210°（青系）で鮮やかで暗め」と読める
    明度だけ変えてホバー効果を作れる: `hsl(210, 100%, 42%)` → やや明るい青

## DESIGN_SYSTEM.md のトークン体系

| トークン | 値 | 用途 |
|---------|-----|------|
| `--color-primary` | Digital Blue | 信頼感、ナビゲーション |
| `--color-accent` | Serendie Teal | インタラクション、強調 |
| `--color-background` | Deep Space | ダークモード背景 |
| `--color-text` | White | 本文テキスト |

### 実装ルール

1. **ハードコード禁止**: `color: #005CB9` ではなく `color: hsl(var(--color-primary))`
2. **Vanilla First**: フレームワーク（Tailwind等）より CSS Variables を優先
3. **セマンティック HTML**: `<div>` 乱用禁止。`<nav>`, `<main>`, `<article>` を使う

## RuleScribe のスタイリング解剖

### レイアウト: CSS Grid

```css
@media (min-width: 768px) {
  .main-layout {
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 24px;
  }
}
```

**モバイルファースト**: デフォルトは縦積み（`flex-direction: column`）。768px 以上で2カラム。

### インタラクション: トランジション

```css
.game-card {
  transition: all 0.2s;
}

.game-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.1);
}
```

`0.2s` = 200ミリ秒。人間が「なめらか」と感じる最小時間。

### グラスモーフィズム

```css
.game-detail-pane {
  background: var(--bg-card);           /* 半透明の背景 */
  backdrop-filter: blur(10px);          /* 背景をぼかす */
  border: 1px solid var(--border);      /* 微かな境界線 */
  border-radius: 16px;                  /* 角丸 */
}
```

これにより「ガラスのような」プレミアムな見た目になる。

## 演習

### 問1: HSL を読め

`hsl(184, 100%, 34%)` は何色か？

??? note "解答"
    - H=184°: 青と緑の中間（シアン/ティール系）
    - S=100%: 最大に鮮やか
    - L=34%: やや暗い
    → **Serendie Teal**（ダークティール）

### 問2: なぜ Vanilla CSS か

Tailwind CSS ではなく CSS Variables を使う理由を3つ挙げよ。

??? note "解答"
    1. **依存なし**: ビルドツール不要でブラウザが直接解釈
    2. **ランタイム変更**: JavaScript で `setProperty` すればテーマを動的に切替可能
    3. **学習価値**: CSS の基礎を理解でき、どのフレームワークにも応用できる

## チェックリスト

- [ ] CSS Variables の定義と使用方法を書ける
- [ ] HSL カラーモデルの3成分を説明できる
- [ ] モバイルファーストの意味と実装方法を理解している
- [ ] `transition` と `transform` の違いを説明できる
