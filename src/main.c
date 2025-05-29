#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#ifdef __arm__
#include <unistd.h>
#include <rc/time.h>
#include <rc/servo.h>
#else
#include "../dev_includes/beaglebone_stubs.h"  // All BeagleBone and system stubs
#endif
#include "main.h"
#include "auto_targeting.h"
#include "ServoAdjust.h"

// Initialize turret angles with default values
int current_horizontal_angle = DEFAULT_HORIZONTAL_ANGLE;
int current_vertical_angle = DEFAULT_VERTICAL_ANGLE;

// Global control flag
volatile bool running = true;

// Shared target info between processes
static TargetInfo current_target;
static volatile bool has_new_target = false;

int main() {
    printf("Starting turret control system...\n");

    // initialize PRU
    printf("Initialising PRU\n");
	if(rc_servo_init()) return -1;

    pid_t pid = fork();
    
    if (pid < 0) {
        // Fork failed
        printf("Error: Failed to fork process\n");
        return -1;
    }
    else if (pid == 0) {
        // Child process - handles servo movements
        if (Servo_Movements() != 0) {
            printf("Error: Failed to initialize servo movements\n");
            return -1;
        }
        return 0;  // Child process ends here if Servo_Movements returns
    }
    else {
        // Parent process - handles target detection
        while(running) {
            // Try to find and track a person
            if (find_closest_target(ID_PERSON, &current_target) == 1) {
                // Move turret to track target
                if (move_to_closest_target(&current_target) != 0) {
                    printf("Error: Failed to move turret\n");
                }
            }
            rc_usleep(20000);  // 20ms delay for target detection
        }
    }

    return 0;
}


