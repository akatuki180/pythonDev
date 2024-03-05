import os
import time

from openai import OpenAI

os.environ['OPENAI_API_KEY'] = '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'
client = OpenAI()

# ファイルアップロード
file = client.files.create(
  file=open("content/kotowaza.txt", "rb"),
  purpose='assistants'
)

# Assistant作成
assistant = client.beta.assistants.create(
  name="ことわざ大魔神",
  instructions="あなたは日本のことわざを知りつくしている人です。Knowledgeのファイルを使用して質問に答えます。",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)

# Thread作成
thread = client.beta.threads.create()

# Thread内にMessageを作成し追加
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="「お」から始まることわざを教えて下さい"
)

## Thread作成と同時にMessageを作成して追加することもできます
# thread = client.beta.threads.create(
#   messages=[
#     {
#       "role": "user",
#       "content": "「お」から始まることわざを教えて下さい"
#     }
#   ]
# )

# スレッドを指定し実行
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)


# 実行が完了するまで待つ
while True:
    # 実行状態の取得
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print("run.status:", run.status)

    # completedになればループを抜ける
    if run.status == 'completed':
        break

    time.sleep(5)

# 結果受け取り
messages = client.beta.threads.messages.list(thread.id)
print(messages)