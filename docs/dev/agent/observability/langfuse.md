# Langfuse

オープンソースのLLMエンジニアリングプラットフォーム。

## 本質

LLMアプリケーションの実行トレース、評価、プロンプト管理を一元化し、詳細な可視化を提供するツール。

## 基本

- **トレース**: 実行フロー全体を可視化しデバッグを容易に
- **評価**: モデルベース評価やユーザーフィードバックの収集
- **プロンプト管理**: バージョン管理とテスト

## 使い方

```bash
pip install langfuse
```

```python
import os
from langfuse import Langfuse

# APIキー設定（環境変数推奨）
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."

langfuse = Langfuse()

# トレース作成
trace = langfuse.trace(name="llm-feature")

# スパン（処理単位）作成
span = trace.span(name="embedding")
span.end()

trace.update(output="Result")
```

## 参照

- [公式ドキュメント](https://langfuse.com/docs)
