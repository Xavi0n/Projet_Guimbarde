#ifndef BEAGLEBONE_STUBS_H
#define BEAGLEBONE_STUBS_H

#include <stdbool.h>

// Process ID type and process control
typedef int pid_t;
int fork(void);
unsigned int sleep(unsigned int seconds);
int usleep(unsigned int usec);

// BeagleBone Blue rc_time functions
void rc_usleep(unsigned int us);

// BeagleBone Blue servo functions
int rc_servo_init(void);
void rc_servo_cleanup(void);
int rc_servo_send_pulse_normalized(int ch, double input);

// Global control flag
extern volatile bool running;

#endif // BEAGLEBONE_STUBS_H 