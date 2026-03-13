import os

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def _get_selected_provider() -> str:
    return (os.getenv("PROVIDER_LLM") or "").strip().lower()


def get_embeddings_provider():
    selected_provider = _get_selected_provider()
    if selected_provider == "google":
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    if selected_provider == "openai":
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    raise ValueError(f"Unsupported provider: {os.getenv('PROVIDER_LLM')}")


def get_chat_provider(temperature: float = 0.5):
    selected_provider = _get_selected_provider()
    if selected_provider == "google":
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_CHAT_MODEL"),
            temperature=temperature,
        )
    if selected_provider == "openai":
        return ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"), temperature=temperature)
    raise ValueError(f"Unsupported provider: {os.getenv('PROVIDER_LLM')}")
