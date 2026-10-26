from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Local LLM
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# Tool
@tool
def check_server_status():
    """Checks the server status."""
    print("Checking server...")
    return "Server is running."

# Agent
agent = Agent(
    model=model,
    tools=[check_server_status]
)

# Maximum allowed iterations
max_loops = 3

for i in range(max_loops):
    print(f"\nIteration {i+1}")
    response = agent("Check the server status.")
    print(response)

print("\nMaximum iterations reached! Agent stopped.")