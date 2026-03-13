from langchain_postgres import PGVector

from llm_providers import get_embeddings_provider


def get_postgres_collection(collection_name: str, connection_url: str) -> PGVector:
    return PGVector(
        embeddings=get_embeddings_provider(),
        collection_name=collection_name,
        connection=connection_url,
        use_jsonb=True,
    )
