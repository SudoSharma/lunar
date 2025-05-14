from sim_world import get_position, step_sim, get_robot_id, move_object
from perception import detect_object
import pybullet as p

def look_for(object_name: str):
    info = detect_object(object_name)
    if info:
        return f"Found {object_name} at {info['position']}"
    else:
        return f"Could not find {object_name} from this location"

def navigate_to(target_name: str):
    print(f"🚶 Navigating to {target_name}...")

    robot_id = get_robot_id()
    target_pos = get_position(target_name)

    if not robot_id or not target_pos:
        print(f"❌ Cannot navigate to {target_name}")
        return "failed"

    expected_pos = target_pos  # Save for scene drift detection

    for step in range(200):  # max steps
        # # Simulate cube moving mid-navigation
        # if step == 40 and target_name == "blue cube":
        #     print("👋 Moving blue cube to test replanning...")
        #     move_object("blue cube", [3.0, 0.0, 0.15])  # simulate disruption

        # Get current target position (it might have moved)
        current_pos = get_position(target_name)

        # Replan if target moved too far from expected
        drift = sum(
            (current_pos[i] - expected_pos[i])**2
            for i in range(2)
        ) ** 0.5

        if drift > 0.2:  # drift threshold (20 cm)
            print("⚠️ Object moved — aborting and triggering replanning")
            return "replan"

        # Robot motion logic
        robot_pos, _ = p.getBasePositionAndOrientation(robot_id)
        dx = current_pos[0] - robot_pos[0]
        dy = current_pos[1] - robot_pos[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 0.05:
            print(f"✅ Reached {target_name}")
            return "success"

        step_size = 0.01
        vx = dx / distance * step_size
        vy = dy / distance * step_size
        new_pos = [robot_pos[0] + vx, robot_pos[1] + vy, robot_pos[2]]

        p.resetBasePositionAndOrientation(robot_id, new_pos, [0, 0, 0, 1])
        step_sim(1)

    print("⚠️ Timed out trying to navigate.")
    return "failed"

def grasp(object_name: str):
    print(f"🤖 Attempting to grasp {object_name}...")
    pos = get_position(object_name)
    if pos:
        print(f"✅ Pretending to grasp object at {pos}")
        step_sim(100)
    else:
        print(f"❌ Cannot find object: {object_name}")

def release():
    print("👐 Releasing object...")
    step_sim(60)
