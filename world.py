import pybullet as p

# This should be shared with sim_world
object_name_to_id = {}

def get_current_scene():
    scene = []
    for name, obj_id in object_name_to_id.items():
        pos, _ = p.getBasePositionAndOrientation(obj_id)
        scene.append({"name": name, "location": pos})
    return scene
