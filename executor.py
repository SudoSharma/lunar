import json
from robot_skills import navigate_to, grasp, release
from world import get_current_scene
from planner import propose_plan, resume_after_tools

def scene_check(skill_name, args, scene):
    if skill_name == "grasp":
        obj = args.get("object_name", "")
        return any(o["name"] == obj for o in scene)

    if skill_name == "navigate_to":
        target = args.get("location", "")
        if target in {o["location"] for o in scene}:
            return True
        if any(o["name"] == target for o in scene):
            return True
        return False

    return True

def execute_loop(initial_user_command):
    tool_calls = propose_plan(initial_user_command)

    while tool_calls:
        tool_outputs = []

        for call in tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)
            tool_call_id = call.id

            print(f"🔧 Executing: {name}({args})")
            if not scene_check(name, args, get_current_scene()):
                content = f"Scene invalid for {name} with arguments: {args}"
                print(f"❌ {content}")
                tool_outputs.append({
                    "tool_call_id": tool_call_id,
                    "name": name,
                    "content": content
                })
                continue

            try:
                if name == "navigate_to":
                    content = navigate_to(args["location"])
                elif name == "grasp":
                    content = grasp(args["object_name"])
                elif name == "release":
                    content = release()
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

        tool_calls = resume_after_tools(tool_outputs)
