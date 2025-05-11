import pybullet as p
import numpy as np
from sim_world import object_name_to_id, get_robot_id

def detect_object(name: str):
    """
    Simulated object detection using PyBullet's segmentation mask.
    Returns: {'position': [x, y, z], 'confidence': 1.0} or None
    """

    obj_id = object_name_to_id.get(name)
    if obj_id is None:
        return None

    robot_id = get_robot_id()
    robot_pos, _ = p.getBasePositionAndOrientation(robot_id)
    cam_target = [robot_pos[0] + 1.0, robot_pos[1], robot_pos[2]]

    view_matrix = p.computeViewMatrix(
        cameraEyePosition=[*robot_pos[:2], 0.5],
        cameraTargetPosition=[*cam_target[:2], 0.5],
        cameraUpVector=[0, 0, 1]
    )

    projection_matrix = p.computeProjectionMatrixFOV(
        fov=60,
        aspect=1.0,
        nearVal=0.1,
        farVal=10.0
    )

    _, _, _, _, seg = p.getCameraImage(
        width=224,
        height=224,
        viewMatrix=view_matrix,
        projectionMatrix=projection_matrix,
        renderer=p.ER_BULLET_HARDWARE_OPENGL
    )

    seg = np.array(seg)
    mask = seg[:, :, 0] == obj_id

    if not np.any(mask):
        return None  # Object not visible in camera

    # Simulated detection succeeded — return actual object position
    # (In a real system, you'd compute the 3D position from depth + pixel)
    pos, _ = p.getBasePositionAndOrientation(obj_id)
    return {"position": pos, "confidence": 1.0}
