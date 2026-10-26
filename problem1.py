import random

from strands import Agent, tool
from strands.models.ollama import OllamaModel


# Tool
@tool
def run_test_suite(suite_name: str) -> dict:


    pass_rate = random.randint(60, 100)
    execution_time = f"{random.randint(10, 90)} seconds"

    return {
        "suite_name": suite_name,
        "pass_rate": f"{pass_rate}%",
        "execution_time": execution_time
    }


# Ollama Model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:1b"   
)

# Agent
agent = Agent(
    model=model,
    tools=[run_test_suite],
    system_prompt="""
    You are a QA Automation Assistant.
    Whenever the user asks to execute or run a test suite,
    use the run_test_suite tool.
    """
)

print("QA Automation Agent")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    agent(user_input) 