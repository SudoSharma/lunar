import queue

inbox = queue.Queue()    # Robot → Human
outbox = queue.Queue()   # Human → Robot

def send_to_human(msg: str):
    inbox.put(msg)

def send_to_robot(msg: str):
    outbox.put(msg)

def get_from_human():
    try:
        return outbox.get_nowait()
    except queue.Empty:
        return None

def get_from_robot():
    try:
        return inbox.get_nowait()
    except queue.Empty:
        return None
