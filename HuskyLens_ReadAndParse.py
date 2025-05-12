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
