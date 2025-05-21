from PWM import set_pwm_width, angle_to_pulse, set_throttle_percent, disable_one_channel, enable_one_channel
import time

ACCELEROMETER = 0x00
JOYSTICK = 0x01

DEADZONE = 0


def AdjustFromTheSlab(SPI_frame_dict, Current_X_Angle, Current_Y_Angle):
    """
    Adjusts the position of the turret from info received from the command module.
    """
    # Extract relevant information from the SPI frame dictionary
    Manual_X = SPI_frame_dict.get("x")
    Manual_Y = SPI_frame_dict.get("y")
    Fire_Button = SPI_frame_dict.get("button")
    Fan_Speed = SPI_frame_dict.get("fan_speed")
    Shoot_Strength = SPI_frame_dict.get("shoot_strength")

    # Print the received information
    print(f"Manual X: {Manual_X}, Manual Y: {Manual_Y}, Fire Button: {Fire_Button}, Fan Speed: {Fan_Speed}, Shoot Strength: {Shoot_Strength}")

    if Manual_X != DEADZONE:
        set_pwm_width(1, angle_to_pulse(Current_X_Angle + Manual_X))  # X-axis servo (channel 1)
        print(f"X-axis servo angle: {Current_X_Angle + Manual_X}")

    if Manual_Y != DEADZONE:
        set_pwm_width(2, angle_to_pulse(Current_Y_Angle + Manual_Y))  # Y-axis servo 1 (channel 2)
        set_pwm_width(3, angle_to_pulse((270 - Current_Y_Angle) - Manual_Y))  # Y-axis servo 2 (channel 3)
        print(f"Y-axis servo angle: {Current_Y_Angle + Manual_Y}")

    if Fire_Button == 1:
        enable_one_channel(5)
        print("Fire button pressed, shooting enabled.")
    else:
        disable_one_channel(5)
        print("Fire button released, shooting disabled.")

    set_throttle_percent(3, Fan_Speed)  # Fan speed control (channel 3)
    set_throttle_percent(5, Shoot_Strength)  # Shooting strength control (channel 5)