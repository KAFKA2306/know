# LLM Agents

自律システムの構築に必要なツールスタック。

## フレームワーク選定

| 用途 | 推奨 |
|------|------|
| マルチステップワークフロー・ツール統合 | LangChain/LangGraph |
| RAG・データ検索特化 | LlamaIndex |
| マルチエージェント協調 | CrewAI |

## Core Layers

1. **[Data Storage](data-storage/)**: ベクトルDB（Qdrant, Pinecone）
2. **[Observability](observability/)**: トレーシング・モニタリング（LangSmith, Langfuse）
3. **[Evaluation](evaluation/)**: 評価（Ragas, Galileo）
4. **[Orchestration](orchestration/)**: ワークフロー管理（LangChain, CrewAI）
5. **[Memory](memory/)**: 状態永続化（Mem0, Letta）
