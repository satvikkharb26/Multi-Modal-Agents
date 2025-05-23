# Multi-Agent Assistant System

A sophisticated multi-agent system that handles various types of queries through specialized agents.

### You Tube Demo Link (Backend) - 
https://youtu.be/DZfDO-vWnlE

### Architecture Diagram - 
https://lucid.app/lucidspark/107e3036-f5ac-4b44-ac26-3df406a2da29/edit?viewport_loc=-808%2C-951%2C3275%2C1853%2C0_0&invitationId=inv_d6e4d84c-f315-4d46-98d3-2008687308b3
### File Structure

```none
multi_agent_assistant/
├── .env                    # Environment variables and configuration
├── config.py              # Configuration loading and constants
├── credentials.json       # Google Calendar API credentials
├── main.py                # FastAPI server entry point
├── requirements.txt       # Project dependencies
├── agents/                # Individual agent implementations
├── chains/                # Agent orchestration
├── memory/                # Vector storage and embeddings
└── tools/                 # External service integrations
```

### Core Components

1. API Layer (main.py)

* Implements a FastAPI server that handles incoming queries
* Initializes the vector store and agent graph
* Processes requests through /ask endpoint
* Returns responses with used agents

2. Agent Graph (chains/agent\_graph.py)

* Orchestrates the flow between different agents
* Implements a state machine using langgraph
* Flow: Planner → Specific Agent → Memory → End
* Manages the state transitions and agent coordination

3. Agents

* PlannerAgent: Routes queries to appropriate agents
* ResponderAgent: Handles general queries
* SchedulerAgent: Manages calendar events
* CoderAgent: Handles programming-related queries
* MemoryAgent: Manages conversation history

6. Memory System

* vectorstore.py: Implements Qdrant vector storage
* embeddings.py: Handles text embeddings (OpenAI/HuggingFace)

7. Tools

* calendar\_tool.py: Google Calendar integration

### Setup Requirements

1. Environment Setup
``` none
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Required Environment Variables
```
OPENAI_API_KEY=your_key
GPT_SIMPLE_MODEL=gpt-3.5-turbo
GPT_CODE_MODEL=gpt-4
EMBEDDING_MODEL=openai
QDRANT_HOST=[http://localhost:6333](http://localhost:6333)
QDRANT_COLLECTION=conversation_memory
GOOGLE_CALENDAR_CREDENTIALS_PATH=path/to/credentials.json
API_HOST=0.0.0.0
API_PORT=8000
MEMORY_TOP_K=3
```
4.External Services

* Qdrant vector database (running locally or remote)

* OpenAI API access

* Google Calendar API credentials

## Flow Description

1. Query Entry

* User sends query to /ask endpoint
* Request is processed by FastAPI server
* Planning Phase

2. Planning Phase

* PlannerAgent analyzes query intent
* Retrieves relevant context from memory
* Routes to appropriate specialized agent

3. Execution Phase

* Specialized agent processes query:
* ResponderAgent: General queries
* SchedulerAgent: Calendar management
* CoderAgent: Code-related queries

4. Memory Management

* Interaction stored in vector database
* Used for context in future queries

## Running the System
```
#Start Qdrant (if running locally)
docker run -p 6333:6333 qdrant/qdrant

#Start the API server
python main.py
```
The server will be available at [http://localhost:8000](http://localhost:8000)

## Security Notes

* Keep API keys and credentials secure

* Don't commit .env or credentials.json

* Use appropriate access controls for the API

## Dependencies

### Key packages and their purposes:

* fastapi: API server framework
* langchain: LLM interaction and chains
* qdrant-client: Vector database
* langgraph: Agent orchestration
* google-api-python-client: Calendar integration
* See requirements.txt for full list
  The architecture is designed to be modular and extensible, allowing for easy addition of new agents and capabilities.

