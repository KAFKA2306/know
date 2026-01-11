# Letta (旧 MemGPT)

ステートフルなLLMエージェント構築フレームワーク。

## 本質

LLMのコンテキストウィンドウの制限を超え、長期記憶と状態管理を実現する「LLMのOS」のようなシステム。

## 基本

- **仮想コンテキスト管理**: OSの仮想メモリのように、必要な情報を動的にコンテキストに出し入れする
- **永続性**: エージェントの状態、記憶、ツールを永続化
- **自己編集**: エージェント自身が記憶を更新・整理

## 使い方

CLIでの使用が最も一般的:

```bash
pip install letta
```

```bash
# サーバー起動 (バックグラウンド)
letta server start

# クライアントで接続 (別ターミナル)
# CLIで対話可能
letta-cli run
```

Python SDK:

```python
from letta import CreateClient

client = CreateClient()

# エージェント作成
agent = client.create_agent(
    name="my_agent",
    memory=client.create_memory(human="My name is Sarah")
)

# メッセージ送信
response = client.send_message(
    agent_id=agent.id,
    message="What is my name?",
    role="user"
)
print(response.messages)
```

## 参照

- [公式ドキュメント](https://docs.letta.com/)
