#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LEN 128
#define MAX_BLOCKS 32

typedef struct {
    int x;
    int y;
    int width;
    int height;
    int ID;
} Block;


int main() {
    Block blocks[MAX_BLOCKS];
    int blockCount = 0;

    FILE *fp = popen("python3 HuskyLens_ReadAndParse.py", "r");
    if (!fp) {
        perror("Failed to run HuskyLens_ReadAndParse.py");
        return 1;
    }

    char line[MAX_LINE_LEN];
    while (fgets(line, sizeof(line), fp) && blockCount < MAX_BLOCKS) {
        Block b;
        if (sscanf(line, "%d %d %d %d %d", &b.x, &b.y, &b.width, &b.height, &b.ID) == 5) {
            blocks[blockCount++] = b;
        }
    }

    pclose(fp);

    // Example: print blocks
    for (int i = 0; i < blockCount; ++i) {
        printf("Block %d: ID=%d X=%d Y=%d Width=%d Height=%d\n",
               i, blocks[i].ID, blocks[i].x, blocks[i].y, blocks[i].width, blocks[i].height);
    }

    return 0;
}

