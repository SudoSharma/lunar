import pybullet as p
import pybullet_data
import time
from world import object_name_to_id

robot_id = None  # Declare robot globally so skills can use it

def init_world(gui=True):
    global robot_id

    if gui:
        physics_client = p.connect(p.GUI)
    else:
        physics_client = p.connect(p.DIRECT)

    p.setGravity(0, 0, -9.8)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")

    # Add a simple robot base — sphere
    robot_start_pos = [0.0, 0.0, 0.1]
    robot_id = p.loadURDF("sphere2.urdf", robot_start_pos)
    object_name_to_id["robot"] = robot_id

    # Add objects
    cube_start_pos = [2.0, 0.0, 0.15]  # ~2 meters in front
    visual_shape_id = p.createVisualShape(
        shapeType=p.GEOM_BOX,
        halfExtents=[0.15, 0.15, 0.15],  # 30cm cube
        rgbaColor=[0, 0, 1, 1],  # blue
    )
    collision_shape_id = p.createCollisionShape(
        shapeType=p.GEOM_BOX,
        halfExtents=[0.15, 0.15, 0.15]
    )
    cube_id = p.createMultiBody(
        baseMass=1,
        baseCollisionShapeIndex=collision_shape_id,
        baseVisualShapeIndex=visual_shape_id,
        basePosition=cube_start_pos
    )
    object_name_to_id["blue cube"] = cube_id

    return physics_client

def get_position(object_name):
    obj_id = object_name_to_id.get(object_name)
    if obj_id is None:
        return None
    pos, _ = p.getBasePositionAndOrientation(obj_id)
    return pos

def step_sim(n=240):
    for _ in range(n):
        p.stepSimulation()
        time.sleep(1. / 240.)

def get_robot_id():
    return object_name_to_id.get("robot")

def move_object(object_name: str, new_pos: list):
    obj_id = object_name_to_id.get(object_name)
    if obj_id:
        p.resetBasePositionAndOrientation(obj_id, new_pos, [0, 0, 0, 1])
        print(f"🧊 Moved '{object_name}' to {new_pos}")
