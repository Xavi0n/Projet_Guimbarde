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

// Global Flags
extern unsigned char On_Target; // Flag to indicate if the target is centered

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

// Mode definitions
#define AUTOMATIC 0
#define MANUAL 1

// UART definitions
#define NON_CANONICAL 0
#define CANONICAL 1
#define UART_BAUDRATE 19200
#define UART_TIMEOUT 0.1  // 100 ms timeout for UART operations
#define UART_BUS 1

#define DONT_SHOOT 0    // Do not shoot command
#define SHOOT 1         // Shoot command

#endif

