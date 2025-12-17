import json
from app.llm.anthropic_client import client
from app.llm.agent_tools import fetch_logged_in_user, fetch_all_cars, fetch_filtered_cars



TOOLS = {
    "fetch_logged_in_user": {
        "name": "fetch_logged_in_user",
        "description": "Fetch logged-in user details from Neo4j.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"}
            },
            "required": ["user_id"]
        },
        "func": fetch_logged_in_user
    },
    "fetch_all_cars": {
        "name": "fetch_all_cars",
        "description": "Fetch all cars stored in Neo4j.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "func": fetch_all_cars
    },
    "fetch_filtered_cars": {
        "name": "fetch_filtered_cars",
        "description": "Fetch cars filtered by year / make / model.",
        "input_schema": {
            "type": "object",
            "properties": {
                "year": {"type": "integer"},
                "make": {"type": "string"},
                "model": {"type": "string"}
            },
           
            
            "required": []
        },
        "func": fetch_filtered_cars
    }
}


SYSTEM_PROMPT = """
You are an AI agent that uses tools.

When you want to call a tool, output ONLY a JSON object:

{
  "name": "<tool_name>",
  "input": { ... }
}

Valid tool_name values:
- fetch_logged_in_user
- fetch_all_cars
- fetch_filtered_cars

Rules:
- Never invent new tool names.
- Never output explanations with the JSON.
- Never wrap JSON in text, markdown, or code blocks.
- If no tool is needed, reply normally.
"""


def run_agent(user_message: str, user_id: int):
    """
    Runs user message through Claude, executes tool if needed,
    then returns a natural-language response.
    """

    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        system=SYSTEM_PROMPT,
        max_tokens=500,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    text_response = response.content[0].text.strip()

    print("\n===== MODEL RAW OUTPUT =====")
    print(text_response)
    print("===========================\n")

    if text_response.startswith("{"):
        try:
            tool_json = json.loads(text_response)
        except Exception:
            return {
                "text": "Invalid tool JSON received.",
                "raw_data": text_response
            }

        tool_name = tool_json.get("name")
        tool_input = tool_json.get("input", {})

        
        if tool_name == "fetch_logged_in_user":
            tool_input["user_id"] = user_id

        tool_entry = TOOLS.get(tool_name)
        if not tool_entry:
            return {"text": f"Unknown tool '{tool_name}'.", "raw_data": None}

        tool_func = tool_entry["func"]

        
        try:
            tool_result = tool_func(**tool_input)
        except Exception as e:
            return {"text": f"Tool execution error: {str(e)}", "raw_data": None}

        
        follow_up = client.messages.create(
            model="claude-3-5-haiku-latest",
            system="You are an AI assistant. Explain the tool result clearly to the user.",
            max_tokens=300,  
            messages=[        
                {"role": "assistant", "content": text_response},
                {"role": "user", "content": f"Tool Result: {json.dumps(tool_result)}"}
            ]
        )

        return {
            "text": follow_up.content[0].text.strip(),
            "raw_data": tool_result
        }

    return {
        "text": text_response,
        "raw_data": None
    }
