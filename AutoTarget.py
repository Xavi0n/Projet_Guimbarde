from Servomotors import set_servo_pwm, angle_to_pulse

import math

PERSON_ID = 1
BOTTLE_ID = 2
FLOWER_POT_ID = 3

def find_closest_object_to_center(parsed_objects, target_id, center_x=160, center_y=120):
    """
    Finds the object with the given ID that is closest to the image center.

    Parameters:
        parsed_objects (list): List of object dictionaries from parse_huskylens_response().
        target_id (int): The object ID to search for.
        center_x (int): X-coordinate of the image center (default: 160).
        center_y (int): Y-coordinate of the image center (default: 120).

    Returns:
        Dictionary of the closest matching object, or None if no match is found.
    """
    closest_obj = None
    min_distance = float('inf')

    for obj in parsed_objects:
        if obj['id'] != target_id:
            continue

        dx = obj['x'] - center_x
        dy = obj['y'] - center_y
        distance = math.hypot(dx, dy)  # Euclidean distance

        if distance < min_distance:
            min_distance = distance
            closest_obj = obj

    return closest_obj

def track_object_with_servos(parsed_objects, target_id, center_x=160, center_y=120):
    global x_servo_angle, y1_servo_angle, y2_servo_angle

    obj = find_closest_object_to_center(parsed_objects, target_id)

    if obj is None:
        print("No matching object found.")
        return

    x_diff = obj['x'] - center_x  # Horizontal direction
    y_diff = obj['y'] - center_y  # Vertical direction

    # Move X-axis servo (channel 1)
    if x_diff > 0:
        x_servo_angle = min(180, x_servo_angle + 1)  # move right
    elif x_diff < 0:
        x_servo_angle = max(0, x_servo_angle - 1)    # move left

    # Move Y-axis servos (channel 2 and 3)
    if y_diff > 0:
        y1_servo_angle = min(180, y1_servo_angle + 1)  # move down
        y2_servo_angle = min(180, y2_servo_angle + 1)
    elif y_diff < 0:
        y1_servo_angle = max(0, y1_servo_angle - 1)    # move up
        y2_servo_angle = max(0, y2_servo_angle - 1)

    # Set servo PWM for X-axis and Y-axis servos
    set_servo_pwm(1, angle_to_pulse(x_servo_angle))  # X-axis servo (channel 1)
    set_servo_pwm(2, angle_to_pulse(y1_servo_angle))  # Y1-axis servo (channel 2)
    set_servo_pwm(3, angle_to_pulse(y2_servo_angle))  # Y2-axis servo (channel 3)

    print(f"Moved servos to: X={x_servo_angle}, Y1={y1_servo_angle}, Y2={y2_servo_angle}")