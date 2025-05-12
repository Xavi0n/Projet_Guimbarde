from smbus2 import SMBus, i2c_msg
import time

HUSKYLENS_I2C_ADDR = 0x32  # 7-bit address
CMD_REQUEST_BLOCKS = [0x55, 0xAA, 0x11, 0x00, 0x11]  # Request all learned blocks

def request_blocks_i2c(bus_number=2):
    try:
        with SMBus(bus_number) as bus:
            # Send request command
            write = i2c_msg.write(HUSKYLENS_I2C_ADDR, CMD_REQUEST_BLOCKS)
            bus.i2c_rdwr(write)
            time.sleep(0.05)

            # Read up to 64 bytes
            read = i2c_msg.read(HUSKYLENS_I2C_ADDR, 64)
            bus.i2c_rdwr(read)

            response = list(read)
            print("Raw response:", [hex(b) for b in response])
            return response
    except Exception as e:
        print(f"I2C communication error: {e}")
        return None

def parse_huskylens_response(data_bytes):
    """
    Parses HuskyLens object recognition response data.

    Parameters:
        data_bytes (list of int): Raw byte data from HuskyLens.

    Returns:
        List of dictionaries, one per recognized object.
        Also prints each validated frame as a hex string.
    """
    FRAME_HEADER = [0x55, 0xAA]
    FRAME_SIZE = 16
    PAYLOAD_SIZE = 10
    parsed_objects = []

    i = 0
    while i < len(data_bytes) - FRAME_SIZE + 1:
        if data_bytes[i] == FRAME_HEADER[0] and data_bytes[i + 1] == FRAME_HEADER[1]:
            frame = data_bytes[i:i + FRAME_SIZE]

            address = frame[2]
            length = frame[3] + (frame[4] << 8)
            if address != 0x11 or length != PAYLOAD_SIZE:
                i += 1
                continue

            checksum = frame[-1]
            checksum_calc = (sum(frame[2:-1])) & 0xFF
            if checksum != checksum_calc:
                i += 1
                continue

            # Print validated frame as hex
            hex_frame = ' '.join(f'{byte:02X}' for byte in frame)
            print(f'Validated frame: {hex_frame}')

            # Parse payload
            payload = frame[5:15]
            obj_id    = payload[0] + (payload[1] << 8)
            x_center  = payload[2] + (payload[3] << 8)
            y_center  = payload[4] + (payload[5] << 8)
            width     = payload[6] + (payload[7] << 8)
            height    = payload[8] + (payload[9] << 8)

            parsed_objects.append({
                'id': obj_id,
                'x': x_center,
                'y': y_center,
                'width': width,
                'height': height
            })

            i += FRAME_SIZE
        else:
            i += 1

    return parsed_objects