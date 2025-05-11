from sim_world import init_world
from planner import plan_from_llm
from executor import execute_tool_calls

if __name__ == "__main__":
    init_world(gui=True)
    user_command = input("🗣 What should the robot do? ")
    # TODO: rename to generate_plan
    tool_calls = plan_from_llm(user_command)
    # TODO: rename to execute_plan
    execute_tool_calls(tool_calls)
