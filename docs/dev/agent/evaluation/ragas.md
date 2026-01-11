# RAGAS

RAGパイプラインの評価フレームワーク。

## 本質

Retrieval Augmented Generation (RAG) パイプラインの性能を、グラウンドトゥルース（正解データ）なしでも評価可能にする仕組み。

## 基本

- **メトリクス**: Faithfulness（忠実性）、Answer Relevancy（回答関連性）、Context Precision（文脈精度）などを算出
- **自動生成**: 評価用データセットの生成機能
- **適応**: RAG特有の課題に特化

## 使い方

```bash
pip install ragas
```

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

# 評価データ準備 ({question, answer, contexts, ground_truth})
data = {
    "question": ["When was the company formed?"],
    "answer": ["The company was formed in 2020."],
    "contexts": [["The company was founded in 2020 by..."]],
    "ground_truth": ["2020"]
}
dataset = Dataset.from_dict(data)

# 評価実行
results = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
)
print(results)
```

## 参照

- [公式ドキュメント](https://docs.ragas.io/)
