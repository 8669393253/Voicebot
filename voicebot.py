import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "list"])

import os
import json
import streamlit as st

import os
from gtts import gTTS
import base64
from io import BytesIO

# Streamlit page configurations
st.set_page_config(
    page_title="🤖 Llama 3.1 Chatbot",
    page_icon="🖪",
    layout="wide"
)

# Load configuration data
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()


# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True
if "language_code" not in st.session_state:
    st.session_state.language_code = "en"

# Function to convert text to speech and return base64 audio
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return base64.b64encode(audio_bytes.read()).decode('utf-8')

# Function to create an audio player with JavaScript to stop previous playback
def audio_player(audio_base64):
    audio_html = f"""
    <script>
        var audios = document.getElementsByTagName('audio');
        for (var i = 0; i < audios.length; i++) {{
            audios[i].pause();
            audios[i].currentTime = 0;
        }}
    </script>
    <audio controls autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html

# Sidebar with settings
with st.sidebar:
    st.title("🤖 Llama 3.1 Chatbot Settings")
    
    # Voice settings
    st.markdown("### Voice Settings")
    st.session_state.voice_enabled = st.checkbox(
        "Enable Voice", 
        value=st.session_state.voice_enabled
    )
    
    # Chat settings
    st.markdown("### Chat Settings")
    behavior = st.radio(
        "Chatbot Behavior", 
        ["Casual", "Formal"],
        index=0
    )
    
    expertise = st.selectbox(
        "Area of Expertise", 
        ["General Knowledge", "Technology", "Science", "History", "Art", "Literature"],
        index=0
    )
    
    interests = st.multiselect(
        "Interests",
        ["AI", "Space", "Health", "Gaming", "Music", "Sports"]
    )
    
    # Model settings
    st.markdown("### Model Settings")
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7
    )
    
    max_tokens = st.slider(
        "Max Tokens", 
        min_value=50, 
        max_value=2000, 
        value=500
    )
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Tansen")

# Main chat interface
st.title("🤖 Llama 3.1 Chatbot with Voice")
st.caption("Ask anything and hear the responses!")

# Display chat history
for i, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Add audio player for assistant responses
        if message["role"] == "assistant" and "audio_base64" in message:
            st.markdown(audio_player(message["audio_base64"]), unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Ask Llama..."):
    # Add user message to chat
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Create system message based on settings
    system_message = f"""
    You are a {behavior.lower()} assistant specialized in {expertise}.
    Your interests include {', '.join(interests) if interests else 'various topics'}.
    Respond in a {behavior.lower()} manner.
    """
    
    # Generate response
    messages = [
        {"role": "system", "content": system_message},
        *[{"role": msg["role"], "content": msg["content"]} 
          for msg in st.session_state.chat_history]
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        assistant_response = response.choices[0].message.content
        
        # Generate audio if enabled
        audio_base64 = None
        if st.session_state.voice_enabled:
            audio_base64 = text_to_speech(
                assistant_response,
                lang=st.session_state.language_code
            )
        
        # Add to chat history
        chat_entry = {
            "role": "assistant",
            "content": assistant_response
        }
        if audio_base64:
            chat_entry["audio_base64"] = audio_base64
        
        st.session_state.chat_history.append(chat_entry)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            if audio_base64:
                st.markdown(audio_player(audio_base64), unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
