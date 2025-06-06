#include <stdio.h>
#include <stdlib.h>  // For abs()
#include <stdint.h>
#include "huskylens_api.h"
#include "auto_targeting.h"
#include "main.h"

#ifdef __arm__
// BeagleBone target platform
#include <unistd.h>
#else
// Development platform
#include "../dev_includes/beaglebone_stubs.h"
#endif


// Helper function to get object name from ID
const char* get_object_name(int id) {
    switch(id) {
        case ID_DOG:    return "DOG";
        case ID_CAT:    return "CAT";
        case ID_BOTTLE: return "BOTTLE";
        case ID_PERSON: return "PERSON";
        case ID_CHAIR:  return "CHAIR";
        default:        return "UNKNOWN";
    }
}

/**
 * Find the object with specified ID that's closest to screen center
 * 
 * @param target_id The ID to look for (use ID_* defines)
 * @param target_info Pointer to TargetInfo structure to store results
 * @return 1 if target found, 0 if not found, -1 on error
 */
int find_closest_target(int target_id, TargetInfo *target_info) {
    if (!target_info) {
        printf("Error: Invalid target_info pointer\n");
        return -1;
    }

    // Initialize target info
    target_info->distance = UINT16_MAX;

    // Get objects from HuskyLens
    HuskylensObject objects[MAX_OBJECTS];
    int num_objects = get_huskylens_objects(objects, MAX_OBJECTS);

    if (num_objects < 0) {
        printf("Error: Failed to get objects from HuskyLens\n");
        return -1;  // Error reading from HuskyLens
    }

    int found = 0;
    // Look for closest matching object
    for (int i = 0; i < num_objects; i++) {
        if (objects[i].id == target_id) {
            // Calculate distance from center using integer math
            int dx = objects[i].x - SCREEN_CENTER_X;
            int dy = objects[i].y - SCREEN_CENTER_Y;
            // Using manhattan distance instead of euclidean to avoid floating point
            uint16_t distance = (uint16_t)(abs(dx) + abs(dy));

            // If this is the closest one so far, update target_info
            if (distance < target_info->distance) {
                target_info->x = (uint16_t)objects[i].x;
                // Calculate Y position 1/4 down from the top of the object
                // Instead of subtracting half height (center to top), subtract 1/4 height
                target_info->y = (uint16_t)(objects[i].y - (objects[i].height / 8));
                target_info->distance = distance;
                found = 1;
            }
        }
    }

    if (found) {
        printf("%s found at (%u, %u), distance from center: %u\n", 
               get_object_name(target_id), target_info->x, target_info->y, target_info->distance);
        return 1;
    } else {
        printf("No %s found\n", get_object_name(target_id));
        return 0;
    }
} 

// Helper function to clamp a value between min and max
static int clamp(int value, int min, int max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

int move_to_closest_target(TargetInfo *target_info) {
    if (!target_info) {
        printf("Error: Invalid target_info pointer\n");
        return -1;
    }

    // Calculate offset from center
    int dx = (int)target_info->x - SCREEN_CENTER_X;
    int dy = (int)target_info->y - SCREEN_CENTER_Y;

    // Only move if outside the deadzone
    if (abs(dx) > TARGET_DEADZONE || abs(dy) > TARGET_DEADZONE) {
        On_Target = 0; // Target is not centered
        
        // Calculate angle adjustments based on distance from center
        // Further from center = larger angle adjustment
        int horizontal_adjustment;
        int vertical_adjustment;

        if (mode == AUTOMATIC){
            // Horizontal adjustment
            if (abs(dx) > SCREEN_CENTER_X/2) {
                horizontal_adjustment = 15; // Far from center, move more
            } else if (abs(dx) > SCREEN_CENTER_X/4) {
                horizontal_adjustment = 10; // Between 1/4 and 1/2, move moderately
            }else {
                horizontal_adjustment = 5; // Closer to center, move less
            }

            // Vertical adjustment
            if (abs(dy) > SCREEN_CENTER_Y/2) {
                vertical_adjustment = 15; // Far from center, move more
            }else if(abs(dy) > SCREEN_CENTER_Y/4) {
                vertical_adjustment = 10; // Between 1/4 and 1/2, move moderately
            }else {
                vertical_adjustment = 5; // Closer to center, move less
            }
        }

        if (mode == MANUAL) {
            // Manual mode uses fixed adjustments
            if (target_info->x == 1) {horizontal_adjustment = -2;}
            else if (target_info->x == 2) {horizontal_adjustment = -1;}
            else if (target_info->x == 3) {horizontal_adjustment = 0;}
            else if (target_info->x == 4) {horizontal_adjustment = 1;}
            else if (target_info->x == 5) {horizontal_adjustment = 2;}

            if (target_info->y == 1) {vertical_adjustment = -2;}
            else if (target_info->y == 2) {vertical_adjustment = -1;}
            else if (target_info->y == 3) {vertical_adjustment = 0;}
            else if (target_info->y == 4) {vertical_adjustment = 1;}
            else if (target_info->y == 5) {vertical_adjustment = 2;}
        }

        // Update angles based on target position and clamp to valid ranges
        if (abs(dx) > TARGET_DEADZONE) {
            int old_angle = current_horizontal_angle;
            current_horizontal_angle += (dx > 0 ? -horizontal_adjustment : horizontal_adjustment);
            current_horizontal_angle = clamp(current_horizontal_angle, MIN_HORIZONTAL_ANGLE, MAX_HORIZONTAL_ANGLE);
            printf("Horizontal: dx=%d, adj=%d, angle: %d -> %d\n", 
                   dx, horizontal_adjustment, old_angle, current_horizontal_angle);
        }

        if (abs(dy) > TARGET_DEADZONE) {
            int old_angle = current_vertical_angle;
            // Invert dy because screen coordinates increase downward
            current_vertical_angle += (dy > 0 ? -vertical_adjustment : vertical_adjustment);
            current_vertical_angle = clamp(current_vertical_angle, MIN_VERTICAL_ANGLE, MAX_VERTICAL_ANGLE);
            printf("Vertical: dy=%d, adj=%d, angle: %d -> %d\n", 
                   dy, vertical_adjustment, old_angle, current_vertical_angle);
        }

        // Send the calculated angles through the pipe
        ServoPosition pos = {
            .x = (char)current_horizontal_angle,
            .y = (char)current_vertical_angle
        };
        write(pipefd[1], &pos, sizeof(ServoPosition));
    }
    else {
        On_Target = 1; // Target is centered, shoot
    }

    return 0;
}
