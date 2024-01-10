from gtts import gTTS
import gradio as gr

def tts(text):
    myobj = gTTS(text=text, lang='en', slow=False) 
    myobj.save("test.wav") 
    return 'test.wav'

iface = gr.Interface(fn = tts,
                     inputs = "textbox",
                     outputs = gr.Audio(autoplay=True), 
                     verbose = True)

iface.launch()