import spidev
import threading

def spi_listener(bus=1, device=0, speed=500000):
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = speed
    spi.mode = 0  # SPI mode 0

    def read_frame():
        buffer = []

        while True:
            byte = spi.readbytes(1)[0]

            # Sync to start of frame: 0x55, then 0xAA
            if len(buffer) == 0 and byte == 0x55:
                buffer.append(byte)
            elif len(buffer) == 1:
                if byte == 0xAA:
                    buffer.append(byte)
                else:
                    buffer = []  # Restart sync
            elif 2 <= len(buffer) < 9:
                buffer.append(byte)

            if len(buffer) == 9:
                # Extract payload (excluding headers)
                payload = buffer[2:8]
                received_checksum = buffer[8]
                calculated_checksum = sum(payload) & 0xFF

                if received_checksum == calculated_checksum:
                    mode, x, y, button, fan, strength = payload
                    print(f"[SPI Frame] Mode: {mode}, X: {x}, Y: {y}, Button: {button}, Fan: {fan}, Strength: {strength}")
                else:
                    print("[SPI Frame] Invalid checksum")

                buffer = []  # Reset buffer for next frame

    # Run the read loop
    read_frame()
