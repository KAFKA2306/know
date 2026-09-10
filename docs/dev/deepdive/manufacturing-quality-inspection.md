# 製造品質検査の研究判断

## Decision

製造品質の自動化を比較するとき、単に「AIを導入したか」ではなく、**検査対象のcoverageがどこまで広がったか**を優先して確認する。

General Motors の Factory ZERO では、WeldBrAIn のpilotにより、body shopの品質確認が「1 shift あたり4 partsのmanual inspection」から「every single weld on every single bodyをreal timeで確認」へ拡張されたとGMが報告している。

したがって、溶接品質の自動検査を評価するときは、従来の抜取検査と同じ検査件数として扱わず、coverage、検出単位、real-time性を分けて比較する。

## Observation

- source repository: `KAFKA2306/factory`
- source revision: `968ae84ec033438943f7f97766992f4649bd066c`
- FactoryDB record: `facility:gm-factory-zero`
- equipment type: `automated_weld_inspection`
- status: `installed`
- deployment stage: `pilot`
- observed at: `2026-05-05`
- source id: `gm-smart-tools-2026`

FactoryDBは、この技術をproduction-wide deploymentではなくpilotとして保持している。statusを`operational`へ推測昇格しない。

## Primary evidence

General Motors, "How smarter AI tools help build better vehicles"

https://news.gm.com/home.detail.html/Pages/topic/us/en/2026/may/0505-smarterAItoolsbuildvehicles.html

GMの一次情報では、Factory ZEROのWeldBrAInについて次を確認できる。

- 従来のquality checkpointはmanual inspectionで、1 shiftあたり4 partsを確認していた
- WeldBrAInはevery single weld on every single bodyをreal timeで確認する
- 技術はFactory ZEROでpilot中と記載されている

FactoryDB source registry:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/robotics-sources.json

FactoryDB canonical robotics ledger:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/automation.jsonl

確認日: 2026-09-10

## USE / CONDITION / REJECT

USE:

- 抜取検査からinline全数監視へ移る技術の比較
- quality inspection automationのcoverageを評価する研究
- manual sample countとautomated observation coverageを分離した工程設計

CONDITION:

- `4 parts per shift` と `every weld / every body` はcoverageの差であり、同一単位の単純な倍率へ変換しない
- pilot evidenceを全工場展開や量産標準化の証拠へ拡張しない
- defect rate、false positive、false negative、labor-hours、ROIはこのsourceだけではUNVERIFIED

REJECT:

- 「AI導入済み」という二値だけで品質技術を比較する
- pilotをproduction-wide deploymentとして扱う
- every weldを「不良ゼロ」や「100%検出」と読み替える
- sourceにない人員削減、cost saving、ROIを推定する

## Re-check triggers

次の場合はFactoryDBとGM一次情報を再確認する。

- WeldBrAInがpilotからproduction deploymentへstatus transitionしたとき
- defect detection accuracy、false-positive rate、labor time、rework、scrapなどの実測値が公開されたとき
- 他社で同じ単位のinspection coverage evidenceが得られ、比較可能になったとき

このページはFactoryDBの事実を複製する正本ではない。事実のauthorityはFactoryDBとGM一次情報に残し、このページは研究判断と利用境界だけを保持する。
