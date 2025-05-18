from tools.calendar_tool import create_calendar_event
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import GPT_SIMPLE_MODEL
from datetime import datetime

def is_valid_iso_datetime(time_str: str) -> bool:
    try:
        datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

class SchedulerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model=GPT_SIMPLE_MODEL, temperature=0.4)
        self.prompt = ChatPromptTemplate.from_template(
            """
            Extract event details and convert the time to ISO 8601 format in UTC.
            For example: 2025-05-19T10:00:00Z

            Format your response exactly like this:
            TITLE: <event title>
            TIME: <YYYY-MM-DDThh:mm:ssZ>

            Query: {query}
            """
        )

    def run(self, query: str, context: list[str]) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})
        lines = response.content.strip().splitlines()
        title = next((l.split(":", 1)[1].strip() for l in lines if l.startswith("TITLE:")), None)
        time_str = next((l.split(":", 1)[1].strip() for l in lines if l.startswith("TIME:")), None)

        if not title or not time_str:
            return "❌ Couldn't parse event details."
            
        if not is_valid_iso_datetime(time_str):
            return "❌ Invalid datetime format. Expected ISO 8601 format (e.g., 2025-05-19T10:00:00Z)"

        link = create_calendar_event(title, time_str)
        return f"✅ Event '{title}' created. [View]({link})"
