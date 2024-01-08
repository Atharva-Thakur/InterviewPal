import chainlit as cl
import pyttsx3  

def createAudio(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

from gtts import gTTS

mytext = 'Welcome to geeksforgeeks!'


@cl.on_chat_start
async def main():
    await cl.Avatar(
        name="Tool 1",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()
    await cl.Message(
        content="Here is an audio file",
        author="Tool 1"
    ).send()
    createAudio(mytext)
