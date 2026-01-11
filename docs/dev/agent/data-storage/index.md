# Data Storage

ベクトルDBによるセマンティック検索。

## 比較

| DB | 特徴 | 推奨用途 |
|----|------|----------|
| Qdrant | Rust製高速、強力フィルタリング | プロダクション、高スループット |
| Pinecone | フルマネージド、自動スケーリング | エンタープライズ |
| Weaviate | ハイブリッド検索、GraphQL | ナレッジグラフ |
| Chroma | 軽量、Python-first | プロトタイプ、ローカル開発 |
| MongoDB | NoSQL + ベクトル検索 | 既存MongoDB環境 |

## Tools

1. **[Qdrant](qdrant.md)**: 高速ベクトル検索エンジン
2. **[Pinecone](pinecone.md)**: マネージドベクトルDB
3. **[Weaviate](weaviate.md)**: オープンソースベクトルDB
4. **[Chroma](chroma.md)**: 軽量エンベディングDB
5. **[MongoDB](mongodb.md)**: NoSQL + ベクトル検索
