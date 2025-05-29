#ifndef BEAGLEBONE_STUBS_H
#define BEAGLEBONE_STUBS_H

#include <stdbool.h>

// Type definitions
#ifdef _WIN32
typedef long long ssize_t;
#endif

// Process ID type and process control
typedef int pid_t;
int fork(void);
unsigned int sleep(unsigned int seconds);
int usleep(unsigned int usec);

// File descriptor operations
int close(int fd);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
int pipe(int pipefd[2]);

// fcntl definitions
int fcntl(int fd, int cmd, ...);
#define F_GETFL 3
#define F_SETFL 4
#define O_NONBLOCK 04000

// Error codes
extern int errno;
#define EAGAIN 11  /* Try again */

// BeagleBone Blue rc_time functions
void rc_usleep(unsigned int us);

// BeagleBone Blue servo functions
int rc_servo_init(void);
void rc_servo_cleanup(void);
int rc_servo_send_pulse_normalized(int ch, double input);

// Global control flag
extern volatile bool running;

#endif // BEAGLEBONE_STUBS_H 