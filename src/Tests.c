#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "huskylens_api.h"

// Colors for test output
#define RED     "\x1b[31m"
#define GREEN   "\x1b[32m"
#define YELLOW  "\x1b[33m"
#define RESET   "\x1b[0m"

// Test status tracking
static int tests_run = 0;
static int tests_passed = 0;

// Test helper macros
#define ASSERT(message, test) do { \
    tests_run++; \
    if (test) { \
        tests_passed++; \
        printf(GREEN "✓ %s\n" RESET, message); \
    } else { \
        printf(RED "✗ %s\n" RESET, message); \
    } \
} while (0)

// Test functions
void test_null_pointer() {
    printf("\nTesting NULL pointer handling:\n");
    int result = get_huskylens_objects(NULL, 5);
    ASSERT("NULL pointer returns -1", result == -1);
}

void test_zero_max_objects() {
    printf("\nTesting zero max objects:\n");
    HuskylensObject objs[1];
    int result = get_huskylens_objects(objs, 0);
    ASSERT("Zero max_objects returns 0", result == 0);
}

void test_basic_functionality() {
    printf("\nTesting basic functionality:\n");
    HuskylensObject objs[10];
    int result = get_huskylens_objects(objs, 10);
    
    ASSERT("Function returns non-negative value", result >= 0);
    
    if (result > 0) {
        ASSERT("First object has valid coordinates", 
               objs[0].x >= 0 && objs[0].x < 320 && // HuskyLens camera is 320x240
               objs[0].y >= 0 && objs[0].y < 240);
        
        ASSERT("First object has valid dimensions",
               objs[0].width > 0 && objs[0].height > 0);
    }
}

void test_multiple_calls() {
    printf("\nTesting multiple consecutive calls:\n");
    HuskylensObject objs[5];
    int first_call = get_huskylens_objects(objs, 5);
    sleep(1); // Wait a second between calls
    int second_call = get_huskylens_objects(objs, 5);
    
    ASSERT("Multiple calls succeed", 
           first_call >= 0 && second_call >= 0);
}

void test_object_count_consistency() {
    printf("\nTesting object count consistency:\n");
    
    // Test with different array sizes to verify count consistency
    HuskylensObject small_array[3];
    HuskylensObject large_array[50];
    
    // Get objects with small array
    int small_count = get_huskylens_objects(small_array, 3);
    if (small_count < 0) {
        printf(RED "Error: Failed to get objects for small array\n" RESET);
        return;
    }
    
    // Get objects with large array immediately after
    int large_count = get_huskylens_objects(large_array, 50);
    if (large_count < 0) {
        printf(RED "Error: Failed to get objects for large array\n" RESET);
        return;
    }
    
    // If small array was filled completely, we expect large array might have more objects
    if (small_count == 3 && large_count > small_count) {
        printf(YELLOW "Note: Found %d objects total, small array was limited to %d\n" RESET, 
               large_count, small_count);
        ASSERT("Object count properly limited by array size", true);
    } else {
        // If small array wasn't filled, counts should match
        ASSERT("Object counts are consistent between different array sizes", 
               small_count == large_count);
    }
    
    // Verify all objects in the larger array are valid
    for (int i = 0; i < large_count; i++) {
        if (large_array[i].x < 0 || large_array[i].x >= 320 ||
            large_array[i].y < 0 || large_array[i].y >= 240 ||
            large_array[i].width <= 0 || large_array[i].height <= 0) {
            printf(RED "Invalid object data at index %d\n" RESET, i);
            ASSERT("All objects have valid data", false);
            return;
        }
    }
    ASSERT("All objects have valid data", true);
}

// Main test runner
int main() {
    printf("=== BeagleBone Blue HuskyLens API Tests ===\n");
    
    // Run all tests
    test_null_pointer();
    test_zero_max_objects();
    test_basic_functionality();
    test_multiple_calls();
    test_object_count_consistency();
    
    // Print summary
    printf("\n=== Test Summary ===\n");
    printf("Tests run: %d\n", tests_run);
    printf("Tests passed: %d\n", tests_passed);
    printf("Success rate: %.2f%%\n", (float)tests_passed/tests_run * 100);
    
    return (tests_passed == tests_run) ? 0 : 1;
}
