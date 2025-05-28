#include <stdio.h>
#include <stdlib.h>  // For abs()
#include <stdint.h>
#include "huskylens_api.h"
#include "auto_targeting.h"

#define SCREEN_CENTER_X 160
#define SCREEN_CENTER_Y 120
#define MAX_OBJECTS 32

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
                target_info->y = (uint16_t)objects[i].y;
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