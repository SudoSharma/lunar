import requests
import threading
import time

def poll_responses():
    while True:
        try:
            res = requests.get("http://localhost:5000/response").json()
            if res["text"]:
                print(f"\nBot: {res['text']}\n> ", end="", flush=True)
        except:
            pass
        time.sleep(0.5)

def main():
    print("Type 'quit' to exit.")
    threading.Thread(target=poll_responses, daemon=True).start()

    while True:
        msg = input("> ")
        if msg.lower() == "quit":
            break
        try:
            requests.post("http://localhost:5000/command", json={"text": msg})
        except Exception as e:
            print(f"Failed to send message: {e}")

if __name__ == "__main__":
    main()
