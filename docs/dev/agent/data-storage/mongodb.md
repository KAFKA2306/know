# MongoDB

ドキュメント指向データベース。

## 本質

柔軟なスキーマを持つJSONライクなドキュメントを保存するデータベース。近年はベクトル検索機能（Atlas Vector Search）も統合。

## 基本

- **柔軟性**: スキーマレスで構造化データを保存可能
- **ベクトル検索**: Atlas Vector Searchにより、運用データとベクトルデータを統合管理
- **実績**: 大規模運用での高い信頼性と実績

## 使い方

```bash
pip install pymongo
```

```python
from pymongo import MongoClient

# 接続
client = MongoClient("mongodb+srv://<user>:<password>@cluster.mongodb.net/")
db = client.test_database
collection = db.test_collection

# データ挿入
post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python"]}
post_id = collection.insert_one(post).inserted_id

# 検索
import pprint
pprint.pprint(collection.find_one({"author": "Mike"}))
```

## 参照

- [公式ドキュメント](https://www.mongodb.com/docs/)
