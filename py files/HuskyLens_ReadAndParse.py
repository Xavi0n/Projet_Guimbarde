# huskylens.py
from smbus2 import SMBus, i2c_msg
import time

HUSKYLENS_I2C_ADDR = 0x32  # 7-bit address
CMD_REQUEST_BLOCKS = [0x55, 0xAA, 0x11, 0x00, 0x11]  # Request all learned blocks

def request_blocks_i2c(I2C_bus_number=2):
    try:
        with SMBus(I2C_bus_number) as I2C_bus:
            # Send request command
            I2C_write_msg = i2c_msg.write(HUSKYLENS_I2C_ADDR, CMD_REQUEST_BLOCKS)
            I2C_bus.i2c_rdwr(I2C_write_msg)
            time.sleep(0.05)

            # Read up to 64 bytes
            I2C_read_msg = i2c_msg.read(HUSKYLENS_I2C_ADDR, 64)
            I2C_bus.i2c_rdwr(I2C_read_msg)

            I2C_response_bytes = list(I2C_read_msg)
            return I2C_response_bytes
    except Exception as e:
        print("I2C error: {}".format(e))
        return None

def parse_huskylens_response(I2C_data_bytes):
    I2C_FRAME_HEADER = [0x55, 0xAA]
    I2C_FRAME_TOTAL_SIZE = 16
    I2C_PAYLOAD_SIZE = 10
    I2C_parsed_objects = []

    I2C_index = 0
    while I2C_index < len(I2C_data_bytes) - I2C_FRAME_TOTAL_SIZE + 1:
        if I2C_data_bytes[I2C_index] == I2C_FRAME_HEADER[0] and I2C_data_bytes[I2C_index + 1] == I2C_FRAME_HEADER[1]:
            I2C_frame = I2C_data_bytes[I2C_index:I2C_index + I2C_FRAME_TOTAL_SIZE]

            I2C_address = I2C_frame[2]
            I2C_length = I2C_frame[3] + (I2C_frame[4] << 8)
            if I2C_address != 0x11 or I2C_length != I2C_PAYLOAD_SIZE:
                I2C_index += 1
                continue

            I2C_checksum = I2C_frame[-1]
            I2C_checksum_calc = (sum(I2C_frame[2:-1])) & 0xFF
            if I2C_checksum != I2C_checksum_calc:
                I2C_index += 1
                continue

            I2C_payload = I2C_frame[5:15]
            I2C_obj_id    = I2C_payload[0] + (I2C_payload[1] << 8)
            I2C_x_center  = I2C_payload[2] + (I2C_payload[3] << 8)
            I2C_y_center  = I2C_payload[4] + (I2C_payload[5] << 8)
            I2C_width     = I2C_payload[6] + (I2C_payload[7] << 8)
            I2C_height    = I2C_payload[8] + (I2C_payload[9] << 8)

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

    return I2C_parsed_objects

def get_parsed_huskylens_objects():
    data = request_blocks_i2c()
    if data is None:
        return []
    return parse_huskylens_response(data)
