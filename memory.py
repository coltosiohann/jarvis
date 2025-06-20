import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

embedding_fn = OpenAIEmbeddingFunction(api_key="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")

client = chromadb.Client()
collection = client.get_or_create_collection(name="jarvis_memory", embedding_function=embedding_fn)

def save_memory(prompt: str, response: str):
    collection.add(
        documents=[f"User: {prompt}\nJARVIS: {response}"],
        ids=[f"id_{hash(prompt)}"]
    )

def fetch_memories(query: str, k: int = 3) -> list:
    results = collection.query(query_texts=[query], n_results=k)
    return results['documents'][0] if results['documents'] else []
