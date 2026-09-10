# 製造品質検査の研究判断

## Decision

製造品質の自動化を比較するとき、単に「AIを導入したか」ではなく、検査対象、検査coverage、deployment state、同一作業・同一単位で比較できる実測時間を分けて確認する。

General Motors の Factory ZERO では、WeldBrAIn のpilotにより、body shopの品質確認が「1 shift あたり4 partsのmanual inspection」から「every single weld on every single bodyをreal timeで確認」へ拡張された。これはcoverageの変化であり、単純な倍率には変換しない。

GM Defiance Operations の3D Metra Scanでは、castingsのscan timeが60分/partから10分/partへ短縮された。同一対象・同一単位のBefore/Afterなので、50分/part、83.3%のscan-time reductionとして比較できる。

GM Bedford Casting Plant のCT scanningでは、鋳造品内部のporosity等を非破壊で調べるquality checkについて、GMが50〜70% fasterと報告している。Bedfordは2019年からCTを使用し、current source時点でscannerを最大18時間/日運用して自拠点と他GM casting facilitiesの部品を検査している。

したがって、表面・寸法形状を高速に測るDefianceのMetra Scanと、鋳造品内部を三次元で調べるBedfordのCTを「83.3% vs 50〜70%」だけで優劣比較しない。改善率の対象jobとbaselineが異なる。技術選定では、まず検査対象が表面寸法か内部欠陥かを決め、その後に同一job内のtime、accuracy、rework、scrap、labor、ROIを比較する。

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

GM Bedford / CT scanning:

- official source publisher: General Motors
- official source published_at: `2025-07-15`
- physical site: GM Bedford Casting Plant, Indiana
- process: non-destructive volumetric inspection of castings
- use since: `2019`
- reported quality-check speed improvement: `50-70% faster`
- scanner utilization: `up to 18 hours/day`
- inspected defects include porosity such as air bubbles and shrink holes
- Bedford also scans parts for other GM casting facilities

DefianceとBedfordの値はGM一次情報から直接取得した研究判断用evidenceであり、この時点ではFactoryDB canonical recordとして複製しない。

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

General Motors, "How GM uses CT scanning to boost vehicle manufacturing quality"

https://news.gm.com/home.detail.html/Pages/topic/us/en/2025/jul/0715-GM-CT-scanning-vehicle-manufacturing-quality.html

GMの一次情報では、Bedford Casting PlantのCT scanningについて次を確認できる。

- Bedfordは2019年からCTを鋳造品のdefect検出に使用
- CTは鋳造品を破壊せず三次元画像化し、porosityなど内部欠陥候補を確認する
- quality checksを50〜70% fasterにできるとGMが報告
- scannerを最大18時間/日運用
- Bedford自身だけでなく他GM casting facilitiesの部品もscanしている
- sourceはquality向上とwaste reductionへの寄与を述べるが、defect reduction量、waste削減量、labor cost、ROIの数値は示していない

FactoryDB source registry:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/robotics-sources.json

FactoryDB canonical robotics ledger:

https://github.com/KAFKA2306/factory/blob/968ae84ec033438943f7f97766992f4649bd066c/data/automation.jsonl

確認日: 2026-09-10

## USE / CONDITION / REJECT

USE:

- 抜取検査からinline全数監視へ移る技術のcoverage比較
- castingsのsurface/dimensional inspectionで同一単位 `min/part` の時間比較を行う研究
- castingsのinternal/volumetric inspectionでCTによるquality-check時間改善を評価する研究
- surface geometryとinternal defect inspectionをjob別に分けた工程設計

CONDITION:

- `4 parts per shift` と `every weld / every body` はcoverageの差であり、同一単位の単純な倍率へ変換しない
- `60 min/part -> 10 min/part` は同一単位なので50 min/part、83.3% reductionとして扱える
- Bedfordの`50-70% faster`はGMがquality checks全体について報告したrangeのまま保持し、単一値へ丸めない
- `up to 4 hours -> 5 minutes` のbeforeは上限表現なので、常に235分短縮したとは扱わない
- `several hours -> 15 minutes` はbeforeが数量化されていないため削減率を計算しない
- `up to 18 hours/day` はscanner utilizationの上限表現であり、毎日18時間稼働したとは扱わない
- pilot evidenceを全工場展開や量産標準化の証拠へ拡張しない
- defect rate、false positive、false negative、labor-hours、rework削減量、scrap削減量、ROIは現在のsourceだけではUNVERIFIED

REJECT:

- 「AI導入済み」という二値だけで品質技術を比較する
- Defianceの83.3%とBedfordの50〜70%を異なる検査jobのまま単純ランキングする
- pilotをproduction-wide deploymentとして扱う
- every weldを「不良ゼロ」や「100%検出」と読み替える
- `up to 4 hours` を固定240分のbaselineとして平均削減時間を計算する
- `up to 18 hours/day` を実測daily throughputへ変換する
- sourceにない人員削減、cost saving、ROIを推定する

## Re-check triggers

次の場合はFactoryDBとGM一次情報を再確認する。

- WeldBrAInがpilotからproduction deploymentへstatus transitionしたとき
- DefianceのMetra Scanについてthroughput、labor-hours、accuracy、rework、scrap、ROIなど追加の実測値が公開されたとき
- BedfordのCTについてparts/day、accuracy、defect/rework/scrap削減量、labor、ROIなど同一単位の追加実測値が公開されたとき
- FactoryDBにDefiance / Metra ScanまたはBedford / CTのcanonical identityが追加され、同じevidenceを構造化して再利用できるようになったとき
- 他社で同じ検査job・同じ単位のevidenceが得られ、operator間比較が可能になったとき

このページはFactoryDBの事実を複製する正本ではない。FactoryDBに存在する事実のauthorityはFactoryDBへ残し、DefianceとBedfordの追加evidenceはGM一次情報へ戻れる形で保持する。このページは研究判断、比較可能なmetric、利用境界だけを保持する。
