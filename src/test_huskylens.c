#include <stdio.h>
#include "auto_targeting.h"

#define MAX_OBJECTS 32

int main() {
    printf("Testing HuskyLens Auto Targeting System...\n\n");
    
    // Create target info structure
    TargetInfo target;
    
    // Test finding each object type
    printf("Looking for DOG...\n");
    find_closest_target(ID_DOG, &target);
    printf("\n");
    
    printf("Looking for CAT...\n");
    find_closest_target(ID_CAT, &target);
    printf("\n");
    
    printf("Looking for BOTTLE...\n");
    find_closest_target(ID_BOTTLE, &target);
    printf("\n");
    
    printf("Looking for PERSON...\n");
    find_closest_target(ID_PERSON, &target);
    printf("\n");
    
    printf("Looking for CHAIR...\n");
    find_closest_target(ID_CHAIR, &target);
    printf("\n");
    
    return 0;
} 