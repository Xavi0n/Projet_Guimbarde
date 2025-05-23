# huskylens.py
from smbus import SMBus
import time

HUSKYLENS_I2C_ADDR = 0x32  # 7-bit address

# HuskyLens Commands
COMMAND_HEADER = 0x55
COMMAND_END = 0x54
COMMAND_REQUEST_KNOCK = 0x2C
COMMAND_REQUEST_ALGORITHM = 0x2D
COMMAND_REQUEST_BLOCKS = 0x21
COMMAND_REQUEST_ARROWS = 0x22
COMMAND_REQUEST_LEARNED = 0x24
COMMAND_REQUEST_BLOCKS_LEARNED = 0x25  # This is what we'll use for trained objects
COMMAND_REQUEST_ARROWS_LEARNED = 0x26
COMMAND_REQUEST_BY_ID = 0x27
COMMAND_REQUEST_BLOCKS_BY_ID = 0x28
COMMAND_REQUEST_ARROWS_BY_ID = 0x29

def calculate_checksum(data):
    return sum(data) & 0xFF

def request_blocks_i2c(I2C_bus_number=1):
    try:
        print("Debug: Opening I2C bus {}".format(I2C_bus_number))
        I2C_bus = SMBus(I2C_bus_number)
        
        # First, knock to check if HuskyLens is ready
        knock_command = [COMMAND_HEADER, COMMAND_HEADER, COMMAND_REQUEST_KNOCK, 0x00, 0x00]
        knock_command.append(calculate_checksum(knock_command[2:4]))
        
        print("Debug: Sending knock command: {}".format([hex(x) for x in knock_command]))
        I2C_bus.write_i2c_block_data(HUSKYLENS_I2C_ADDR, knock_command[0], knock_command[1:])
        time.sleep(0.1)  # Wait for HuskyLens to process
        
        # Try to read knock response
        try:
            knock_response = []
            for _ in range(5):
                byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                knock_response.append(byte)
            print("Debug: Knock response: {}".format([hex(x) for x in knock_response]))
            
            # Verify knock response
            if knock_response[0] != COMMAND_HEADER or knock_response[1] != COMMAND_HEADER:
                print("Debug: Invalid knock response")
                return None
                
        except IOError as e:
            print("Debug: Knock read error: {}".format(e))
        
        # Now send request for learned blocks
        request_command = [COMMAND_HEADER, COMMAND_HEADER, COMMAND_REQUEST_BLOCKS_LEARNED, 0x00, 0x00]
        request_command.append(calculate_checksum(request_command[2:4]))
        
        print("Debug: Sending learned blocks request: {}".format([hex(x) for x in request_command]))
        I2C_bus.write_i2c_block_data(HUSKYLENS_I2C_ADDR, request_command[0], request_command[1:])
        time.sleep(0.2)  # Give more time for processing
        
        # Read response
        I2C_response_bytes = []
        try:
            # First read header (should be 5 bytes)
            header = []
            for _ in range(5):
                byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                header.append(byte)
            print("Debug: Response header: {}".format([hex(x) for x in header]))
            
            if header[0] == COMMAND_HEADER and header[1] == COMMAND_HEADER:
                # Valid header found, read the rest based on length
                length = header[3] + (header[4] << 8)
                print("Debug: Expected data length: {}".format(length))
                
                # Read the data and checksum
                for _ in range(length + 1):  # +1 for checksum
                    byte = I2C_bus.read_byte(HUSKYLENS_I2C_ADDR)
                    I2C_response_bytes.append(byte)
                    print("Debug: Read data byte: {}".format(hex(byte)))
            
        except IOError as e:
            print("Debug: Data read error: {}".format(e))
        finally:
            I2C_bus.close()
        
        if header and I2C_response_bytes:
            full_response = header + I2C_response_bytes
            print("Debug: Full response: {}".format([hex(x) for x in full_response]))
            return full_response
        return None
        
    except Exception as e:
        print("I2C error: {}".format(e))
        if 'I2C_bus' in locals():
            I2C_bus.close()
        return None

def parse_huskylens_response(data):
    if not data or len(data) < 5:
        print("Debug: Invalid response data")
        return []
        
    print("Debug: Parsing response of {} bytes".format(len(data)))
    objects = []
    
    # Check header
    if data[0] != COMMAND_HEADER or data[1] != COMMAND_HEADER:
        print("Debug: Invalid header")
        return []
        
    # Get length
    length = data[3] + (data[4] << 8)
    print("Debug: Data length from header: {}".format(length))
    
    # Check if we have enough data
    if len(data) < length + 6:  # header(5) + data(length) + checksum(1)
        print("Debug: Incomplete data")
        return []
        
    # Process data blocks
    data_start = 5
    while data_start < len(data) - 5:  # Need at least 5 bytes for a block
        try:
            obj_id = data[data_start] + (data[data_start + 1] << 8)
            x = data[data_start + 2] + (data[data_start + 3] << 8)
            y = data[data_start + 4] + (data[data_start + 5] << 8)
            width = data[data_start + 6] + (data[data_start + 7] << 8)
            height = data[data_start + 8] + (data[data_start + 9] << 8)
            
            print("Debug: Found object - ID: {}, pos: ({}, {}), size: {}x{}".format(
                obj_id, x, y, width, height))
                
            objects.append({
                'id': obj_id,
                'x': x,
                'y': y,
                'width': width,
                'height': height
            })
            
            data_start += 10
        except IndexError:
            break
            
    print("Debug: Parsed {} objects".format(len(objects)))
    return objects

def get_parsed_huskylens_objects():
    print("Debug: Starting HuskyLens object detection")
    data = request_blocks_i2c()
    if data is None:
        print("Debug: No data received from HuskyLens")
        return []
    return parse_huskylens_response(data)
