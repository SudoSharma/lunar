from sim_world import init_world
from executor import execute_loop

if __name__ == "__main__":
    init_world(gui=True)
    user_command = input("🗣 What should the robot do? ")
    execute_loop(user_command)
