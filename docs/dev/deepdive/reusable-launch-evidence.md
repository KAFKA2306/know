# 再使用ロケットの研究判断

## Decision

再使用能力を比較するとき、打上げ回数を再使用回数の代理指標にしない。再使用成熟度の判断には、同じvehicle / stageについて一次情報で明示されたreflight、recovery、landing、lossを使い、planned missionやauthorizationとcompleted/reuse eventを分離する。

## Observation

参照する正本は `KAFKA2306/space_launches` main `2eaca85cf4980700f5247c2b85b4745bc467bc68`。

2026-09-09T22:35:54Z時点のcanonical indexは、2024-01-02以降のcompleted launch 478件、reuse event 11件を保持する。operator別completed launchはSpaceX 414、Rocket Lab 47、Blue Origin 17。これらのlaunch countからreuse countを推定しない。

明示されたreuse evidenceの例:

- SpaceX Falcon 9 / Starlink 6-59: first stageの21回目のflightをoperator primary mission dataで確認。
- Rocket Lab Electron / Four Of A Kind: 2024-01-31 missionでfirst stageのsuccessful ocean splashdown and recoveryをRocket Lab公式mission情報で確認。
- Blue Origin New Glenn: NG-1のbooster loss、NG-2のlanding、同boosterのNG-3 reflightを別eventとして保持。ただしBlue Origin primary pagesはGitHub-hosted runnerからHTTP 429となるため、current repositoryではreviewed_primary_urlとしてlive-fetched evidenceと分離する。

## Evidence

- Canonical index: https://github.com/KAFKA2306/space_launches/blob/2eaca85cf4980700f5247c2b85b4745bc467bc68/api/v1/space-launches/index.json
- Canonical reuse events: https://github.com/KAFKA2306/space_launches/blob/2eaca85cf4980700f5247c2b85b4745bc467bc68/api/v1/space-launches/reuse-events.json
- Rocket Lab, Four Of A Kind: https://rocketlabcorp.com/missions/launches/four-of-a-kind/
- Rocket Lab mission release: https://rocketlabcorp.com/updates/rocket-lab-successfully-launches-first-electron-mission-of-busy-2024-launch-schedule/

## USE / CONDITION / REJECT

USE:

- vehicle / stage identityが一致し、operatorまたはregulatorの一次情報がreflight / recovery / landing / lossを明示している場合。
- completed missionのcadenceとreuse eventを別metricとして比較する場合。

CONDITION:

- `live_fetched_primary` と `reviewed_primary_url` を同じ取得状態として扱わない。
- turnaround daysを比較するときは同じvehicle identityと連続するevidenced eventsに限定する。

REJECT:

- launch countからbooster reuse countを推定する。
- planned missionやFAA authorizationをcompleted missionとして数える。
- recovery attemptをsuccessful recoveryとして扱う。
- Blue Originのreviewed evidenceをlive-fetched evidenceと表示する。

## Re-check trigger

新しいbooster reflight / landing / lossが一次情報で確認された場合、またはoperator間で比較可能な同一定義のturnaround evidenceが増えた場合に再評価する。
