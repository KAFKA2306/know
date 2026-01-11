# Traceloop

OpenLLMetryに基づくLLM可観測性プラットフォーム。

## 本質

OpenTelemetry標準に基づき、LLMアプリケーションの実行データを透過的に収集・可視化するツール。

## 基本

- **簡単導入**: 既存のコードにわずかな行を追加するだけで計測開始
- **OpenTelemetry**: 標準規格準拠による高い相互運用性
- **アラート**: 異常検知と通知機能

## 使い方

```bash
pip install traceloop-sdk
```

```python
from traceloop.sdk import Traceloop

# 初期化（これだけでOpenAI等の呼び出しが自動計測される）
Traceloop.init(app_name="my_app")

# 通常通りコードを実行
import openai
openai.ChatCompletion.create(...)
```

## 参照

- [公式ドキュメント](https://www.traceloop.com/docs/introduction)
