# Llama 3.1 Chatbot with Voice (Streamlit + Groq API + gTTS)

## Overview
This is a **Streamlit-based chatbot** powered by **Llama 3.1** using the **Groq API** for natural language processing. It features **text-to-speech (TTS) support** using `gTTS`, allowing the chatbot to respond with audio. The chatbot includes **interactive settings** for adjusting language, behavior, expertise, and response parameters, providing a personalized user experience.

## Features
- **Conversational AI**: Uses Llama 3.1 to generate responses.
- **Voice Output**: Converts text responses to speech using Google Text-to-Speech (gTTS).
- **Dynamic Audio Handling**: Automatically stops previous responses before playing a new one.
- **Customizable Settings**:
  - Toggle voice responses on/off.
  - Select preferred voice language.
  - Choose chatbot behavior (Casual or Formal).
  - Define areas of expertise.
  - Adjust AI parameters like temperature and token limits.
- **Chat History**: Displays previous interactions for a seamless experience.
- **User-Friendly Interface**: Built with Streamlit, offering a clean and interactive UI.

## Installation & Setup
### Prerequisites
- Python 3.8+
- Streamlit
- Groq API key
- Required Python libraries

### Installation Steps
1. Clone the repository or download the project files.
2. Install the required dependencies:
   ```sh
   pip install streamlit groq gtts
   ```
3. Set up your **config.json** file with your Groq API key.
4. Run the chatbot application:
   ```sh
   streamlit run app.py
   ```

## Usage
1. Launch the application in your browser.
2. Adjust the settings in the **sidebar**, including voice and chat preferences.
3. Type a question in the input field and press Enter.
4. The chatbot will generate a text response and optionally play the voice output.
5. If voice is enabled, the previous response's audio will stop when a new one starts.

## Customization
- Modify the **default behavior** and **expertise areas** by adjusting the sidebar settings.
- Change the **voice language** for TTS output.
- Experiment with **temperature and token limits** for varied response styles.

## Troubleshooting
- **API Key Errors**: Ensure your Groq API key is correctly set in `config.json`.
- **Audio Not Playing**: Check your browser’s autoplay settings and ensure gTTS is installed.
- **Slow Responses**: Reduce the max token limit or lower the temperature setting.
