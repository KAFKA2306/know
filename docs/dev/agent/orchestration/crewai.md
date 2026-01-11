# CrewAI

AIエージェントのオーケストレーションフレームワーク。

## 本質

役割を持った複数のAIエージェントが協力してタスクを遂行する「チーム」を設計・運用するためのフレームワーク。

## 基本

- **Role-playing**: 各エージェントに役割、目標、バックストーリーを設定
- **Task**: 具体的な達成目標を定義し、エージェントに割り当て
- **Process**: エージェント間の協調作業の順序（順次、階層的など）を制御

## 使い方

```bash
pip install crewai
```

```python
from crewai import Agent, Task, Crew, Process

# エージェント定義
researcher = Agent(
  role='Researcher',
  goal='Uncover groundbreaking technologies',
  verbose=True,
  backstory="You are a senior researcher..."
)

# タスク定義
task1 = Task(
  description='Analyze the latest AI trends',
  agent=researcher
)

# チーム組成と実行
crew = Crew(
  agents=[researcher],
  tasks=[task1],
  process=Process.sequential
)

result = crew.kickoff()
print(result)
```

## 参照

- [公式ドキュメント](https://docs.crewai.com/)
