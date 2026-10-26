import json
import re
from pydantic import BaseModel
from strands import Agent
from strands.models.ollama import OllamaModel


# Pydantic model
class DeploymentManifest(BaseModel):
    image_tag: str
    replica_count: int
    environment: str


# Convert schema to string
schema = json.dumps(DeploymentManifest.model_json_schema(), indent=2)

# Create model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)

# Create agent
agent = Agent(
    model=model,
    system_prompt=f"""
You are an API.

Return ONLY one JSON object.

Do NOT return the schema.
Do NOT explain anything.
Do NOT use markdown.

The JSON must match this schema:

{schema}
"""
)

# Ask the model
response = agent(
    "Create a deployment manifest for nginx:v1.2 with 3 replicas in production."
)

print("Raw Output:\n")
print(response)

text = str(response)

# Try direct JSON parsing
try:
    data = json.loads(text)

except json.JSONDecodeError:
    # Find all JSON objects in the response
    matches = re.findall(r"\{[\s\S]*?\}", text)

    data = None

    # Use the JSON object that contains the required fields
    for item in matches:
        try:
            obj = json.loads(item)

            if (
                "image_tag" in obj
                and "replica_count" in obj
                and "environment" in obj
            ):
                data = obj
                break

        except:
            continue

    if data is None:
        raise ValueError("No valid deployment manifest found.")

# Validate with Pydantic
manifest = DeploymentManifest(**data)

print("\nValidated Deployment Manifest:")
print(manifest)