#include <stdio.h>
#include <stdbool.h>
#ifdef __arm__
#include <unistd.h>
#include <rc/time.h>
#include <rc/servo.h>
#include <errno.h>
#include <sys/types.h>
#include <fcntl.h>
#else
#include "../dev_includes/beaglebone_stubs.h"  // All BeagleBone and system stubs
#endif
#include "main.h"
#include "auto_targeting.h"
#include "ServoAdjust.h"

// Initialize turret angles with default values
int current_horizontal_angle = DEFAULT_HORIZONTAL_ANGLE;
int current_vertical_angle = DEFAULT_VERTICAL_ANGLE;

int pipefd[2];

// Global control flag
volatile bool running = true;

int main() {
    printf("Starting turret control system...\n");

    rc_usleep(50000);
	rc_servo_cleanup();
    
    // initialize PRU
    printf("Initialising PRU\n");
	if(rc_servo_init()) return -1;
    
    // Create pipe
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return 1;
    }
    
    pid_t pid = fork();
    
    if (pid < 0) {
        // Fork failed
        printf("Error: Failed to fork process\n");
        return -1;
    }
    else if (pid == 0) {
        // Child process - only handles servo movements
        close(pipefd[1]); // Close write end in child
        
        // Set non-blocking flag for read end
        int flags = fcntl(pipefd[0], F_GETFL);
        if (flags == -1) {
            perror("fcntl get flags failed");
            return -1;
        }
        if (fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK) == -1) {
            perror("fcntl set non-blocking failed");
            return -1;
        }
        
        ServoPosition pos;
        while(running) {
            // Try to read from pipe (non-blocking)
            ssize_t bytes_read = read(pipefd[0], &pos, sizeof(ServoPosition));
            if (bytes_read > 0) {
                // Call Servo_Movements with the received positions
                if (Servo_Movements(pos.x, pos.y) != 0) {
                    printf("Error: Failed to move servos\n");
                }
            } else if (bytes_read == -1 && errno != EAGAIN) {
                // EAGAIN means no data available (expected for non-blocking)
                // Any other error is unexpected
                perror("read error");
            }
            //rc_usleep(20000);  // 20ms delay
        }
        
        close(pipefd[0]);
        return 0;
    }
    else {
        // Parent process - handles target detection
        close(pipefd[0]); // Close read end in parent
        
        TargetInfo current_target;
        while(running) {
            // Try to find and track a bottle
            if (find_closest_target(ID_CHAIR, &current_target) == 1) {
                // Let move_to_closest_target handle angle calculation and pipe communication
                move_to_closest_target(&current_target);
            }
            //rc_usleep(20000);  // 20ms delay for target detection
        }
        
        close(pipefd[1]);
    }

    return 0;
}


