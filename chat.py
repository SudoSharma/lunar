import threading
import message_bus
import time

def listen_to_robot():
    while True:
        msg = message_bus.get_from_robot()
        if msg:
            print(f"\nBot: {msg}\n> ", end="", flush=True)
        time.sleep(0.2)

def main():
    print("Type 'quit' to exit.")
    threading.Thread(target=listen_to_robot, daemon=True).start()

    while True:
        user_input = input("> ")
        if user_input.lower() == "quit":
            break
        message_bus.send_to_robot(user_input)

if __name__ == "__main__":
    main()
