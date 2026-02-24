"""Embedding functions for the pipeline."""
from .config import (
    OPENAI_API_KEY, USE_LOCAL_EMBEDDINGS,
    EMBEDDING_MODEL_OPENAI, EMBEDDING_MODEL_LOCAL,
)


def get_embedding_function():
    """Return the appropriate embedding function based on configuration."""
    if USE_LOCAL_EMBEDDINGS or not OPENAI_API_KEY:
        return _get_local_embedding_function()
    return _get_openai_embedding_function()


def _get_openai_embedding_function():
    """OpenAI embedding function for ChromaDB."""
    from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

    return OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL_OPENAI,
    )


def _get_local_embedding_function():
    """Local sentence-transformers embedding function for ChromaDB."""
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    return SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_LOCAL,
    )
