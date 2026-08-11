# Evidence Contract Integration Pack

AI / Agentが生成する調査・データ更新・レポートについて、**何を観測し、何を主張し、どのtestとevidenceを通してdecisionにしたか**をrepository内で追跡するための導入パックです。

## 無料starter

公開starterには次を含みます。

- `Observation / Claim / Test / Evidence / Decision` を分離する最小schema
- provenance欠落や未検証evidenceによる`PASS`を拒否するvalidator
- positive / fail-closed fixture
- 導入先へコピーできるGitHub Actions workflow
- 最小`ontology/project.yaml`

[templateを見る](https://github.com/KAFKA2306/know/tree/main/templates/evidence-contract-starter)

## 有償PoCの想定範囲

最初のPoCは **1 repository / 1 use case / 2週間** を想定します。開始前に対象repository、use case、private-data境界、acceptance criteriaを合意し、次を対象とします。

1. 現行のclaim / evidence / testフローのmapping
2. 必要最小schemaへの落とし込み
3. CI gate導入
4. 公開可能または顧客環境内だけで扱うsample migration
5. review session

価格・実績・工数削減率は、合意済み見積や実測がない段階では保証値として表示しません。

[自分のrepoへ適用する](https://github.com/KAFKA2306/know/issues/new?title=Evidence%20Contract%20Integration%20Pack%20%E7%9B%B8%E8%AB%87)

## 顧客側で準備するもの

- 対象repositoryと対象use case
- どの出力を採用判断したいか
- 利用可能な一次情報・内部情報の境界
- CIで失敗させる条件
- private source / credential / business dataをpublic repositoryへ出さない運用境界

## 保証しないこと

このstarterやPoC単体では、次を保証しません。

- 規制・法令・外部監査基準への準拠
- LLM hallucinationの防止
- source自体の真偽
- decisionの業務上・法務上の妥当性
- セキュリティレビュー完了

CIが示すのは、**宣言したcontractに対して機械検査が通ったか**という範囲です。最終判断が必要な領域では人間レビューを残します。

## Data boundary

public `know` repositoryへ顧客のprivate source、prompt、credential、個人情報、business dataを保存しません。公開fixtureはsynthetic / public sourceだけを対象にします。

## Funnelの記録

実際に観測したものだけを次の別状態で記録します。

- `starter_opened`
- `template_copied`
- `integration_inquiry_started`
- `qualified_inquiry`
- `mapping_session_completed`
- `paid_pilot`
- `multi_repo_expansion_requested`

未観測イベントを実績として補完しません。初期台帳はすべて0・evidenceなしです。
