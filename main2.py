import chainlit as cl
import pandas as pd

# @cl.on_message
# async def main(message: cl.Message):
#     # Your custom logic goes here...
#     messages.append({"role":"user", "content":message.content})
#     question = generate_question()
#     messages.append({"role":"assitant", "content":question})
#     # Send a response back to the user
#     await cl.Message(
#         content=question,
#     ).send()

@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="What is your name?").send()
    if res:
        name = res['content']
        await cl.Message(
            content=f"Hello {name}",
        ).send()

    res = await cl.AskActionMessage(
    content="Pick an job title",
    actions=[
      cl.Action(name="Data Scientist", value="MLDL-train.csv", label="Data Scientist"),
      cl.Action(name="DevOps Engineer", value="DevOps-data.csv", label="DevOps Engineer")
    ]
    ).send()

    df = pd.read_csv(res.get("value"))
    job_title = res.get("name")

    if res:
        await cl.Message(
        content=f"Job title selected: {job_title}",
        ).send()


