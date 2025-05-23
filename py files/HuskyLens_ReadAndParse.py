# huskylens.py
from smbus import SMBus
import time

HUSKYLENS_I2C_ADDR = 0x32

# Protocol Headers and Commands
COMMAND_HEADER = 0x55
COMMAND_END = 0x54
COMMAND_REQUEST_KNOCK = 0x2C
COMMAND_REQUEST_BLOCKS_LEARNED = 0x25

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum += byte
    return checksum & 0xFF

def send_command(bus, command, data=None):
    if data is None:
        data = []
    
    # Construct the message
    header = [COMMAND_HEADER, COMMAND_HEADER]  # Double header required
    length_bytes = [len(data) & 0xFF, (len(data) >> 8) & 0xFF]  # Little endian length
    message = [command] + length_bytes + data
    checksum = calculate_checksum(message)
    full_message = header + message + [checksum]
    
    print("Debug: Sending message: {}".format([hex(x) for x in full_message]))
    
    # Send byte by byte with small delays
    try:
        for i, byte in enumerate(full_message):
            bus.write_byte(HUSKYLENS_I2C_ADDR, byte)
            time.sleep(0.001)  # 1ms delay between bytes
        return True
    except Exception as e:
        print("Debug: Send error at byte {}: {}".format(i, e))
        return False

def read_response(bus, expected_length=5):
    response = []
    try:
        # Read with timeout
        start_time = time.time()
        while len(response) < 2 and (time.time() - start_time) < 1.0:
            byte = bus.read_byte(HUSKYLENS_I2C_ADDR)
            response.append(byte)
            if len(response) >= 2 and (response[0] != COMMAND_HEADER or response[1] != COMMAND_HEADER):
                print("Debug: Invalid header received")
                response = []  # Reset and try again
            time.sleep(0.001)
        
        if len(response) < 2:
            print("Debug: Timeout waiting for header")
            return None
            
        # Read command and length
        for _ in range(3):  # Command + 2 length bytes
            response.append(bus.read_byte(HUSKYLENS_I2C_ADDR))
            time.sleep(0.001)
            
        # Calculate actual data length from response
        data_length = response[3] + (response[4] << 8)
        print("Debug: Expected data length: {}".format(data_length))
        
        # Read data and checksum
        for _ in range(data_length + 1):  # +1 for checksum
            response.append(bus.read_byte(HUSKYLENS_I2C_ADDR))
            time.sleep(0.001)
            
        print("Debug: Full response: {}".format([hex(x) for x in response]))
        
        # Verify checksum
        received_checksum = response[-1]
        calculated_checksum = calculate_checksum(response[2:-1])  # Exclude headers and checksum
        if received_checksum != calculated_checksum:
            print("Debug: Checksum mismatch. Received: {}, Calculated: {}".format(
                hex(received_checksum), hex(calculated_checksum)))
            return None
            
        return response
    except Exception as e:
        print("Debug: Read error: {}".format(e))
        return None

def request_blocks_i2c(I2C_bus_number=1):
    try:
        print("Debug: Opening I2C bus {}".format(I2C_bus_number))
        bus = SMBus(I2C_bus_number)
        
        # First send knock command
        print("Debug: Sending knock command...")
        if not send_command(bus, COMMAND_REQUEST_KNOCK):
            print("Debug: Failed to send knock command")
            return None
            
        # Read knock response
        print("Debug: Reading knock response...")
        knock_response = read_response(bus)
        if knock_response is None:
            print("Debug: No valid knock response")
            return None
            
        time.sleep(0.1)  # Wait before next command
        
        # Request learned blocks
        print("Debug: Requesting learned blocks...")
        if not send_command(bus, COMMAND_REQUEST_BLOCKS_LEARNED):
            print("Debug: Failed to send blocks request")
            return None
            
        # Read blocks response
        print("Debug: Reading blocks response...")
        blocks_response = read_response(bus)
        if blocks_response is None:
            print("Debug: No valid blocks response")
            return None
            
        return blocks_response
        
    except Exception as e:
        print("Debug: I2C error: {}".format(e))
        return None
    finally:
        if 'bus' in locals():
            bus.close()
            print("Debug: I2C bus closed")

def parse_huskylens_response(data):
    if not data:
        print("Debug: No data to parse")
        return []
        
    print("Debug: Parsing response of {} bytes".format(len(data)))
    print("Debug: Raw data: {}".format([hex(x) for x in data]))
    
    # Need at least headers (2) + command (1) + length (2) + checksum (1)
    if len(data) < 6:
        print("Debug: Response too short")
        return []
        
    # Verify headers
    if data[0] != COMMAND_HEADER or data[1] != COMMAND_HEADER:
        print("Debug: Invalid headers")
        return []
        
    # Get data length
    data_length = data[3] + (data[4] << 8)
    print("Debug: Data length from header: {}".format(data_length))
    
    objects = []
    if data_length > 0:
        # Each block is 5 words (10 bytes)
        num_blocks = data_length // 10
        for i in range(num_blocks):
            start = 5 + (i * 10)  # Skip header, command, and length
            try:
                obj_id = data[start] + (data[start + 1] << 8)
                x = data[start + 2] + (data[start + 3] << 8)
                y = data[start + 4] + (data[start + 5] << 8)
                width = data[start + 6] + (data[start + 7] << 8)
                height = data[start + 8] + (data[start + 9] << 8)
                
                print("Debug: Found object - ID: {}, pos: ({}, {}), size: {}x{}".format(
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
                print("Debug: Error parsing block {}".format(i))
                break
    
    print("Debug: Found {} valid objects".format(len(objects)))
    return objects

def get_parsed_huskylens_objects():
    print("Debug: Starting HuskyLens object detection")
    data = request_blocks_i2c()
    if data is None:
        print("Debug: No data received from HuskyLens")
        return []
    return parse_huskylens_response(data)
