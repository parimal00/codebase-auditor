# src/config/llm.py
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

# def get_llm(model: str = "openrouter/free", temperature: float = 0):
#     return ChatOpenAI(
#         model="nvidia/nemotron-3.5-lightning:free",  
#         temperature=temperature,
#         openai_api_key=os.getenv("OPENAI_API_KEY"),
#         openai_api_base="https://openrouter.ai/api/v1",
#     )

# print(os.getenv("OPENAI_API_KEY"))
    
# llm = ChatOpenAI(
#     model="nvidia/nemotron-3.5-lightning:free",  
#     openai_api_key=os.getenv("OPENAI_API_KEY"), 
#     openai_api_base="https://openrouter.ai/api/v1",
#     timeout=30,
#     max_retries=2,
# )
# result = llm.invoke([{"role": "user", "content": "Hello, how are you?"}])
# print(result)

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
        timeout=120,
        max_retries=2,
)

# llm = get_llm()
# try:
#     result = llm.invoke([{"role": "user", "content": "Hello, how are you?"}])
#     print(result.content)
# except Exception as e:
#     print(f"Error: {type(e).__name__} - {e}")