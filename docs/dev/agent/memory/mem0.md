# Mem0

AIのためのメモリレイヤー。

## 本質

ユーザー、セッション、AIエージェントごとに個別の記憶を管理し、継続的に学習・適応するインテリジェントなメモリシステム。

## 基本

- **パーソナライズ**: ユーザーごとの嗜好や履歴を記憶
- **API**: シンプルなAPIで記憶の保存・検索・管理が可能
- **適応性**: 時間経過とともに記憶を更新・最適化

## 使い方

```bash
pip install mem0ai
```

```python
from mem0 import Memory

m = Memory()

# 記憶を追加 (user_id紐づけ)
m.add("Likes to play cricket on weekends", user_id="alice", metadata={"category": "hobbies"})

# 記憶を検索
related_memories = m.search(query="What are Alice's hobbies?", user_id="alice")
print(related_memories)

# 履歴全体も取得可能
all_memories = m.get_all(user_id="alice")
```

## 参照

- [公式ドキュメント](https://docs.mem0.ai/)
