from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import GPT_SIMPLE_MODEL

class ResponderAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=GPT_SIMPLE_MODEL, temperature=0.7)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful assistant. Use the context if available to answer the user.

            Context: {context}
            User: {query}
            """
        )

    def run(self, query: str, context: list[str]) -> str:
        context_str = "\n".join(context) if context else "None"
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query, "context": context_str})
        result = response.content.strip()
        return result.removeprefix("Response:").strip()
