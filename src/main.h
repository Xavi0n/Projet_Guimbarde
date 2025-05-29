#ifndef MAIN_H
#define MAIN_H

#include <stdbool.h>

#define DEFAULT_VERTICAL_ANGLE 10       // Default vertical angle for the turret, looking fully down
#define DEFAULT_HORIZONTAL_ANGLE 50     // Default horizontal angle for the turret, looking right in the center

// Current angles of the turret
extern int current_horizontal_angle;
extern int current_vertical_angle;

// Global control flag
extern volatile bool running;

#endif

