# huskylens.py
from smbus import SMBus
import time

HUSKYLENS_I2C_ADDR = 0x32  # 7-bit address

# HuskyLens Commands
COMMAND_HEADER = 0x55
COMMAND_REQUEST_KNOCK = 0x2C
COMMAND_REQUEST_BLOCKS_LEARNED = 0x25

def request_blocks_i2c(I2C_bus_number=1):
    try:
        print("Debug: Opening I2C bus {}".format(I2C_bus_number))
        I2C_bus = SMBus(I2C_bus_number)
        
        try:
            # Try a simple read first to check connection
            print("Debug: Testing basic I2C read...")
            test_byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
            print("Debug: Basic read test result: {}".format(hex(test_byte)))
            
            # Small delay
            time.sleep(0.1)
            
            # Try writing a single byte
            print("Debug: Testing basic I2C write...")
            I2C_bus.write_byte(HUSKYLENS_I2C_ADDR, COMMAND_HEADER)
            time.sleep(0.1)
            
            # Now try the knock command
            print("Debug: Sending simplified knock command...")
            # Send header and command only
            I2C_bus.write_byte_data(HUSKYLENS_I2C_ADDR, COMMAND_HEADER, COMMAND_REQUEST_KNOCK)
            time.sleep(0.1)
            
            # Read response
            print("Debug: Reading knock response one byte at a time...")
            response = []
            for i in range(5):
                byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                response.append(byte)
                print("Debug: Read byte {}: {}".format(i, hex(byte)))
                time.sleep(0.01)
            
            if any(byte != 0 for byte in response):
                print("Debug: Got non-zero response!")
                
                # If we got a response, try requesting learned blocks
                print("Debug: Sending request for learned blocks...")
                cmd = [COMMAND_HEADER, COMMAND_HEADER, COMMAND_REQUEST_BLOCKS_LEARNED, 0x00, 0x00]
                # Send command one byte at a time
                for byte in cmd:
                    I2C_bus.write_byte(HUSKYLENS_I2C_ADDR, byte)
                    time.sleep(0.01)
                
                # Read response
                print("Debug: Reading block data response...")
                block_data = []
                for i in range(20):  # Read more bytes to see what we get
                    try:
                        byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                        block_data.append(byte)
                        print("Debug: Block data byte {}: {}".format(i, hex(byte)))
                    except IOError as e:
                        print("Debug: Stopped reading at byte {}: {}".format(i, e))
                        break
                    time.sleep(0.01)
                
                return block_data
            else:
                print("Debug: Got all zeros in response")
                return None
                
        except IOError as e:
            print("Debug: I2C communication error: {}".format(e))
            return None
            
    except Exception as e:
        print("I2C error: {}".format(e))
        return None
    finally:
        if 'I2C_bus' in locals():
            I2C_bus.close()
            print("Debug: I2C bus closed")

def parse_huskylens_response(data):
    if not data:
        print("Debug: No data to parse")
        return []
        
    print("Debug: Raw data received: {}".format([hex(x) for x in data]))
    objects = []
    
    # Look for header pattern
    for i in range(len(data) - 10):
        if data[i] == COMMAND_HEADER and data[i+1] == COMMAND_HEADER:
            try:
                obj_id = data[i+5] + (data[i+6] << 8)
                x = data[i+7] + (data[i+8] << 8)
                y = data[i+9] + (data[i+10] << 8)
                width = data[i+11] + (data[i+12] << 8)
                height = data[i+13] + (data[i+14] << 8)
                
                print("Debug: Found potential object - ID: {}, pos: ({}, {}), size: {}x{}".format(
                    obj_id, x, y, width, height))
                    
                if 0 <= x < 320 and 0 <= y < 240 and width > 0 and height > 0:
                    objects.append({
                        'id': obj_id,
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height
                    })
            except IndexError:
                break
    
    print("Debug: Found {} valid objects".format(len(objects)))
    return objects

def get_parsed_huskylens_objects():
    print("Debug: Starting HuskyLens object detection with simplified protocol")
    data = request_blocks_i2c()
    if data is None:
        print("Debug: No data received from HuskyLens")
        return []
    return parse_huskylens_response(data)
