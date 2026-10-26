from strands import Agent
from strands.models.ollama import OllamaModel
from strands.agent.conversation_manager import SummarizingConversationManager

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

agent = Agent(
    model=model,
    system_prompt="""
    You are a monitoring assistant.
    Reply in one short sentence (maximum 10 words).
    Do not explain unless asked.
    """,
    conversation_manager=SummarizingConversationManager(
        preserve_recent_messages=4
    )
)

messages = [
    "Start monitoring",
    "CPU 50%",
    "RAM 60%",
    "Disk 70%",
    "Check network",
    "Restart Apache",
    "CPU 80%",
    "Generate report",
    "Any errors?",
    "Stop monitoring"
]

for msg in messages:
    print(f"\nUser: {msg}")
    response = agent(msg)
    print("Agent:", response)