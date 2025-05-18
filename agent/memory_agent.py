from memory.vectorstore import upsert_memory, search_memory

class MemoryAgent:
    def retrieve_context(self, query: str):
        results = search_memory(query)
        return [doc.page_content for doc in results]

    def store_interaction(self, query: str, response: str, agents_used: list):
        upsert_memory(query, response, agents_used)
