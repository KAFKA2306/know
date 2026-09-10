# California AV報告制度の研究判断（2026-09-10）

## Decision

Californiaの自動運転事業者を比較するとき、2025年までのdisengagement seriesを、2026年8月26日からoperativeになった新しいreporting metricsへ連結しない。

2026年9月10日時点では、新制度はoperativeだが主要な初回提出期限前である。新制度の実提出データが公開されるまでは、企業間の新しい安全・運行比較を作らず `UNVERIFIED` とする。

## Observation

KAFKA2306/autonomous-vehicles current mainは、California DMVの制度境界を次のように保持している。

- 規則発効: 2026-04-28
- 新しいtesting reporting requirementsのoperative date: 2026-08-26
- drivered testing: Dynamic Driving Task Performance Relevant System Failures、Vehicle Miles Traveledなどを月次報告
- driverless testing: Vehicle Immobilizations、Vehicle Miles Traveledなどを月次報告
- deployment: Vehicle Immobilizations、Dynamic Driving Task Performance Relevant System Failures、Vehicle Miles Traveledを四半期報告
- deploymentの最初の四半期報告期限: 2026-09-30
- 旧disengagement metricと新metricは同じseriesとして接続しない

参照revision: `68c0aa2c5ba92a36fd6331fa2b217412de5e339e`

## Primary evidence

- California DMV, Autonomous Vehicles Program Permit Resources: https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/autonomous-vehicles-program-permit-resources/
- California DMV, adopted autonomous vehicle regulations: https://www.dmv.ca.gov/portal/news-and-media/new-autonomous-vehicle-regulations-strengthen-oversight-and-enforcement-authorize-trucks-and-transit/
- California DMV, adopted regulatory text: https://www.dmv.ca.gov/portal/file/adopted-regulatory-text-article-3-8-2025-0415-04-pdf/
- Canonical consumer source: https://github.com/KAFKA2306/autonomous-vehicles/blob/main/data/california-dmv-testing.json

DMVは従来のdisengagement reportsについて、各permit holderのoperational activityを見るための情報であり、企業間比較用には設計されていないと明記している。またdeployment permitのoperationは従来のdisengagement reporting対象外だった。

## USE / CONDITION / REJECT

USE:
新制度下の実提出CSVがCalifornia DMVから公開され、同じreporting period・permit type・metric definitionで比較できる場合。

CONDITION:
metric definition、permit type、period、reporting regimeを揃える。値が0なのか未提出・未公開なのかを区別する。

REJECT:
旧disengagement countやmiles-per-disengagementを、新制度のsystem failure・vehicle immobilizationと同じseriesとして時系列接続すること。report countだけでcompany safety rankingを作ること。未公開の新制度値を0として扱うこと。

## Re-check trigger

California DMVが2026年8月26日以降を対象にした新しいmonthly / quarterly reporting dataを公開した時点で再評価する。特にdeploymentの2026年9月30日提出期限通過後は、公開データの有無とschemaを確認する。
