import openai
import os
from PIL import Image
import base64
import io
from dotenv import load_dotenv
from controller import Motor
import math

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_camera_image(camera):
    width = camera.getWidth()
    height = camera.getHeight()
    raw = camera.getImage()

    img = Image.frombytes("RGBA", (width, height), raw)
    img = img.convert("RGB")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def call_gpt4o_with_image_base64(b64_image: str, object_name: str):
    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "user", "content": f"Is there a {object_name} in this image? Reply only with yes, or no."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content

def look_for(robot, camera, object_name: str, max_attempts: int = 12, move_every: int = 3):
    for attempt in range(max_attempts):
        b64_image = get_camera_image(camera)
        response = call_gpt4o_with_image_base64(b64_image, object_name)
        print(f"[look_for] Attempt {attempt + 1}: GPT response → {response}")

        if "yes" in response.lower():
            return f"Found {object_name} in view on attempt {attempt + 1}"

        if (attempt + 1) % move_every == 0:
            move(robot, distance=5)
        else:
            rotate(robot, angle=90)

    return f"Could not find {object_name} after {max_attempts} attempts."

def navigate_to(robot, target: str):
    # TODO: Check if 'target' is a known location or remembered object.
    # If known, retrieve its position and move there directly.

    # If unknown, fallback to visual search
    result = look_for(robot, robot.getDevice("camera"), target)
    return f"Navigation result: {result}"


def move(robot, distance: float, speed: float = 2.0):
    """
    Move the robot forward or backward by a given distance (in meters).
    Positive = forward, Negative = backward.
    """

    timestep = int(robot.getBasicTimeStep())
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))

    direction = 1 if distance >= 0 else -1
    actual_speed = direction * abs(speed)

    left_motor.setVelocity(actual_speed)
    right_motor.setVelocity(actual_speed)

    # Assume speed is in m/s and robot moves at speed meters per second
    duration_secs = abs(distance) / abs(speed)
    steps = int((duration_secs * 1000) / timestep)

    for _ in range(steps):
        robot.step(timestep)

    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    return f"Moved {'forward' if direction == 1 else 'backward'} {abs(distance):.2f} meters."


def grasp(robot, object_name: str):
    return "Done"

def rotate(robot, angle: int):
    # Convert degrees to radians
    angle_rad = math.radians(angle)

    # Robot parameters
    WHEEL_RADIUS = 0.02  # in meters (adjust to your robot)
    AXLE_LENGTH = 0.05   # distance between wheels in meters (adjust to your robot)

    # Compute rotation time
    angular_speed = 1.0  # rad/s
    duration = abs(angle_rad / angular_speed)

    # Get motors
    left_motor: Motor = robot.getDevice("left wheel motor")
    right_motor: Motor = robot.getDevice("right wheel motor")

    # Enable velocity control
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # Determine wheel speeds
    if angle > 0:
        left_speed = angular_speed
        right_speed = -angular_speed
    else:
        left_speed = -angular_speed
        right_speed = angular_speed

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

    steps = int(duration * 1000 / robot.getBasicTimeStep())
    for _ in range(steps):
        robot.step(int(robot.getBasicTimeStep()))

    # Stop motors
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    return f"Rotated {angle} degrees."

def remember_location(label: str):
    return "Done"

def release():
    return "Done"
