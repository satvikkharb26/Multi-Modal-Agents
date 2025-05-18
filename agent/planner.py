from agents.memory_agent import MemoryAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import GPT_SIMPLE_MODEL

class PlannerAgent:
    def __init__(self):
        self.memory_agent = MemoryAgent()
        self.llm = ChatOpenAI(model=GPT_SIMPLE_MODEL, temperature=0)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an intent classifier. 
            Given the user's message, classify the intent as one of the following:
            - "responder" for general/simple queries.
            - "scheduler" only if the user explicitly stated to set up a meeting or block a time. 
            - "coder" for anything about programming, code, functions, bugs, or APIs.

            Respond with only one word: responder, scheduler, or coder.

            Message: {query}
            """
        )

    def analyze_intent(self, query: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})
        return response.content.strip().lower()

    def plan(self, query: str) -> dict:
        context = self.memory_agent.retrieve_context(query)
        destination = self.analyze_intent(query)
        return {"next_agent": destination, "context": context}
