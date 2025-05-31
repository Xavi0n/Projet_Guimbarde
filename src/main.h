#ifndef MAIN_H
#define MAIN_H

#include <stdbool.h>

// Structure to hold positions for pipe communication
typedef struct {
    char x;
    char y;
} ServoPosition;

// Pipe file descriptors
extern int pipefd[2];

// Global angle variables
extern int current_horizontal_angle;
extern int current_vertical_angle;

// Global control flag
extern volatile bool running;

// Default angles
#define DEFAULT_HORIZONTAL_ANGLE 55  // Default horizontal angle for the turret, looking right in the center
#define DEFAULT_VERTICAL_ANGLE 55    // Default vertical angle for the turret

// Angle limits for turret movement
#define MIN_HORIZONTAL_ANGLE 0
#define MAX_HORIZONTAL_ANGLE 110  // Limited horizontal range
#define MIN_VERTICAL_ANGLE 55    // Limited downward movement
#define MAX_VERTICAL_ANGLE 160   // Limited upward movement

// Screen dimensions and constants
#define SCREEN_CENTER_X 160
#define SCREEN_CENTER_Y 120
#define MAX_OBJECTS 32     
#define TARGET_DEADZONE 3  // Target is considered centered if within this many pixels

// Object ID definitions
#define ID_DOG     1
#define ID_CAT     2
#define ID_BOTTLE  3
#define ID_PERSON  4
#define ID_CHAIR   5

// UART definitions
#define NON_CANONICAL 0
#define CANONICAL 1
#define UART_BAUDRATE 115200
#define UART_TIMEOUT 0.1  // 100 ms timeout for UART operations
#define UART_BUS "/dev/ttyS1"

#define DEFAULT_FLYWHEEL_SPEED 50  // Default speed for the flywheel 0-100
#define DEFAULT_FAN_SPEED 50       // Default speed for the fan 0-100       
#define DEFAULT_RECOIL_SPEED 50    // Default speed for the recoil 0-100
#define DEFAULT_AGITATOR_SPEED 50  // Default speed for the agitator 0-100

#endif

