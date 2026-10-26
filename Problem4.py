from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Load model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# ---------------- Developer Agent ----------------
developer_agent = Agent(
    model=model,
    system_prompt="""
    You are a Developer Agent.
    Your job is to write clean and simple code snippets.
    Only return the code with a short explanation.
    """
)

# ---------------- Tool Wrapper ----------------
@tool
def ask_developer(task: str) -> str:
    """
    Sends the coding request to the Developer Agent.
    """
    return developer_agent(task)

# ---------------- Manager Agent ----------------
manager_agent = Agent(
    model=model,
    tools=[ask_developer],
    system_prompt="""
    You are a Manager Agent.

    Responsibilities:
    1. Read the user's request.
    2. If coding is needed, call the ask_developer tool.
    3. Format the final response as a technical markdown review.

    Markdown Format:

    ## Task
    <User Request>

    ## Developer Solution
    <Code from Developer Agent>

    ## Review
    Mention whether the solution satisfies the request.
    """
)

# ---------------- Run ----------------
user_input = input("Enter your request: ")

response = manager_agent(user_input)

print("\nFinal Response:\n")
print(response)