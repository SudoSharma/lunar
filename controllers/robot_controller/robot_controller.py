from lunarbot.robot_skills import * 
from lunarbot.planner import propose_plan, resume_after_tools
from controller import Robot
import requests
import json

def get_command():
    try:
        res = requests.get("http://localhost:5000/command").json()
        return res["text"]
    except Exception as e:
        print(f"[robot] Error fetching command: {e}")
        return None

def send_response(text):
    try:
        requests.post("http://localhost:5000/response", json={"text": text})
    except Exception as e:
        print(f"[robot] Error sending response: {e}")

robot = Robot()
timestep = int(robot.getBasicTimeStep())
camera = robot.getDevice('camera')
camera.enable(timestep)

while robot.step(timestep) != -1:
    cmd = get_command()
    if not cmd:
        continue

    natural_reply, plan = propose_plan(cmd)
    if plan:
        send_response(f"Proposed Plan: {[(step.function.name, step.function.arguments) for step in plan]}")
    send_response(natural_reply)

    tool_outputs = []

    for step in plan:
        try:
            tool_call_id = step.id
            fn = step.function.name
            args = json.loads(step.function.arguments)
            output_msg = ""

            if fn == "navigate_to":
                output_msg = navigate_to(robot, **args)
            elif fn == "move":
                output_msg = move(robot, **args)
            elif fn == "look_for":
                output_msg = look_for(robot, camera, **args)
            elif fn == "grasp":
                output_msg = grasp(robot, **args)
            elif fn == "rotate":
                output_msg = rotate(robot, **args)
            elif fn == "remember_location":
                output_msg = remember_location(**args)
            elif fn == "release":
                output_msg = release()
            else:
                output_msg = f"No handler for skill: {fn}"

            if output_msg is None:
                output_msg = f"{fn} executed."

            tool_outputs.append({
                "tool_call_id": tool_call_id,
                "name": fn,
                "content": output_msg
            })

        except Exception as e:
            err_msg = f"Error during {fn}: {e}"
            send_response(err_msg)
            tool_outputs.append({
                "tool_call_id": tool_call_id,
                "name": fn,
                "content": err_msg
            })
            break

    if tool_outputs:
        new_tool_calls, new_msg = resume_after_tools(tool_outputs)
        if new_msg:
            send_response(new_msg)
