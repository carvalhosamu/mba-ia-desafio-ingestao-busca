import os

from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.runnables import chain
from dotenv import load_dotenv
from llm_providers import get_chat_provider
from pgvector_store import get_postgres_collection

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

provider = os.getenv("PROVIDER_LLM")
collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME") 
connection_url = os.getenv("DATABASE_URL")

def _validate_required_settings() -> None:
  selected_provider = (provider or "").strip().lower()
  required_settings = {
    "PROVIDER_LLM": provider,
    "PG_VECTOR_COLLECTION_NAME": collection_name,
    "DATABASE_URL": connection_url,
  }

  provider_specific_settings = {
    "google": ["GOOGLE_CHAT_MODEL", "GOOGLE_EMBEDDING_MODEL"],
    "openai": ["OPENAI_CHAT_MODEL", "OPENAI_EMBEDDING_MODEL"],
  }

  if selected_provider not in provider_specific_settings:
    raise ValueError(f"Unsupported provider: {provider}")

  for env_var_name in provider_specific_settings[selected_provider]:
    required_settings[env_var_name] = os.getenv(env_var_name)

  missing_vars = [name for name, value in required_settings.items() if not value]

  if missing_vars:
    raise ValueError(
      "Missing required environment variables: " + ", ".join(missing_vars)
    )

def _get_postgres_collection():
  return get_postgres_collection(collection_name=collection_name, connection_url=connection_url)

@chain
def _search_similar_contexts(pipiline_input: dict) -> dict:
  store = _get_postgres_collection()
  results =  store.similarity_search_with_score(pipiline_input["pergunta"], k=10)
  return {"contexto": [resultado[0].page_content for resultado in results], "pergunta": pipiline_input["pergunta"]}



def search_prompt(question=None) -> BaseMessage:
  if not question:
    raise ValueError("A pergunta do usuário é obrigatória.")

  _validate_required_settings()
    
  prompt_template = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["contexto", "pergunta"])
  chat_provider = get_chat_provider()

  pipeline = _search_similar_contexts | prompt_template | chat_provider
  result = pipeline.invoke({"pergunta": question})
  return result
    
    