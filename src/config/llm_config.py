import os
from langchain_openai.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

def get_llm(provider="openai", temperature=0.3, model="gpt-4"):
    """
    Factory function to create LLM instances based on provider

    Args:
        provider (str): "openai", "azure", "groq", or "gemini"
        temperature (float): Model temperature
        model (str): Model name/deployment
    """
    if provider == "azure":
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temperature
        )
    elif provider == "groq":
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name=os.getenv("GROQ_MODEL_NAME"),
            temperature=temperature,
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL_NAME"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=temperature,
        )
    else:  # default to OpenAI
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
            model=model
        )
