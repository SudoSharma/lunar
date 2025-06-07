from robot_skills import * 
from planner import propose_plan, resume_after_tools
from controller import Robot
import message_bus

robot = Robot()
timestep = int(robot.getBasicTimeStep())

while robot.step(timestep) != -1:
    cmd = message_bus.get_from_human()
    if not cmd:
        continue

    message_bus.send_to_human(f"Received: '{cmd}'")

    natural_reply, plan = propose_plan(cmd)
    message_bus.send_to_human(natural_reply)

    tool_outputs = []

    for step in plan:
        try:
            fn = step["function"]["name"]
            args = step["function"]["arguments"]
            tool_call_id = step.get("id", "no-id")
            output_msg = ""

            if fn == "navigate_to":
                output_msg = navigate_to(robot, **args)
            elif fn == "look_for":
                output_msg = look_for(robot, **args)
            elif fn == "grasp":
                output_msg = grasp(robot, **args)
            elif fn == "rotate":
                output_msg = rotate(robot, **args)
            elif fn == "remember_location":
                output_msg = remember_location(robot, **args)
            elif fn == "release":
                output_msg = release(robot)
            else:
                output_msg = f"No handler for skill: {fn}"

            # Default to a success message if function returns None
            if output_msg is None:
                output_msg = f"{fn} executed."

            tool_outputs.append({
                "tool_call_id": tool_call_id,
                "name": fn,
                "content": output_msg
            })

        except Exception as e:
            err_msg = f"Error during {fn}: {e}"
            message_bus.send_to_human(err_msg)
            tool_outputs.append({
                "tool_call_id": step.get("id", "no-id"),
                "name": fn,
                "content": err_msg
            })
            break  # Optionally stop executing the rest if one fails

    if tool_outputs:
        new_tool_calls, new_msg = resume_after_tools(tool_outputs)
        if new_msg:
            message_bus.send_to_human(new_msg)
