# Qdrant

高速ベクトル検索エンジン。

## 本質

Rust製の高速・スケーラブルなベクトル類似度検索エンジン。

## 基本

- **フィルタリング**: ペイロードベースの高度なフィルタリングが可能
- **分散型**: クラウドネイティブな分散アーキテクチャ
- **使いやすさ**: Python, Go, Rust等のクライアントライブラリが充実

## 使い方

```bash
pip install qdrant-client
```

```python
from qdrant_client import QdrantClient

# メモリ内モードで起動（PoC用）
client = QdrantClient(":memory:")

# コレクション作成
client.add(
    collection_name="my_collection",
    documents=["Qdrant is fast", "Vector search is cool"],
)

# 検索
hits = client.query(
    collection_name="my_collection",
    query_text="fast database",
)
print(hits[0].document)
```

## 参照

- [公式ドキュメント](https://qdrant.tech/documentation/)
