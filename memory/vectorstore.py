from langchain_qdrant import Qdrant
from langchain.schema import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from config import QDRANT_HOST, QDRANT_COLLECTION, MEMORY_TOP_K
from memory.embeddings import get_embedding_model

def get_qdrant_client():
    return QdrantClient(url=QDRANT_HOST)

def init_qdrant():
    client = get_qdrant_client()
    if QDRANT_COLLECTION not in [col.name for col in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )

def get_vectorstore():
    client = get_qdrant_client()
    # Ensure collection exists
    if QDRANT_COLLECTION not in [col.name for col in client.get_collections().collections]:
        init_qdrant()
    return Qdrant(
        client=client,
        collection_name=QDRANT_COLLECTION,
        embeddings=get_embedding_model()
    )


def upsert_memory(query: str, response: str, agents: list):
    doc = Document(
        page_content=f"Query: {query}\nResponse: {response}",
        metadata={"agents": agents}
    )
    vectorstore = get_vectorstore()
    vectorstore.add_documents([doc])

def search_memory(query: str):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=MEMORY_TOP_K)
