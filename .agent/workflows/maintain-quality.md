---
description: リポジトリの品質を維持するための定期メンテナンスフロー
---

# 品質維持ワークフロー

// turbo-all

## 1. ビルド検証

```bash
task check
```

WARNING / ERROR が出た場合は必ず修正する。

## 2. 鮮度確認

`task check` が `grep -rn "2025" docs/` を含む。ヒットした場合:
- 情報が古い → `/update-content` で更新
- 過去の正確な記録 → そのまま

## 3. ナビゲーション整合性

`mkdocs.yml` の `nav:` に記載されたパスがすべて実在することを確認。

## 4. デプロイ

```bash
task git MESSAGE="chore: maintenance pass"
```

## 実行頻度

週次 または 大きな変更の前後。
