#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>

#define ACK 1
#define NACK 0
#define I2C_DEVICE "/dev/i2c-2"  // I2C2 on BeagleBone Blue
#define HL_I2C_ADDRESS 0x32      // 7-bit address

int iRequestObjectDetection()
{
    int file;
    const char *filename = "/dev/i2c-2";
    unsigned char buffer[9];

    // Fill the buffer with the request frame
    buffer[0] = 0x55;     // Start byte
    buffer[1] = 0xAA;     // Header byte
    buffer[2] = 0x11;     // Length LSB
    buffer[3] = 0x00;     // Length MSB
    buffer[4] = 0x36;     // Command byte (request data)
    // No additional data

    // Compute checksum
    unsigned char checksum = 0;
    for (int i = 0; i < 5; ++i) checksum += buffer[i];
    buffer[5] = checksum;

    // Open I2C device
    if ((file = open(filename, O_RDWR)) < 0) {
        perror("I2C open failed");
        return NACK;
    }

    // Set I2C slave address (0x32)
    if (ioctl(file, I2C_SLAVE, 0x32) < 0) {
        perror("I2C ioctl failed");
        close(file);
        return NACK;
    }

    // Write the command frame
    if (write(file, buffer, 6) != 6) {
        perror("I2C write failed");
        close(file);
        return NACK;
    }

    close(file);
    return ACK;
}

int iReadHuskyLensData(unsigned char *buffer, int maxLength)
{
    int file;
    const char *filename = I2C_DEVICE;

    // Open I2C device
    if ((file = open(filename, O_RDWR)) < 0) {
        perror("Failed to open I2C bus");
        return -1;
    }

    // Set I2C slave address
    if (ioctl(file, I2C_SLAVE, HL_I2C_ADDRESS) < 0) {
        perror("Failed to set I2C slave address");
        close(file);
        return -1;
    }

    // Read first 5 bytes to get the header
    unsigned char header[5];
    if (read(file, header, 5) != 5) {
        perror("Failed to read header");
        close(file);
        return -1;
    }

    // Validate start and header bytes
    if (header[0] != 0x55 || header[1] != 0xAA) {
        fprintf(stderr, "Invalid response header: %02X %02X\n", header[0], header[1]);
        close(file);
        return -1;
    }

    int length = header[2] | (header[3] << 8);  // Payload length
    int totalBytes = 5 + length;               // Total frame size including header + payload

    if (totalBytes > maxLength) {
        fprintf(stderr, "Response too long (%d bytes), buffer too small (%d)\n", totalBytes, maxLength);
        close(file);
        return -1;
    }

    // Copy header to the output buffer
    for (int i = 0; i < 5; ++i) buffer[i] = header[i];

    // Read the rest of the frame (payload + checksum)
    int remaining = length;
    if (read(file, buffer + 5, remaining) != remaining) {
        perror("Failed to read payload");
        close(file);
        return -1;
    }

    close(file);
    return totalBytes;  // Return number of bytes read
}
