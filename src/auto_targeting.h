#ifndef AUTO_TARGETING_H
#define AUTO_TARGETING_H

#include <stdint.h>  // For uint16_t

// Object ID definitions
#define ID_DOG     1
#define ID_CAT     2
#define ID_BOTTLE  3
#define ID_PERSON  4
#define ID_CHAIR   5

// Structure to hold targeting information
typedef struct {
    uint16_t x;           // x position of target (0-320)
    uint16_t y;           // y position of target (0-240)
    uint16_t distance;    // distance from center in pixels
} TargetInfo;

/**
 * Find the object with specified ID that's closest to screen center
 * 
 * @param target_id The ID to look for (use ID_* defines)
 * @param target_info Pointer to TargetInfo structure to store results
 * @return 1 if target found, 0 if not found, -1 on error
 */
int find_closest_target(int target_id, TargetInfo *target_info);

#endif // AUTO_TARGETING_H 