# LUNAR

**LLM-based Understanding for Navigational and Adaptive Robotics**

LUNAR is an experimental framework for building intelligent home robots powered by large language models. It combines natural language understanding, symbolic skill execution, and live perception to create agents that can interpret human commands, plan multi-step tasks, react to dynamic changes, and ask for help when needed.

---


## 🛠️ Setup Instructions

- Clone and install repo: `pip install -e .`
- Install requirements: `pip install -r requirements.txt`
- Setup OpenAI key in `.env` file: `OPENAI_API_KEY=sk...`
- Start env: `source .venv/bin/activate`
- Run server: `python lunarbot/message_server.py`
- Run chat interface: `python lunarbot/chat.py`
- Run simulation: `webots`
- Start chatting in `chat.py` terminal: "Hello!"

---

## ✨ Key Features

- **Language-first control**  
  Use natural language to drive behavior — no hardcoded scripts required.

- **Dynamic replanning**  
  Robots can detect when plans fail and autonomously replan with LLM feedback.

- **Symbolic + reactive skill layer**  
  Separates high-level reasoning from low-level motion, enabling both adaptation and control.

- **Scene awareness**  
  Uses simulated perception to track object positions and react when the environment changes.

---

## 📦 Example Workflow

1. **User command:**

   > "Go get the blue cube and bring it back."

2. **LLM-generated plan:**

   - Navigate to blue cube
   - Grasp blue cube
   - Return to start
   - Release

3. **Live simulation:**
   - Robot executes steps in PyBullet
   - If the object moves or disappears, the LLM is prompted to replan
   - The robot may ask:
     > "I can't find the blue cube. Do you know where it might be?"

---

## 🧪 Test Case Preview

- Search for an object that isn’t immediately visible
- Handle failure mid-task and replan
- Ask the user for guidance if the goal becomes ambiguous
- Chain multiple steps with memory of locations and task progress

More test cases: [test_cases.md](./test_cases.md)

---

## 🚀 Coming Soon

- Real-world hardware integration (ROS2 or microcontroller interface)  
- Visual grounding and object detection  
- Memory persistence and long-term task context  
- Voice interaction and multimodal inputs

---

## License

MIT License.
