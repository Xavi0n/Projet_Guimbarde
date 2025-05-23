import rc
import time

def init_PWM():
    """
    Initialize the PWM subsystem.
    This function should be called before using any PWM functions.
    """
    rc.pwm_init()
    rc.pwm_power_rail_en(True)
    print("PWM subsystem initialized and power rail enabled")

def set_pwm_width(channel: int, pulse_us: int):
    """
    Send a pulse to a PWM output using librobotcontrol.
    Args:
        channel (int): PWM channel (1–8 on BeagleBone Blue)
        pulse_us (int): Pulse width in microseconds (1000–2000 typical)
    """
    rc.pwm_set_width(channel, pulse_us)
    print(f"Sent {pulse_us} µs pulse to PWM channel {channel}")

def disable_one_channel(channel: int):
    rc.pwm_disable(channel)
    print(f"Channel {channel} off.")

def enable_one_channel(channel: int):
    rc.pwm_enable(channel)
    print(f"Channel {channel} on.")

def stop_all_servos():
    rc.pwm_power_off()
    print("All PWM channels powered off")

def angle_to_pulse(angle: float) -> int:
    """
    Converts an angle (in degrees) to a pulse width in microseconds.
    Typical range: 0° -> 1000 µs, 180° -> 2000 µs
    """
    angle = max(0, min(180, angle))  # Clamp between 0 and 180
    return int(1000 + (angle / 180.0) * 1000)

def set_throttle_percent(channel=3, percent=50):
    """
    Converts a % value (0–100) to pulse width and sends it.
    """
    percent = max(0, min(100, percent))
    pulse_width = 1000 + (percent / 100) * 1000  # Range 1000–2000 µs
    set_pwm_width(channel, int(pulse_width))

def sweep_servo(channel: int, start_angle: float, end_angle: float, step: float = 1.0, delay: float = 0.02):
    """
    Gradually sweep a servo between two angles.

    Args:
        channel (int): Servo channel (1–8)
        start_angle (float): Starting angle in degrees
        end_angle (float): Ending angle in degrees
        step (float): Step size in degrees per update
        delay (float): Delay between steps in seconds
    """
    rc.servo_power_rail_en(True)

    try:
        if start_angle < end_angle:
            angle_range = range(int(start_angle), int(end_angle) + 1, int(step))
        else:
            angle_range = range(int(start_angle), int(end_angle) - 1, -int(step))

        for angle in angle_range:
            pulse = angle_to_pulse(angle)
            rc.servo_send_pulse_us(channel, pulse)
            print(f"Angle: {angle}°, Pulse: {pulse} µs")
            time.sleep(delay)

    finally:
        print("Servo sweep complete.")

    # Example usage:
    #sweep_servo(channel=1, start_angle=0, end_angle=180, step=2)