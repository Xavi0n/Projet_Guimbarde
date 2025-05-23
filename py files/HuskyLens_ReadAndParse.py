# huskylens.py
from smbus import SMBus
import time

HUSKYLENS_I2C_ADDR = 0x32  # 7-bit address
CMD_REQUEST_BLOCKS = [0x55, 0xAA, 0x11, 0x00, 0x11]  # Request all learned blocks

def request_blocks_i2c(I2C_bus_number=1):
    try:
        print("Debug: Opening I2C bus {}".format(I2C_bus_number))
        I2C_bus = SMBus(I2C_bus_number)
        
        # Send request command
        print("Debug: Sending command bytes: {}".format([hex(x) for x in CMD_REQUEST_BLOCKS]))
        I2C_bus.write_i2c_block_data(HUSKYLENS_I2C_ADDR, CMD_REQUEST_BLOCKS[0], CMD_REQUEST_BLOCKS[1:])
        time.sleep(0.05)

        # Read up to 64 bytes
        I2C_response_bytes = []
        try:
            print("Debug: Reading response bytes...")
            for _ in range(64):
                byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                I2C_response_bytes.append(byte)
                print("Debug: Read byte: {}".format(hex(byte)))
        except IOError as e:
            print("Debug: Stopped reading at {} bytes. Reason: {}".format(len(I2C_response_bytes), e))
            pass  # Stop reading when no more data

        I2C_bus.close()
        print("Debug: Total bytes read: {}".format(len(I2C_response_bytes)))
        if I2C_response_bytes:
            print("Debug: First few bytes: {}".format([hex(x) for x in I2C_response_bytes[:8]]))
        return I2C_response_bytes
    except Exception as e:
        print("I2C error: {}".format(e))
        return None

def parse_huskylens_response(I2C_data_bytes):
    if not I2C_data_bytes:
        print("Debug: No data bytes to parse")
        return []
        
    I2C_FRAME_HEADER = [0x55, 0xAA]
    I2C_FRAME_TOTAL_SIZE = 16
    I2C_PAYLOAD_SIZE = 10
    I2C_parsed_objects = []

    print("Debug: Starting to parse {} bytes".format(len(I2C_data_bytes)))
    
    I2C_index = 0
    while I2C_index < len(I2C_data_bytes) - I2C_FRAME_TOTAL_SIZE + 1:
        if I2C_data_bytes[I2C_index] == I2C_FRAME_HEADER[0] and I2C_data_bytes[I2C_index + 1] == I2C_FRAME_HEADER[1]:
            I2C_frame = I2C_data_bytes[I2C_index:I2C_index + I2C_FRAME_TOTAL_SIZE]
            print("Debug: Found frame at index {}: {}".format(I2C_index, [hex(x) for x in I2C_frame]))

            I2C_address = I2C_frame[2]
            I2C_length = I2C_frame[3] + (I2C_frame[4] << 8)
            if I2C_address != 0x11 or I2C_length != I2C_PAYLOAD_SIZE:
                print("Debug: Invalid frame - address: {}, length: {}".format(hex(I2C_address), I2C_length))
                I2C_index += 1
                continue

            I2C_checksum = I2C_frame[-1]
            I2C_checksum_calc = (sum(I2C_frame[2:-1])) & 0xFF
            if I2C_checksum != I2C_checksum_calc:
                print("Debug: Checksum mismatch - expected: {}, got: {}".format(hex(I2C_checksum), hex(I2C_checksum_calc)))
                I2C_index += 1
                continue

            I2C_payload = I2C_frame[5:15]
            I2C_obj_id    = I2C_payload[0] + (I2C_payload[1] << 8)
            I2C_x_center  = I2C_payload[2] + (I2C_payload[3] << 8)
            I2C_y_center  = I2C_payload[4] + (I2C_payload[5] << 8)
            I2C_width     = I2C_payload[6] + (I2C_payload[7] << 8)
            I2C_height    = I2C_payload[8] + (I2C_payload[9] << 8)

            print("Debug: Parsed object - ID: {}, pos: ({}, {}), size: {}x{}".format(
                I2C_obj_id, I2C_x_center, I2C_y_center, I2C_width, I2C_height))

            I2C_parsed_objects.append({
                'id': I2C_obj_id,
                'x': I2C_x_center,
                'y': I2C_y_center,
                'width': I2C_width,
                'height': I2C_height
            })

            I2C_index += I2C_FRAME_TOTAL_SIZE
        else:
            I2C_index += 1

    print("Debug: Parsed {} objects".format(len(I2C_parsed_objects)))
    return I2C_parsed_objects

def get_parsed_huskylens_objects():
    print("Debug: Starting HuskyLens object detection")
    data = request_blocks_i2c()
    if data is None:
        print("Debug: No data received from HuskyLens")
        return []
    return parse_huskylens_response(data)
