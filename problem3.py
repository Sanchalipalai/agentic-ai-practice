from strands import Agent, tool
from strands.models.ollama import OllamaModel


# Tool
@tool
def evaluate_system_thresholds(
    cpu_utilization: float,
    ram_available_gb: float,
    disk_io_mbps: int
) -> str:
    """
    Evaluates system health based on CPU, RAM, and Disk I/O.
    """

    alerts = []

    if cpu_utilization > 80:
        alerts.append("High CPU usage")

    if ram_available_gb < 8:
        alerts.append("Low available RAM")

    if disk_io_mbps > 100:
        alerts.append("High Disk I/O")

    if alerts:
        return "System Alert: " + ", ".join(alerts)
    else:
        return "System is operating within normal limits."


# Load local model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# Create agent
agent = Agent(
    model=model,
    tools=[evaluate_system_thresholds]
)

# User prompt
response = agent(
    "The system is currently running with a CPU usage of 85.5 percent, "
    "4GB RAM left, and disk speeds at 120 mbps. Give me an assessment."
)

print(response)