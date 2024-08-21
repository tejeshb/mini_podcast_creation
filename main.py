import streamlit as st
import whisper
import openai
from gtts import gTTS
from openai import OpenAI

# Streamlit app
st.title("Audio Transcription and Summarization App")

# Input API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key to proceed.")
    st.stop()

# Set OpenAI API key
openai.api_key = api_key
client = OpenAI()

# Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    # Transcribe the audio file
    st.write("Transcribing the audio file...")
    transcription =  client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
    transcript = transcription.text
    st.write("Transcribed Text:\n", transcript)

    # Summarize the transcribed text
    st.write("Summarizing the text...")
    def summarize_text(transcription):
        response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
        return response.choices[0].message.content

    summary = summarize_text(transcript)
    st.write("Summary:\n", summary)

    # Convert the summary to speech
    st.write("Converting summary to speech...")
    def text_to_speech(text, output_file):
        tts = gTTS(text)
        tts.save(output_file)
        st.audio(output_file)

    text_to_speech(summary, "short_podcast.mp3")
