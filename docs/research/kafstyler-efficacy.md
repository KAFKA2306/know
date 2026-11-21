---
title: Kafstylerの効果とGitHub Pages実証
description: 改善したと主張する前に、実利用で比較して判定する研究判断。
tags:
  - agent
  - github
  - evaluation
  - evidence
type: knowledge
---

# Kafstylerの効果とGitHub Pages実証

**整理日：2026年11月21日。状態：比較実験は未完了。** リポジトリの整備、CI成功、Issue整理と、訪問者が目的を達成できたことは別の結果である。

## 問いと判断

**問い：** Kafstylerを使うと、同じ課題と実行予算で、使える成果が増えるか。

**現時点の判断：** 運用ルールと個別の完了記録は存在するが、統制した比較実験の効果量は未確認。したがって「Kafstylerで改善した」と一般化しない。

## 実際の利用経路

1. そのサイトのMISSION・README・既存Issueから、利用者の達成したい一件を決める。
2. 公開URLを開き、最初の操作から完了までをブラウザで試す。
3. 失敗を再現し、同じ条件で直す。前回修正済みの問題は繰り返さない。
4. コードと必要最低限の検査を行い、GitHub上の正本へ反映する。
5. 公開デプロイを確認し、**修正後の本番URLで同じ操作を再実行**する。
6. 操作が成功した証拠、対象SHA、残った失敗を台帳へ記録する。

ブラウザ接続が失敗したら、その層は**未検証**とする。「公開した」と「操作できた」は別の状態で管理する。

## 比較実験の条件

| 揃えるもの | 方法 |
| --- | --- |
| 比較群 | Kafstylerあり・なしを、近い難度の実案件へ無作為に割り当てる |
| 実行予算 | 同じ基盤モデル、同じ制限時間・トークン予算、同じ権限 |
| 成果判定 | 正解を知らない第三者または決定論的検査で、本番の操作完了を判定する |
| 主要指標 | 操作完了率、重大な不具合、手戻り、実行時間 |
| 失敗の扱い | デプロイ不成立・ブラウザ接続失敗・調査だけで終わった案件を成功に数えない |

単一案件の「実装できた」は比較結果ではない。差が出ても、モデル性能、作業量、タスク難度などの別の説明を検討する。

## 正本と一次資料

- [Kafstyler 作業規約](https://github.com/KAFKA2306/kafstyler/blob/main/AGENTS.md)：目的、台帳、検証、完了条件の現行正本。
- [Kafstyler ミッション](https://github.com/KAFKA2306/kafstyler/blob/main/MISSION.md)：知見を次の成果に使うための要件。
- [Know の前回公開検証 #22](https://github.com/KAFKA2306/know/issues/22)：検索、記事表示、画面幅を検証した既存の記録。
- [今回の更新台帳 #23](https://github.com/KAFKA2306/know/issues/23)：最新版の関心テーマをサイトで使える入口へ変更する。
- [GitHub Pages 公式の公開元設定](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)：公開結果の検証先。

## 再確認条件

異なるリポジトリで、同一条件の対照実験と本番操作の両方が記録されたら効果を再判定する。実行記録が欠ける場合、原因と再開条件まで残す。

関連：[根拠の記録・検証の導入](../services/evidence-contract-integration.md) · [製造品質検査の判断](../dev/deepdive/manufacturing-quality-inspection.md)
