#include "ServoAdjust.h"
#ifdef __arm__
#include <unistd.h>
#include <rc/time.h>
#include "ServoAdjust.h"
#ifdef __arm__
#include <unistd.h>
#include <rc/time.h>
#include <rc/servo.h>
#include <errno.h>
#include <sys/types.h>
#include <fcntl.h>
#include <rc/uart.h>
#else
#include "../dev_includes/beaglebone_stubs.h"  // All BeagleBone and system stubs
#endif

// Initialize turret angles with default values
int current_horizontal_angle = DEFAULT_HORIZONTAL_ANGLE;
int current_vertical_angle = DEFAULT_VERTICAL_ANGLE;

unsigned char sent_uart_data[2] = {'$', DONT_SHOOT};                  // Buffer for outgoing UART data
unsigned char received_uart_data[4] = {0x00, 0x00, 0x00, 0x00};       // Buffer for incoming UART data

unsigned char mode = AUTOMATIC;
unsigned char On_Target = 0; // Flag to indicate if the target is centered

int pipefd[2];

// Global control flag
volatile bool running = true;

int main() {
    printf("Starting turret control system...\n");

    rc_usleep(50000);
    rc_servo_cleanup();

    // Initialize PRU
    printf("Initialising PRU\n");
    if (rc_servo_init()) return -1;

    // Initialize UART
    printf("Initialising UART\n");
    if (rc_uart_init(UART_BUS, UART_BAUDRATE, 0.1, NON_CANONICAL, 1, 0) < 0) {
        printf("Error: Failed to initialize UART\n");
        return -1;
    }

    // Calculate checksum
    unsigned char checksum = 0;
    for (int i = 2; i < sizeof(sent_uart_data) - 1; i++) {
        checksum += sent_uart_data[i];
    }
    sent_uart_data[sizeof(sent_uart_data) - 1] = checksum; // Set checksum byte

    // Send initial settings over UART
    rc_uart_write(UART_BUS, *sent_uart_data, sizeof(sent_uart_data)); // Send initial settings

    // Create pipe
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();

    if (pid < 0) {
        // Fork failed
        printf("Error: Failed to fork process\n");
        return -1;
    }
    else if (pid == 0) {
        // Child process - only handles servo movements
        close(pipefd[1]); // Close write end in child

        // Set non-blocking flag for read end
        int flags = fcntl(pipefd[0], F_GETFL);
        if (flags == -1) {
            perror("fcntl get flags failed");
            return -1;
        }
        if (fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK) == -1) {
            perror("fcntl set non-blocking failed");
            return -1;
        }

        ServoPosition pos;
        while (running) {
            // Try to read from pipe (non-blocking)
            ssize_t bytes_read = read(pipefd[0], &pos, sizeof(ServoPosition));
            if (bytes_read > 0) {
                // Call Servo_Movements with the received positions
                if (Servo_Movements(pos.x, pos.y) != 0) {
                    printf("Error: Failed to move servos\n");
                }
            } else if (bytes_read == -1 && errno != EAGAIN) {
                // EAGAIN means no data available (expected for non-blocking)
                // Any other error is unexpected
                perror("read error");
            }
        }

        close(pipefd[0]);
        return 0;
    }
    else {
        // Parent process - handles target detection
        close(pipefd[0]); // Close read end in parent

        TargetInfo current_target;
        while (running) {
            if (rc_uart_bytes_available(UART_BUS) == 4) {
                // Read the received data
                rc_uart_read(UART_BUS, &received_uart_data, 4);
                printf("Received UART data: %c%c%c%c\n", received_uart_data[0], received_uart_data[1], received_uart_data[2], received_uart_data[3]);
                if (received_uart_data[0] == '$') {
                    if (received_uart_data[1] == 'M') {
                        mode = MANUAL;
                    } else if (received_uart_data[1] == 'A') {
                        mode = AUTOMATIC;
                    }

                    if (mode == AUTOMATIC) {
                        if (On_Target == 1) {
                            On_Target = 0; // Reset the flag
                            sent_uart_data[1] = SHOOT; // Set shoot command
                            rc_uart_write(UART_BUS, sent_uart_data, sizeof(sent_uart_data)); // Send shoot command
                            sent_uart_data[1] = DONT_SHOOT; // Reset to no shoot command
                        }
                        if (find_closest_target(ID_PERSON, &current_target) == 1) {
                            // Let move_to_closest_target handle angle calculation and pipe communication
                            move_to_closest_target(&current_target);
                        }
                    }
                    else { // MANUAL mode
                        unsigned char tempHorizontal = received_uart_data[2];
                        unsigned char tempVertical = received_uart_data[3];

                        if (tempHorizontal == '5') { current_target.x = 320; }
                        else if (tempHorizontal == '4') { current_target.x = 180; }
                        else if (tempHorizontal == '3') { current_target.x = 160; }
                        else if (tempHorizontal == '2') { current_target.x = 140; }
                        else if (tempHorizontal == '1') { current_target.x = 0; }
                        move_to_closest_target(&current_target);
                    }
                }
            }
        }

        close(pipefd[1]);
        return 0;
    }
}

