import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Navigate to a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grasp",
            "description": "Pick up an object",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {"type": "string"}
                },
                "required": ["object_name"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "release",
            "description": "Let go of whatever is held",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }
    }
]

chat_history = [
    {
        "role": "system",
        "content": "You are a robot assistant. Plan and replan using tool calls to complete the user's objective in a dynamic environment."
    }
]

def propose_plan(user_command: str):
    chat_history.append({"role": "user", "content": user_command})
    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=chat_history,
        tools=TOOLS,
        tool_choice="auto"
    )
    message = response.choices[0].message
    chat_history.append({
        "role": "assistant",
        "content": message.content or "",
        "tool_calls": message.tool_calls
    })
    return message.tool_calls or []

def resume_after_tools(tool_outputs: list):
    """
    tool_outputs: list of dicts with keys:
      - tool_call_id
      - name
      - content (the result or simulated result)
    """
    for output in tool_outputs:
        chat_history.append({
            "role": "tool",
            "tool_call_id": output["tool_call_id"],
            "name": output["name"],
            "content": output["content"]
        })

    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=chat_history,
        tools=TOOLS,
        tool_choice="auto"
    )
    message = response.choices[0].message
    chat_history.append({
        "role": "assistant",
        "content": message.content or "",
        "tool_calls": message.tool_calls
    })
    return message.tool_calls or []

def reset_planner_memory():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "You are a robot assistant. Plan and replan using tool calls to complete the user's objective in a dynamic environment."
        }
    ]
