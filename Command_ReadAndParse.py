import spidev
from multiprocessing import Pipe

def SPI_listener(SPI_conn, SPI_bus=1, SPI_device=0, SPI_speed=500000):
    SPI_device_handle = spidev.SpiDev()
    SPI_device_handle.open(SPI_bus, SPI_device)
    SPI_device_handle.max_speed_hz = SPI_speed
    SPI_device_handle.mode = 0  # SPI mode 0

    SPI_buffer = []

    while True:
        SPI_byte = SPI_device_handle.readbytes(1)[0]

        # Sync to frame header: 0x55, 0xAA
        if len(SPI_buffer) == 0 and SPI_byte == 0x55:
            SPI_buffer.append(SPI_byte)
        elif len(SPI_buffer) == 1:
            if SPI_byte == 0xAA:
                SPI_buffer.append(SPI_byte)
            else:
                SPI_buffer = []
        elif 2 <= len(SPI_buffer) < 8:
            SPI_buffer.append(SPI_byte)

        if len(SPI_buffer) == 8:
            SPI_payload = SPI_buffer[2:7]  # Now 5 bytes
            SPI_received_checksum = SPI_buffer[7]
            SPI_calculated_checksum = sum(SPI_payload) & 0xFF

            if SPI_received_checksum == SPI_calculated_checksum:
                SPI_frame_dict = {
                    'x': SPI_payload[0],
                    'y': SPI_payload[1],
                    'button': SPI_payload[2],
                    'fan_speed': SPI_payload[3],
                    'shoot_strength': SPI_payload[4],
                    'checksum': SPI_received_checksum
                }

                SPI_conn.send(SPI_frame_dict)  # Send to main process/thread

            SPI_buffer = []
