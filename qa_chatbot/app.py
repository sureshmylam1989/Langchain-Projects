import os
import streamlit as st
# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# load env
load_dotenv()   

# Set environment variables only if they exist in .env
if os.getenv('LANGCHAIN_API_KEY'):
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
if os.getenv('LANGCHAIN_PROJECT'):
    os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
os.environ['LANGCHAIN_TRACING_V2'] = "true"
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are helpful assistant , please respond to the user queries in a concise and helpful manner."),
        ("user", "Question:{input}")
    ]
)


def generate_response(input, api_key, llm, temperature, max_tokens):
    if not api_key:
        api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(model_name=llm, temperature=temperature, max_tokens=max_tokens, api_key=api_key)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain.invoke({"input": input})

## title of the app
st.title("Demo Q&A Chatbot")

## Settings at the top
st.subheader("Settings")

# Create columns for horizontal layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    api_key = st.text_input("Enter your Groq API Key", type="password")

with col2:
    llm = st.selectbox("Select LLM model", ["groq/compound-mini", "groq/compound"])

with col3:
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

with col4:
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=300, value=100)

st.divider()  # Add a visual separator

## Enter User Input
st.write("Please ask any question")

user_input = st.text_input("Enter your question")

if user_input:
    try:
        response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.write("Assistant: ", response)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.write("Please enter a question")
    
