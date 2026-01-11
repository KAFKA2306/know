# Weaviate

AIネイティブなオープンソースベクトルデータベース。

## 本質

オブジェクトとベクトルを共に保存し、ベクトル検索とキーワード検索を組み合わせたハイブリッド検索が可能なデータベース。

## 基本

- **モジュール式**: ベクトル化モジュールなどをプラグイン可能
- **ハイブリッド検索**: BM25等のキーワード検索とベクトル検索の融合
- **GraphQL**: データアクセスにGraphQLを使用

## 使い方

```bash
pip install weaviate-client
```

```python
import weaviate

# ローカルインスタンスに接続
client = weaviate.connect_to_local()

try:
    # コレクション作成
    questions = client.collections.create("Question")

    # データ追加
    questions.data.insert({"question": "What is Weaviate?"})

    # 検索
    response = questions.query.near_text(
        query="database",
        limit=1
    )
    print(response.objects[0].properties)
finally:
    client.close()
```

## 参照

- [公式ドキュメント](https://weaviate.io/developers/weaviate)
