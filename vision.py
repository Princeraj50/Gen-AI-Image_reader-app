# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv
load_dotenv()  # Take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Ensure API key is set correctly
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("GOOGLE_API_KEY environment variable not set.")
else:
    genai.configure(api_key=api_key)

## Function to load Google model and get responses
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input:
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

## Initialize our Streamlit app
st.set_page_config(page_title="Amazing Image Reader", page_icon=":sparkles:", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: black;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput, .stFileUploader {
            padding: 0.5rem;
        }
        @media (max-width: 600px) {
            .main {
                padding: 1rem;
                border-radius: 5px;
            }
            .css-1d391kg {
                padding: 1rem;
                border-radius: 5px;
            }
            .stButton button {
                padding: 0.3rem 0.5rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("Welcome to the Amazing Image Reader! :camera_flash:")

uploaded_file = st.file_uploader("Upload an image (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Here's the image you uploaded:", use_container_width=True)

input = st.text_input("Enter your text prompt here:", key="input")

submit = st.button("Analyze Image")

## If the submit button is clicked
if submit:
    if input == "" and image == "":
        st.warning("Please provide a text prompt and/or upload an image to proceed.")
    else:
        response = get_gemini_response(input, image)
        st.subheader("Analysis Result")
        st.write(response)