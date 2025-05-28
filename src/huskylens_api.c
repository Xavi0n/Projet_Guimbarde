#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "huskylens_api.h"

#define MAX_LINE_LEN 256
#define PYTHON_SCRIPT_PATH "py files/HuskyLens_ReadAndParse.py"  // Relative path

// Declare popen and pclose for Linux systems
FILE *popen(const char *command, const char *type);
int pclose(FILE *stream);

int get_huskylens_objects(HuskylensObject *objs, int max_objects) {
    if (!objs || max_objects <= 0) {
        return -1;
    }

    // Build command with error redirection
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "python3.7 \"%s\" 2>&1", PYTHON_SCRIPT_PATH);
    
    FILE *fp = popen(cmd, "r");
    if (!fp) {
        perror("Failed to run HuskyLens_ReadAndParse.py");
        return -1;
    }

    char line[MAX_LINE_LEN];
    int count = 0;

    // Read each line from the Python script output
    while (fgets(line, sizeof(line), fp) && count < max_objects) {
        // Remove newline if present
        line[strcspn(line, "\n")] = 0;

        // Try to parse the line as object data
        long id, x, y, width, height;
        if (sscanf(line, "%ld %ld %ld %ld %ld", &x, &y, &width, &height, &id) == 5) {
            objs[count].id = id;
            objs[count].x = x;
            objs[count].y = y;
            objs[count].width = width;
            objs[count].height = height;
            count++;
        }
        // Ignore lines that don't match our format (debug/status messages)
    }

    int status = pclose(fp);
    if (status == -1) {
        perror("Error closing Python script pipe");
        return -1;
    }

    return count;
}

