from strands import Agent, tool
from strands.models.ollama import OllamaModel
import json

# Load Ollama model
model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)


# ------------------ Tool 1 ------------------
@tool
def get_questions(domain: str):
    if domain.lower() == "devops":
        return [
            ("Name a container tool?", "docker"),
            ("Name a CI/CD tool?", "jenkins"),
            ("Name a cloud provider?", "aws")
        ]
    else:   # MERN
        return [
            ("Frontend library?", "react"),
            ("Database used?", "mongodb"),
            ("Backend runtime?", "nodejs")
        ]


# ------------------ Tool 2 ------------------
@tool
def grade(questions, answers):
    score = 0
    wrong = []

    for i in range(len(questions)):
        if answers[i].lower() == questions[i][1]:
            score += 1
        else:
            wrong.append(questions[i][0])

    percent = (score / 3) * 100

    return score, percent, wrong


# ------------------ Tool 3 ------------------
@tool
def report(domain, percent, wrong):
    result = {
        "domain": domain,
        "score_percentage": percent,
        "remediation_areas": wrong
    }

    return json.dumps(result, indent=4)


# ------------------ Agents ------------------
assessor = Agent(model=model, tools=[get_questions])
grader = Agent(model=model, tools=[grade])
reporter = Agent(model=model, tools=[report])


# ------------------ Main Program ------------------
domain = input("Enter domain (MERN/DevOps): ")

questions = get_questions(domain)

answers = []

print("\nAnswer these questions:\n")

for q in questions:
    print(q[0])
    answers.append(input("Answer: "))

score, percent, wrong = grade(questions, answers)

print("\nScore:", score, "/3")
print("Percentage:", percent, "%")

print("\nFinal Report")
print(report(domain, percent, wrong))