# Haystack

LLMアプリケーション構築のためのオープンソースフレームワーク。

## 本質

検索システム（Search）やRAG、QAシステムなど、実用的なNLPアプリケーションを構築することに主眼を置いたパイプラインフレームワーク。

## 基本

- **Pipeline**: コンポーネントを有向非巡回グラフ（DAG）として接続
- **Components**: Document Store, Retriever, Reader, Generatorなどのモジュール
- **実運用志向**: プロダクション環境での信頼性を重視

## 使い方

v2の例:

```bash
pip install haystack-ai
```

```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

# コンポーネント定義
prompt_builder = PromptBuilder(template="Tell me a joke about {{topic}}")
llm = OpenAIGenerator(api_key="...")

# パイプライン構築
pipeline = Pipeline()
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", llm)
pipeline.connect("prompt_builder", "llm")

# 実行
result = pipeline.run({"prompt_builder": {"topic": "Berlin"}})
print(result["llm"]["replies"][0])
```

## 参照

- [公式ドキュメント](https://haystack.deepset.ai/documentation)
