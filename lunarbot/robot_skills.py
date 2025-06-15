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

# def look_for(robot, camera, object_name: str):
#     b64_image = get_camera_image(camera)
#     result = call_gpt4o_with_image_base64(b64_image, object_name)
#     return result


def look_for(robot, camera, object_name: str) -> str:
    for attempt in range(4):  # Try 4 directions (0°, 90°, 180°, 270°)
        b64_image = get_camera_image(camera)
        response = call_gpt4o_with_image_base64(b64_image, object_name)
        print(response)

        if "yes" in response.lower():
            return f"Found {object_name} in view {attempt * 90}°"
        
        # Rotate 90 degrees to the left
        rotate(robot, angle=90)

    return f"Could not find {object_name} after looking around."

def navigate_to(robot, target: str):
    return "Done"


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
