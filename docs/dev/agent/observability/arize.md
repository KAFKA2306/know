# Arize

AIの可観測性と評価プラットフォーム。

## 本質

本番環境のMLモデルとLLMアプリケーションの品質劣化、ドリフト、パフォーマンスを監視・トラブルシューティングするツール。

## 基本

- **Phoenix**: LLMトレースと言語評価のためのオープンソースライブラリ（ローカル開発用）
- **評価**: RAGの検索品質や幻覚（Hallucination）の検出
- **埋め込み可視化**: ベクトル空間の可視化によるデータ理解

## 使い方

ローカルでの可視化（Phoenix）の例：

```bash
pip install arize-phoenix
```

```python
import phoenix as px

# アプリケーション起動
session = px.launch_app()

# 以降、OpenInference対応のトレーサー（LlamaIndex等）からのデータを自動受信
# または手動でデータフレームをログ送信
# px.log_evaluations(...)
```

## 参照

- [公式ドキュメント](https://docs.arize.com/arize/)
