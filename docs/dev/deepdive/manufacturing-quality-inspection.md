# 製造品質検査の研究判断

## Decision

製造品質の自動化を比較するとき、単に「AIを導入したか」ではなく、**検査対象のcoverage**と、同一作業・同一単位で比較できる**実測時間**を分けて確認する。

General Motors の Factory ZERO では、WeldBrAIn のpilotにより、body shopの品質確認が「1 shift あたり4 partsのmanual inspection」から「every single weld on every single bodyをreal timeで確認」へ拡張されたとGMが報告している。これはcoverageの変化であり、単純な倍率には変換しない。

一方、GM Defiance Operations の3D Metra Scanでは、castingsのscan timeが60分/partから10分/partへ短縮された。同一対象・同一単位のBefore/Afterなので、50分/part、83.3%のscan-time reductionとして比較できる。setup/programmingは「最大4時間」から5分なので、上限を含む表現のまま保持し、常に235分短縮したとは扱わない。

したがって、製造品質技術を評価するときは、coverage、deployment state、同一単位のcycle/inspection time、accuracy、rework、scrap、labor、ROIを別metricとして扱う。

## Observation

Factory ZERO / WeldBrAIn:

- source repository: `KAFKA2306/factory`
- source revision: `968ae84ec033438943f7f97766992f4649bd066c`
- FactoryDB record: `facility:gm-factory-zero`
- equipment type: `automated_weld_inspection`
- status: `installed`
- deployment stage: `pilot`
- observed at: `2026-05-05`
- source id: `gm-smart-tools-2026`

FactoryDBは、この技術をproduction-wide deploymentではなくpilotとして保持している。statusを`operational`へ推測昇格しない。

GM Defiance / 3D Metra Scan:

- official source publisher: General Motors
- official source published_at: `2026-05-11`
- physical site: GM Defiance Operations, Ohio
- process: dimensional inspection of castings / tooling
- measured casting scan time: `60 min/part -> 10 min/part`
- measured reduction: `50 min/part` / `83.3%`
- setup/programming: `up to 240 min -> 5 min`
- tooling scan: `several hours -> 15 min`

Defianceの値はGM一次情報から直接取得した研究判断用evidenceであり、この時点ではFactoryDB canonical recordとして複製しない。

## Primary evidence

General Motors, "How smarter AI tools help build better vehicles"

https://news.gm.com/home.detail.html/Pages/topic/us/en/2026/may/0505-smarterAItoolsbuildvehicles.html

GMの一次情報では、Factory ZEROのWeldBrAInについて次を確認できる。

- 従来のquality checkpointはmanual inspectionで、1 shiftあたり4 partsを確認していた
- WeldBrAInはevery single weld on every single bodyをreal timeで確認する
- 技術はFactory ZEROでpilot中と記載されている

General Motors, "This smart 3D scanner spots problems before they leave the shop"

https://news.gm.com/home.detail.html/Pages/topic/us/en/2026/may/0511-smart-3d-scanner.html

GMの一次情報では、Defiance Operationsの3D Metra Scanについて次を確認できる。

- castingsのscan timeは60分/partから10分/partへ短縮
- setup/programmingは最大4時間から5分へ短縮
- tooling scanは従来数時間から15分へ短縮
- scannerはDefianceで数年前から利用され、Saginaw、Brownstown Battery、Factory ZEROにも展開されている
- sourceはrework低減への寄与を述べるが、rework削減量やROIの数値は示していない

FactoryDB source registry:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/robotics-sources.json

FactoryDB canonical robotics ledger:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/automation.jsonl

確認日: 2026-09-10

## USE / CONDITION / REJECT

USE:

- 抜取検査からinline全数監視へ移る技術のcoverage比較
- quality inspection automationのcoverageを評価する研究
- castingsのscan timeを同一単位 `min/part` で比較する研究
- manual sample count、automated observation coverage、inspection timeを分離した工程設計

CONDITION:

- `4 parts per shift` と `every weld / every body` はcoverageの差であり、同一単位の単純な倍率へ変換しない
- `60 min/part -> 10 min/part` は同一単位なので50 min/part、83.3% reductionとして扱える
- `up to 4 hours -> 5 minutes` のbeforeは上限表現なので、常に235分短縮したとは扱わない
- `several hours -> 15 minutes` はbeforeが数量化されていないため削減率を計算しない
- pilot evidenceを全工場展開や量産標準化の証拠へ拡張しない
- defect rate、false positive、false negative、labor-hours、rework削減量、ROIは現在のsourceだけではUNVERIFIED

REJECT:

- 「AI導入済み」という二値だけで品質技術を比較する
- pilotをproduction-wide deploymentとして扱う
- every weldを「不良ゼロ」や「100%検出」と読み替える
- `up to 4 hours` を固定240分のbaselineとして平均削減時間を計算する
- sourceにない人員削減、cost saving、ROIを推定する

## Re-check triggers

次の場合はFactoryDBとGM一次情報を再確認する。

- WeldBrAInがpilotからproduction deploymentへstatus transitionしたとき
- DefianceのMetra Scanについてthroughput、labor-hours、accuracy、rework、scrap、ROIなど追加の実測値が公開されたとき
- FactoryDBにDefiance / Metra Scanのcanonical identityが追加され、同じevidenceを構造化して再利用できるようになったとき
- 他社で同じ単位のinspection coverageまたはscan-time evidenceが得られ、比較可能になったとき

このページはFactoryDBの事実を複製する正本ではない。FactoryDBに存在する事実のauthorityはFactoryDBへ残し、Defianceの追加evidenceはGM一次情報へ戻れる形で保持する。このページは研究判断、比較可能なmetric、利用境界だけを保持する。
