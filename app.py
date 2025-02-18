import streamlit as st
import requests
import os
import time

# Sidebar for API key input
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

def transcribe_audio(file, api_key):
    url = "https://api.groq.com/openai/v1/audio/transcriptions"  
    
    files = {"file": (file.name, file, file.type)}
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"model": "whisper-large-v3", "response_format": "json", "temperature": 0.0}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.json().get("text", "No transcription available")
    else:
        return f"Error: {response.status_code} - {response.text}"

def save_transcription(text, filename="transcription.txt"):
    with open(filename, "w") as f:
        f.write(text)
    return filename

st.title("Audio Transcriber with Groq Whisper")

uploaded_file = st.file_uploader("Upload an audio file (WAV, MP3, M4A, etc.)", type=["wav", "mp3", "m4a"])
start = time.time()

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    
    if st.button("Transcribe Audio"):
        if not api_key:
            st.error("Please enter your Groq API Key in the sidebar.")
        else:
            with st.spinner("Getting the text from the audio..."):
                transcription = transcribe_audio(uploaded_file, api_key)
                st.subheader("Transcription:")
                st.write("Scroll down to download the transcription")
                st.write(transcription)

                st.write("Time taken to transcribe the audio: ", time.time()-start, " seconds")
                
                transcription_file = save_transcription(transcription)
                st.download_button(label="Download Transcription", data=open(transcription_file, "r").read(), file_name="transcribed_data.txt", mime="text/plain")
