#include <stdio.h>
#include "huskylens_api.h"

#define MAX_OBJECTS 32

int main() {
    // Create an array to store the detected objects
    HuskylensObject objects[MAX_OBJECTS];
    
    printf("Testing HuskyLens API...\n");
    
    // Get objects from HuskyLens
    int num_objects = get_huskylens_objects(objects, MAX_OBJECTS);
    
    // Check for errors
    if (num_objects < 0) {
        printf("Error: Failed to get objects from HuskyLens\n");
        return 1;
    }
    
    // Print the results
    printf("Found %d objects:\n", num_objects);
    for (int i = 0; i < num_objects; i++) {
        printf("Object %d:\n", i + 1);
        printf("  ID: %ld\n", objects[i].id);
        printf("  Position: (%ld, %ld)\n", objects[i].x, objects[i].y);
        printf("  Size: %ld x %ld\n", objects[i].width, objects[i].height);
        printf("\n");
    }
    
    return 0;
} 