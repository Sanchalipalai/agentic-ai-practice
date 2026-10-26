from strands import Agent, tool
from strands.models.ollama import OllamaModel


@tool
def fetch_database_metrics(table_id: int) -> str:
    try:
        table_id = int(table_id)

        if table_id < 0:
            return "Invalid Table ID. Please provide a positive integer."

        metrics = {
            1: {"Rows": 1200, "Size": "15 MB"},
            2: {"Rows": 850, "Size": "8 MB"},
            3: {"Rows": 5000, "Size": "40 MB"}
        }

        if table_id in metrics:
            return f"Database Metrics: {metrics[table_id]}"
        else:
            return f"No metrics found for Table ID {table_id}."

    except:
        return "Invalid Table ID. Please provide a positive integer."


model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

agent = Agent(
    model=model,
    tools=[fetch_database_metrics]
)

agent("Fetch database metrics for table id 2")