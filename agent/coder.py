from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import GPT_CODE_MODEL

class CoderAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=GPT_CODE_MODEL, temperature=0.3)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a senior developer. Write clean, functional code.

            Context: {context}
            Query: {query}
            """
        )

    def run(self, query: str, context: list[str]) -> str:
        context_str = "\n".join(context) if context else "None"
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query, "context": context_str})
        return response.content.strip()
