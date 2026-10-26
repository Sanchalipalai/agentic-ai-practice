import os

from strands import Agent, tool
from strands.models.ollama import OllamaModel


model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# Tool 1: List files in current directory
@tool
def list_directory_contents() -> str:
    """
    Lists all files and folders in the current directory.
    """
    files = os.listdir(".")
    return "\n".join(files)


# Tool 2: Read a file safely
@tool
def read_file_content(filename: str) -> str:
    """
    Reads the contents of a file.
    """

    # Allow only files in current folder
    filepath = os.path.join(".", filename)

    if not os.path.isfile(filepath):
        return "File not found."

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


# Create agent
agent = Agent(
    model=model,
    tools=[list_directory_contents, read_file_content],
)

# User request
query = """
Scan the current project folder.
Read the file named mock_log.txt.
Find every line containing the word CRITICAL.
Display only those lines.
"""

# Run agent
response = agent(query)

print("\n===== Agent Response =====\n")
print(response)