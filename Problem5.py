from strands import Agent, tool
from strands.models.ollama import OllamaModel

# ---------------------------
# Model
# ---------------------------
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# ---------------------------
# Create placeholder agents
# ---------------------------
billing_agent = None
support_agent = None

# ---------------------------
# Handoff Tools
# ---------------------------
@tool
def transfer_to_billing():
    """
    Transfer the conversation to the Billing Agent.
    """
    print("\nHanding off to Billing Agent...\n")
    return billing_agent


@tool
def transfer_to_support():
    """
    Transfer the conversation to the Technical Support Agent.
    """
    print("\nHanding off to Technical Support Agent...\n")
    return support_agent


# ---------------------------
# Billing Agent
# ---------------------------
billing_agent = Agent(
    model=model,
    tools=[transfer_to_support],
    system_prompt="""
You are the Billing Agent.

Handle:
- invoices
- subscriptions
- payments
- refunds

If the user's issue is technical
(example: server errors, API failures,
network problems, deployment issues),
use transfer_to_support().
"""
)

# ---------------------------
# Technical Support Agent
# ---------------------------
support_agent = Agent(
    model=model,
    tools=[transfer_to_billing],
    system_prompt="""
You are the Technical Support Agent.

Handle:
- server issues
- API errors
- deployment problems
- debugging
- cloud infrastructure

If the user has a billing issue,
use transfer_to_billing().
"""
)

# ---------------------------
# User Query
# ---------------------------
user_query = (
    "My server instance is throwing a 502 Bad Gateway error, "
    "please fix it."
)

print("User:", user_query)

# Start with Billing Agent
response = billing_agent(user_query)

print("\nFinal Response:\n")
print(response)