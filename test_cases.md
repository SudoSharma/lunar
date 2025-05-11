# Test Cases: Home Robot LLM + Skill Integration

This document defines high-level test cases for validating the robot's end-to-end behavior across perception, planning, tool execution, and user interaction. These test cases assume a system architecture where an LLM handles planning and reasoning, and skills are exposed as callable functions like `navigate_to`, `grasp`, and `release`.

## Test Case 1: Search and Ask for Help

**Prompt:**  
"Go get the blue cube."

**Expected Behavior:**
1. Robot scans its immediate surroundings but does not see the cube.
2. It autonomously navigates to a few nearby locations (e.g., kitchen, living room).
3. If the cube is still not found, it asks the user:
   "I can't find the blue cube. Do you know where it might be?"
4. User says:
   "Did you try the office?"
5. Robot navigates to the office, finds the cube, picks it up, and returns to the original location.

**Validates:**
- Object search logic
- Replanning via LLM
- Clarification dialogue and memory of location
- Retrieval and return behavior

---

## Test Case 2: Object Moved During Execution

**Prompt:**  
"Bring me the blue cube."

**During Execution:**
- The cube is moved during navigation (e.g., via simulation or manual interaction).

**Expected Behavior:**
- Robot notices the cube has moved and is no longer reachable.
- It reports:  
  "The cube has moved and I can't reach it."
- The LLM replans, locates the object, and continues the task.

**Validates:**
- Mid-task feedback and failure detection
- Replanning logic
- Adaptive task continuation

---

## Test Case 3: Clarify Ambiguous Command

**Prompt:**  
"Get the thing from the room."

**Expected Behavior:**
- Robot replies with a clarification request:  
  "What thing are you referring to? Can you name the object?"

**Validates:**
- Ambiguity detection
- Dialogue-based disambiguation
- Dynamic plan refinement

---

## Test Case 4: Multi-Step Sequential Task

**Prompt:**  
"Pick up the red cube, put it on the table, then come back here."

**Expected Behavior:**
- Robot plans and executes:
  1. Navigate to red cube
  2. Grasp
  3. Navigate to table
  4. Release
  5. Navigate back to the starting location

**Validates:**
- Multi-step planning
- Memory of temporary goals and return locations
- Correct execution ordering
