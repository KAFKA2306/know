# Pinecone

フルマネージドなベクトルデータベース。

## 本質

インフラ管理不要で、API経由で即座に利用可能なベクトル検索サービス。

## 基本

- **フルマネージド**: サーバー管理が一切不要
- **スケーラビリティ**: 数十億規模のベクトルに対応
- **低遅延**: 高速な検索レスポンス

## 使い方

```bash
pip install pinecone-client
```

```python
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")

# インデックスへの接続
index = pc.Index("my-index")

# データ挿入 (ID, Vector)
index.upsert(
    vectors=[("id-1", [0.1, 0.2, 0.3])]
)

# 検索
results = index.query(
    vector=[0.1, 0.2, 0.3],
    top_k=1
)
print(results)
```

## 参照

- [公式ドキュメント](https://docs.pinecone.io/home)
