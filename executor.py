import json
from robot_skills import navigate_to, grasp, release
from world import get_current_scene
from planner import plan_from_llm

def scene_check(skill_name, args, scene):
    if skill_name == "grasp":
        obj = args.get("object_name", "")
        return any(o["name"] == obj for o in scene)

    if skill_name == "navigate_to":
        target = args.get("location", "")
        # valid if it's a known location (e.g. "kitchen")
        if target in {o["location"] for o in scene}:
            return True
        # OR valid if it's an object we can navigate to
        if any(o["name"] == target for o in scene):
            return True
        return False

    return True


def execute_tool_calls(tool_calls):
    for i, call in enumerate(tool_calls):
        name = call.function.name
        args = json.loads(call.function.arguments)

        print(f"🔧 Executing: {name}({args})")
        if not scene_check(name, args, get_current_scene()):
            print(f"❌ Scene invalid for {name} — skipping or replanning.")
            return

        try:
            result = None
            if name == "navigate_to":
                result = navigate_to(args["location"])
            elif name == "grasp":
                result = grasp(args["object_name"])
            elif name == "release":
                result = release()
            else:
                print(f"❓ Unknown skill: {name}")

            if result == "replan":
                print("🔁 Replanning due to scene change...")
                new_prompt = f"The target for step {i+1} moved. What should I do now?"
                new_plan = plan_from_llm(new_prompt)
                print(f"🔄 New plan: {new_plan}")
                execute_tool_calls(new_plan)
                return

        except Exception as e:
            print(f"⚠️ Error during {name}: {e}")