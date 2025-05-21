from PWM import set_pwm_width, angle_to_pulse, init_PWM, set_throttle_percent, disable_one_channel, enable_one_channel
from Command_ReadAndParse import SPI_listener
import time

def TurretStartup():
    init_PWM()

    # Set all servos to middle position of turret
    set_pwm_width(1, angle_to_pulse(135))  # X-axis servo in middle position
    set_pwm_width(2, angle_to_pulse(135))  # Y-axis servo 1 in middle position
    set_pwm_width(3, angle_to_pulse(135))  # Y-axis servo 2 in middle position

    # Init 7-segment display

    # Init ampermeter

    # Set default values for fan and shooting strength
    disable_one_channel(3)  # Disable fan (channel 3) before setting default speed
    disable_one_channel(5)  # Disable shooting (channel 5) before setting default strength
    set_throttle_percent(3, 50)  # Init fan speed to 50% (channel 3)
    set_throttle_percent(5, 50)  # Init shooting strength to 50% (channel 5)

    # Flywheel test run
    enable_one_channel(5)  # Enable shooting (channel 5)
    time.sleep(1.5)  # Wait for shooting to stabilize
    disable_one_channel(5)  # Disable shooting (channel 5)

    # Fan test run
    enable_one_channel(3)  # Enable fan (channel 3)
    time.sleep(1.5)  # Wait for fan to stabilize
    disable_one_channel(3)  # Disable fan (channel 3)

    #Test flash neopixels

    # Look around power on routine
    set_pwm_width(1, angle_to_pulse(0))     # X-axis servo all the way to the left
    time.sleep(1)                           # Wait for servo to reach position
    set_pwm_width(1, angle_to_pulse(270))   # X-axis servo all the way to the right
    time.sleep(1)                           # Wait for servo to reach position
    set_pwm_width(1, angle_to_pulse(135))   # X-axis servo in middle position
    time.sleep(1)                           # Wait for servo to reach position

    set_pwm_width(2, angle_to_pulse(0))     # Y1-axis servo looking down
    set_pwm_width(3, angle_to_pulse(270))   # Y2-axis servo looking down
    time.sleep(1)                           # Wait for servo to reach position

    # Start SPI listener and wait for remote signal
    if (SPI_listener):
        set_pwm_width(1, angle_to_pulse(135))   # X-axis servo in middle position
        set_pwm_width(2, angle_to_pulse(135))   # Y1-axis servo in middle position
        set_pwm_width(3, angle_to_pulse(135))   # Y2-axis servo in middle position
        print("Initialisation complete. Ready to receive commands.")