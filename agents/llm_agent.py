import json
import urllib.request


def ask_local_llm(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen3:1.7b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]


def parse_llm_action(response):
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return None


def normalize_llm_action(action):
    if action is None:
        return None

    normalized = action.copy()

    if "action" in normalized and isinstance(normalized["action"], str):
        normalized["action"] = normalized["action"].upper()

    return normalized


if __name__ == "__main__":
    response = ask_local_llm(
        """
You are Hospital Logistics Agent B.

The authorized task is:
Deliver Medicine-X from Pharmacy-A to Room-205 using Robot-R1.

Return ONLY a JSON object with these fields:
action
resource
source
destination
zone
robot_id

Use the exact identifiers given in the task.
Do not shorten, rename, or normalize identifiers.
Use uppercase action names.

The requested action is to carry Medicine-X through Corridor-A.
Do not include explanations or markdown.
"""
    )

    action = parse_llm_action(response)
    normalized_action = normalize_llm_action(action)

    print("Raw LLM Response:")
    print(response)

    print("\nParsed Action:")
    print(action)

    print("\nNormalized Action:")
    print(normalized_action)