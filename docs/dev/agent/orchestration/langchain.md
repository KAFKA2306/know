# LangChain

LLMアプリケーション構築のためのフレームワーク。

## 本質

LLMと外部データ、計算リソースを結合し、複雑なアプリケーションやエージェントを構築するための「接着剤」兼「足場」。

## 基本

- **コンポーネント**: Prompt Template, LLM, Retriever, Toolなどの標準化された抽象化
- **Chains**: 処理の連鎖を定義
- **LCEL**: 宣言的にチェーンを記述するLangChain Expression Language

## 使い方

```bash
pip install langchain langchain-openai
```

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# モデル
llm = ChatOpenAI(api_key="...")

# プロンプト
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# チェーン定義 (LCEL)
chain = prompt | llm | StrOutputParser()

# 実行
print(chain.invoke({"topic": "ice cream"}))
```

## 参照

- [公式ドキュメント](https://python.langchain.com/docs/get_started/introduction)
