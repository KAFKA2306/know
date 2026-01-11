# LlamaIndex

データフレームワーク。

## 本質

LLMとプライベートデータを接続するためのインターフェース。特にデータの取り込み、構造化、検索（RAG）に強みを持つ。

## 基本

- **Data Connectors**: 多様なソースからデータを取り込み
- **Indices**: データをLLMが利用しやすい形式（ベクトル、キーワード、グラフ等）に構造化
- **Query Engines**: 自然言語クエリに対して知識を検索・回答

## 使い方

```bash
pip install llama-index
```

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# データ読み込み
documents = SimpleDirectoryReader("./data").load_data()

# インデックス作成（自動でベクトル化・保存）
index = VectorStoreIndex.from_documents(documents)

# クエリエンジン作成
query_engine = index.as_query_engine()

# 質問
response = query_engine.query("What did the author do growing up?")
print(response)
```

## 参照

- [公式ドキュメント](https://docs.llamaindex.ai/en/stable/)
