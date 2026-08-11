# Evidence Contract Starter

`know` の Evidence Contract を既存リポジトリへ最小構成で導入するための配布用 starter です。

この starter は、`Observation / Claim / Test / Evidence / Decision` を機械的に分離し、根拠が欠けた判断を `PASS` にしないための最小 validator を提供します。規制準拠、監査対応済み、hallucination 防止を保証するものではありません。

## コピーするもの

導入先リポジトリで次の配置を推奨します。

```text
.github/workflows/evidence-contract.yml
evidence-contract/
  contract.schema.json
  validate_contract.py
  examples/
    valid.json
    missing-evidence.json
  ontology/
    project.yaml
```

1. このディレクトリの `contract.schema.json`、`validate_contract.py`、`examples/`、`ontology/` を導入先の `evidence-contract/` へコピーします。
2. `.github/workflows/evidence-contract.yml` を導入先リポジトリの同じパスへコピーします。
3. `evidence-contract/ontology/project.yaml` を対象リポジトリに合わせて編集します。
4. `examples/valid.json` を実ユースケースの最小fixtureへ置き換えます。private source、credential、prompt、顧客データをpublic repositoryへ追加しないでください。
5. pull requestを作成し、Evidence Contract workflowが成功することを確認します。

## ローカル確認

```bash
python -m unittest evidence-contract/test_validator.py
python evidence-contract/validate_contract.py evidence-contract/examples/valid.json
```

`missing-evidence.json` は失敗することが正しい挙動です。

```bash
python evidence-contract/validate_contract.py evidence-contract/examples/missing-evidence.json
# non-zero exit expected
```

## 判定境界

- provenanceが無いObservationを正常な根拠として扱わない。
- decisionが参照するEvidence IDが存在しなければ失敗する。
- `PASS` decisionが未検証Evidenceだけに依存していれば失敗する。
- 外部標準や法令への適合性は、このstarterの成功だけでは証明しない。
- 顧客固有のprivate source、credential、business dataはこのpublic starterへ保存しない。

## 無料starterと有償PoC

このstarter自体は公開sampleです。有償PoCの範囲は、対象repository 1つ・use case 1つについて、既存workflowを壊さない範囲でschema mapping、CI gate導入、sample migration、レビューを行うことです。実施前に対象repository、private-data境界、受け入れ条件を個別に確定します。

詳細: https://kafka2306.github.io/know/services/evidence-contract-integration/
