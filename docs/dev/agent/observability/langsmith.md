# LangSmith

LLMアプリケーション開発のためのプラットフォーム。

## 本質

LangChain社が提供する、開発から本番運用までのライフサイクル全体（デバッグ、テスト、評価、監視）を支えるツール。

## 基本

- **可視化**: LangChainの複雑なチェーンやエージェントの動作を詳細に追跡
- **データセット**: テストケースの管理と実行
- **ハブ**: プロンプトの共有と管理

## 使い方

1. LangSmithでAPIキーを発行
2. 環境変数を設定（これだけでLangChainの動作が自動記録される）

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
export LANGCHAIN_API_KEY="<your-api-key>"
export LANGCHAIN_PROJECT="my-project"
```

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI()
llm.predict("Hello, World!")
# 自動的にLangSmithにログが送信される
```

## 参照

- [公式ドキュメント](https://docs.smith.langchain.com/)
