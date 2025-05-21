#ifndef HUSKYLENS_API_H
#define HUSKYLENS_API_H

typedef struct {
    long id;
    long x;
    long y;
    long width;
    long height;
} HuskylensObject;

// Returns number of detected objects, or -1 on error
// objs: pointer to array of HuskylensObject with space for max_objects
int get_huskylens_objects(HuskylensObject *objs, int max_objects);

#endif // HUSKYLENS_API_H
