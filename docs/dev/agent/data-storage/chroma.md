# Chroma

オープンソースのAIネイティブ埋め込みデータベース。

## 本質

開発者体験（DX）を重視した、軽量で使いやすいベクトルストア。特にPoCやローカル開発に適する。

## 基本

- **シンプル**: セットアップが非常に簡単（`pip install chromadb`）
- **機能**: 埋め込み、保存、クエリ機能がオールインワン
- **統合**: LangChainやLlamaIndexとの親和性が高い

## 使い方

```bash
pip install chromadb
```

```python
import chromadb

# ローカルクライアント作成
client = chromadb.Client()

# コレクション取得（なければ作成）
collection = client.get_or_create_collection("my_collection")

# データ追加（埋め込みは自動計算される）
collection.add(
    documents=["This is a document", "This is another document"],
    ids=["id1", "id2"]
)

# 検索
results = collection.query(
    query_texts=["This is a query document"],
    n_results=1
)
print(results)
```

## 参照

- [公式ドキュメント](https://docs.trychroma.com/)
