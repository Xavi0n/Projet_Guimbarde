from PWM import set_pwm_width, angle_to_pulse,enable_one_channel, disable_one_channel
import time

import math

PERSON_ID = 1
BOTTLE_ID = 2
FLOWER_POT_ID = 3

def find_closest_object_to_center(I2C_parsed_objects, target_id, center_x=160, center_y=120):
    """
    Finds the object with the given ID that is closest to the image center.

    Parameters:
        I2C_parsed_objects (list): List of object dictionaries from parse_huskylens_response().
        target_id (int): The object ID to search for.
        center_x (int): X-coordinate of the image center (default: 160).
        center_y (int): Y-coordinate of the image center (default: 120).

    Returns:
        Dictionary of the closest matching object, or None if no match is found.
    """
    closest_obj = None
    min_distance = float('inf')

    for obj in I2C_parsed_objects:
        if obj['id'] != target_id:
            continue

        dx = obj['x'] - center_x
        dy = obj['y'] - center_y
        distance = math.hypot(dx, dy)  # Euclidean distance

        if distance < min_distance:
            min_distance = distance
            closest_obj = obj

    return closest_obj

def track_object_with_servos(I2C_parsed_objects, target_id, center_x=160, center_y=120):
    global x_servo_angle, y_servo_angle

    obj = find_closest_object_to_center(I2C_parsed_objects, target_id)

    if obj is None:
        print("No matching object found.")
        return

    x_diff = obj['x'] - center_x  # Horizontal direction
    y_diff = obj['y'] - center_y  # Vertical direction

    if x_diff < 5 and y_diff < 5:
        print("Object is centered, no movement needed.")
        Shoot_if_on_target()
        return

    # Move X-axis servo (channel 1)
    if x_diff > 0:
        x_servo_angle = min(180, x_servo_angle + 1)  # move right
    elif x_diff < 0:
        x_servo_angle = max(0, x_servo_angle - 1)    # move left

    # Move Y-axis servo (channel 2)
    if y_diff > 0:
        y_servo_angle = min(180, y_servo_angle + 1)  # move down
    elif y_diff < 0:
        y_servo_angle = max(0, y_servo_angle - 1)    # move up

    # Set servo PWM for X-axis and Y-axis servos
    set_pwm_width(1, angle_to_pulse(x_servo_angle))  # X-axis servo (channel 1)
    set_pwm_width(2, angle_to_pulse(y_servo_angle))  # Y-axis servo (channel 2)

    print(f"Moved servos to: X={x_servo_angle}, Y={y_servo_angle}")

def Shoot_if_on_target():
    enable_one_channel(4)
    print("Target acquired, shooting enabled.")
    time.sleep(0.5)         #ADJUST WAIT VALUE FOR CONSISTENT 3 ROUND BURSTS
    disable_one_channel(4)