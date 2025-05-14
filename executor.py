import json
from robot_skills import navigate_to, grasp, release, rotate, look_for, remember_location
from planner import propose_plan, resume_after_tools

def execute_loop(initial_user_command):
    tool_calls = propose_plan(initial_user_command)

    while True:
        if not tool_calls:
           return [], None 

        tool_outputs = []

        for call in tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)
            tool_call_id = call.id

            print(f"🔧 Executing: {name}({args})")
            try:
                if name == "remember_location":
                    content = remember_location(args["label"])
                elif name == "look_for":
                    content = look_for(args["object_name"])
                elif name == "rotate":
                    content = rotate(args["angle"])
                elif name == "grasp":
                    content = grasp(args["object_name"])
                elif name == "release":
                    content = release()
                elif name == "navigate_to":
                    content = navigate_to(args["location"])
                else:
                    content = f"Unknown skill: {name}"
                    print(f"❓ {content}")

                tool_outputs.append({
                    "tool_call_id": tool_call_id,
                    "name": name,
                    "content": content
                })

            except Exception as e:
                content = f"⚠️ Error during {name}: {str(e)}"
                print(content)
                tool_outputs.append({
                    "tool_call_id": tool_call_id,
                    "name": name,
                    "content": content
                })

        tool_calls, assistant_reply = resume_after_tools(tool_outputs)

        if assistant_reply and not tool_calls:
            return [], assistant_reply
