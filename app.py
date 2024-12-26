import streamlit as st
import os
import anthropic
import google.generativeai as genai
from openrouter.openrouter import Openrouter


def rephrase_prompt(prompt, api_key, llm_choice):
    if llm_choice == "Anthropic":
        client = anthropic.Anthropic(
            api_key=api_key,
        )
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": f"Rephrase the following prompt: {prompt}",
                }
            ],
        )
        return response.content[0].text
    elif llm_choice == "Gemini Flash 2.0":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(f"Rephrase the following prompt: {prompt}")
        return response.text
    elif llm_choice == "OpenRouter":
        os.environ["OPENROUTER_API_KEY"] = api_key
        openrouter_client = Openrouter(model="google/gemini-2.0-flash-exp")
        openrouter_client.append_messages("user", f"Rephrase the following prompt: {prompt}")
        response = ""
        try:
            for chunk in openrouter_client.ask_stream(text=f"Rephrase the following prompt: {prompt}"):
                print(f"Chunk: {chunk}")
                response += chunk
        except Exception as e:
            print(f"Error during OpenRouter stream: {e}")
            st.error("Error: OpenRouter stream failed")
            return None
        return response
    else:
        return prompt

def generate_response(prompt, api_key, llm_choice):
    if llm_choice == "Anthropic":
        client = anthropic.Anthropic(
            api_key=api_key,
        )
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.content[0].text
    elif llm_choice == "Gemini Flash 2.0":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        return response.text
    elif llm_choice == "OpenRouter":
        os.environ["OPENROUTER_API_KEY"] = api_key
        openrouter_client = Openrouter(model="google/gemini-2.0-flash-exp")
        openrouter_client.append_messages("user", prompt)
        response = ""
        try:
            for chunk in openrouter_client.ask_stream(text=prompt):
                print(f"Chunk: {chunk}")
                response += chunk
        except Exception as e:
            print(f"Error during OpenRouter stream: {e}")
            st.error("Error: OpenRouter stream failed")
            return None
        return response
    else:
      st.error("Error: Invalid LLM choice")
      return None


# Set the app's title with an icon
st.title("🤖 InaiArivu Buddy ")

# Add a prompt input area with a label
prompt = st.text_area("📝 Enter your prompt",
                     help="Write your question, statement, or any text here")

# Add rephrase option
rephrase = st.checkbox("🔄 Rephrase prompt",
                    help="Check to automatically rephrase the prompt")

# Add a radio button to select the LLM with a label
llm_choice = st.radio("🤖 Select LLM",
                   ["Anthropic", "Gemini Flash 2.0", "OpenRouter"],
                     help="Select which LLM to use for generating the response")

# Add API input text input box
api_key = st.text_input("🔑 Enter your API key", type="password",
                      help="Enter your API key")

# Style the button with a colored background and white text
if st.button("✨ Generate",
             help="Click to generate a response from the specified LLM."):
    if not prompt:
        st.error("Please enter a prompt. 📝")
    elif not api_key:
        st.error("Please enter your API key. 🔑")
    else:
        st.write("Generating response... ⏳")
        if rephrase:
            rephrased_prompt = rephrase_prompt(prompt, api_key, llm_choice)
            if rephrased_prompt:
                st.write(f"Rephrased Prompt: 🔄 {rephrased_prompt}")
                response = generate_response(rephrased_prompt, api_key, llm_choice)
                if response:
                  st.write(f"Response: 💡 {response}")
        else:
            response = generate_response(prompt, api_key, llm_choice)
            if response:
              st.write(f"Response: 💡 {response}")
# Add some styling to improve the look
st.markdown(
    """
    <style>
    
    .stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)