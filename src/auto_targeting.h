#ifndef AUTO_TARGETING_H
#define AUTO_TARGETING_H

#include <stdint.h>  // For uint16_t

// Screen dimensions and constants
#define SCREEN_CENTER_X 160
#define SCREEN_CENTER_Y 120
#define MAX_OBJECTS 32     
#define TARGET_DEADZONE 2  // Target is considered centered if within this many pixels

// Object ID definitions
#define ID_DOG     1
#define ID_CAT     2
#define ID_BOTTLE  3
#define ID_PERSON  4
#define ID_CHAIR   5

// Angle limits for turret movement
#define MIN_HORIZONTAL_ANGLE 0
#define MAX_HORIZONTAL_ANGLE 110
#define MIN_VERTICAL_ANGLE 10
#define MAX_VERTICAL_ANGLE 160

// Structure to hold targeting information
typedef struct {
    uint16_t x;           // x position of target (0-320)
    uint16_t y;           // y position of target (0-240)
    uint16_t distance;    // distance from center in pixels
} TargetInfo;

/**
 * Get the name of an object based on its ID
 * 
 * @param id The object ID (use ID_* defines)
 * @return String name of the object
 */
const char* get_object_name(int id);

/**
 * Find the object with specified ID that's closest to screen center
 * 
 * @param target_id The ID to look for (use ID_* defines)
 * @param target_info Pointer to TargetInfo structure to store results
 * @return 1 if target found, 0 if not found, -1 on error
 */
int find_closest_target(int target_id, TargetInfo *target_info);

/**
 * Move the turret to track the specified target
 * 
 * @param target_info Pointer to TargetInfo structure with target position
 * @return 0 on success, -1 on error
 */
int move_to_closest_target(TargetInfo *target_info);

#endif // AUTO_TARGETING_H 