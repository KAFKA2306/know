# 米国電力供給をどう調べるか

## 判断

米国の電力供給制約を調べるとき、原子力・再エネ・天然ガスのどれか一つだけを代表変数にしない。

直近の全米48州の実発電構成では天然ガスが最大で、石炭と原子力もそれぞれ大きな比率を持つ。したがって、短中期の供給余力を判断するときは、少なくとも次を別々に確認する。

- 天然ガス火力の実発電と供給制約
- 原子力の既設容量・稼働と新設計画
- 風力・太陽光・水力の実発電
- 送電・連系・蓄電など、発電容量を需要地点へ届ける制約

この判断は「どの電源へ投資すべきか」や「AIデータセンターが需要増の原因か」を示すものではない。現在の電源構成だけから、原因・価格・地域別混雑・追加容量の実現時期は推定しない。

## 観測

確認日: 2026-09-10

正本: [KAFKA2306/Electricity](https://github.com/KAFKA2306/Electricity)

参照revision: `48684713c5687785da565852f005e1ef08b77aec`

### 実発電

`api/v1/electricity/generation-mix.json` の2026-09-07 UTC完結日では、US48の発電構成は次のとおり。

| 電源 | 発電量 | 構成比 |
| --- | ---: | ---: |
| 天然ガス | 5,161,819 MWh | 41.215% |
| 原子力 | 2,252,571 MWh | 17.986% |
| 石炭 | 2,252,157 MWh | 17.983% |
| 太陽光 | 1,071,734 MWh | 8.557% |
| 風力 | 1,144,241 MWh | 正本参照 |
| 水力 | 469,669 MWh | 正本参照 |

同日のUS48 net generationは12,545,871.62 MWh。日次値は24時間すべて揃ったUTC日の実観測だけを使う。

### 需要と設備容量

`api/v1/electricity/metrics.json` では、US48 electricity demandの最新完結日は2026-09-08で13,586,202.381 MWh。発電構成の最新完結日とは1日ずれるため、両者を同日収支として比較しない。

EIA-860Mの2026年7月inventoryでは、operating net summer capacityは1,316,203.6 MW、planned net summer capacityは283,538.0 MW。plannedはoperatingと分離し、現在利用可能な容量として加算しない。

## Evidence

- Electricity canonical metrics: https://github.com/KAFKA2306/Electricity/blob/main/api/v1/electricity/metrics.json
- Electricity canonical generation mix: https://github.com/KAFKA2306/Electricity/blob/main/api/v1/electricity/generation-mix.json
- EIA Open Data: https://www.eia.gov/opendata/
- EIA Preliminary Monthly Electric Generator Inventory (EIA-860M): https://www.eia.gov/electricity/data/eia860m/

EIAのBalancing Authority hourly operating dataはactual/forecast demand、net generation、系統間flowを提供する。EIA-860Mは既設・計画generatorを月次で追跡するpreliminary inventoryで、後続月に訂正される可能性がある。

## 再確認条件

次の判断をするときは、このページの数値をそのまま再利用せず、Electricity正本を再取得する。

- 特定地域のデータセンター・工場向け電源余力を判断する
- 系統混雑、interconnection queue、電力価格を判断する
- 新設発電所がいつ実供給へ入るか判断する
- 電源別の将来シェアや限界電源を判断する

このページの役割は、Electricityの正本を複製することではなく、「米国電力供給を一電源だけで代表させない」という研究判断と、その根拠を再利用可能にすること。