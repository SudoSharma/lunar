import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "remember_location",
            "description": "Save the robot's current location with a custom label for later use.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"}
                },
                "required": ["label"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "look_for",
            "description": "Look around from the current position for the specified object.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {"type": "string"}
                },
                "required": ["object_name"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rotate",
            "description": "Rotate the robot in place by a given angle in degrees (positive = left, negative = right).",
            "parameters": {
                "type": "object",
                "properties": {
                    "angle": {"type": "number"}
                },
                "required": ["angle"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Navigate to a known location or a previously remembered label.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grasp",
            "description": "Pick up an object if it's visible and within reach.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {"type": "string"}
                },
                "required": ["object_name"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "release",
            "description": "Release the currently held object.",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        },
    }
]

chat_history = [
    {
        "role": "system",
        "content": "You are a robot assistant. Plan and replan using available tools to complete the user's objective in a dynamic environment. You must call skills step by step using only the provided tools."
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

    reply = message.content or ""
    tool_calls = message.tool_calls or []

    return reply, tool_calls

def resume_after_tools(tool_outputs: list):
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
    return message.tool_calls or [], message.content

def reset_planner_memory():
    global chat_history
    chat_history = [
        {
            "role": "system",
            "content": "You are a robot assistant. Plan and replan using available tools to complete the user's objective in a dynamic environment. You must call skills step by step using only the provided tools."
        }
    ]
