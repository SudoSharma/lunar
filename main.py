# from sim_world import init_world
from controllers.robot_controller.robot_controller import execute_loop

if __name__ == "__main__":
    # init_world(gui=True)
    user_input = input("What can I do for you? ")
    while True:
        tool_calls, assistant_reply = execute_loop(user_input)

        if assistant_reply and not tool_calls:
            user_input = input(assistant_reply + "\n")
        else:
            break
