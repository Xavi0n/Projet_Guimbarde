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

#endif

