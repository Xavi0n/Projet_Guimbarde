#include <stdio.h>
#include "auto_targeting.h"

#define MAX_OBJECTS 32

int main() {
    printf("Testing HuskyLens Auto Targeting System...\n\n");
    
    // Create target info structure
    TargetInfo target;
    int result;
    
    // Test finding each object type
    printf("Looking for DOG...\n");
    result = find_closest_target(ID_DOG, &target);
    printf("\n");
    
    printf("Looking for CAT...\n");
    result = find_closest_target(ID_CAT, &target);
    printf("\n");
    
    printf("Looking for BOTTLE...\n");
    result = find_closest_target(ID_BOTTLE, &target);
    printf("\n");
    
    printf("Looking for PERSON...\n");
    result = find_closest_target(ID_PERSON, &target);
    printf("\n");
    
    printf("Looking for CHAIR...\n");
    result = find_closest_target(ID_CHAIR, &target);
    printf("\n");
    
    return 0;
} 