# Galileo

LLMアプリケーションの評価と実験プラットフォーム。

## 本質

開発から本番運用まで、LLMの出力品質、幻覚、セキュリティリスクを体系的に評価・監視するプラットフォーム。

## 基本

- **ChainPoll**: 独自指標による幻覚の検出
- **Prompt管理**: プロンプトの実験と最適化
- **ガードレール**: 本番環境での入出力制御

## 使い方

```bash
pip install galileo-hq
```

```python
import galileo as pq

# ログイン
pq.login()

# プロジェクト初期化
pq.init(project_name="my_rag_project")

# ログ送信（テキスト、Chain等）
pq.log(
    input="What is the capital of France?",
    output="Paris",
    duration_ms=120,
    tags={"model": "gpt-4"}
)
```

## 参照

- [公式ドキュメント](https://docs.galileo.ai/)
