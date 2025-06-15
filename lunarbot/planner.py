import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOOLS = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "remember_location",
    #         "description": "Save the robot's current location with a custom label for later use.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "label": {
    #                     "type": "string",
    #                     "description": "The name to assign to the current location"
    #                 }
    #             },
    #             "required": ["label"]
    #         },
    #     },
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "look_for",
    #         "description": "Look around from the current position for the specified object.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "object_name": {
    #                     "type": "string",
    #                     "description": "Name of the object to search for (e.g., 'blue cube')"
    #                 }
    #             },
    #             "required": ["object_name"]
    #         },
    #     },
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "rotate",
    #         "description": "Rotate the robot in place by a given angle in degrees (positive = left, negative = right).",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "angle": {
    #                     "type": "number",
    #                     "description": "Degrees to rotate. Positive is left, negative is right."
    #                 }
    #             },
    #             "required": ["angle"]
    #         },
    #     },
    # },
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Move to a known or discoverable target location or object (e.g. kitchen, bedroom, blue ball)",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target location or object, like 'kitchen' or 'ball'"
                    }
                },
                "required": ["target"]
            },
        },
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "grasp",
    #         "description": "Pick up an object if it's visible and within reach.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "object_name": {
    #                     "type": "string",
    #                     "description": "Name of the object to pick up"
    #                 }
    #             },
    #             "required": ["object_name"]
    #         },
    #     },
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "release",
    #         "description": "Release the currently held object.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {}
    #         },
    #     },
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "move",
    #         "description": "Move the robot forward or backward by a specified distance in meters.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "distance": {
    #                     "type": "number",
    #                     "description": "Distance in meters (positive for forward, negative for backward)"
    #                 }
    #             },
    #             "required": ["distance"]
    #         },
    #     },
    # }
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
