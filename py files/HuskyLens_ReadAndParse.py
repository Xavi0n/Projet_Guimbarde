# huskylens.py
from smbus import SMBus
import time

HUSKYLENS_I2C_ADDR = 0x32

# Protocol Headers and Commands
COMMAND_HEADER = 0x55
COMMAND_END = 0x54
COMMAND_REQUEST_KNOCK = 0x2C
COMMAND_REQUEST_BLOCKS_LEARNED = 0x25

def flush_i2c(bus):
    """Clear any pending data on the I2C bus"""
    try:
        for _ in range(5):  # Read a few bytes to clear any pending data
            bus.read_byte(HUSKYLENS_I2C_ADDR)
            time.sleep(0.01)
    except:
        pass
    time.sleep(0.1)  # Wait a bit after flushing

def send_command(bus, command, data=None):
    if data is None:
        data = []
    
    # Flush before sending
    flush_i2c(bus)
    
    # Construct the message
    header = [COMMAND_HEADER, COMMAND_HEADER]
    length_bytes = [len(data) & 0xFF, (len(data) >> 8) & 0xFF]
    message = header + [command] + length_bytes + data
    checksum = sum(message[2:]) & 0xFF  # Calculate checksum excluding headers
    full_message = message + [checksum]
    
    print("Debug: Sending message: {}".format([hex(x) for x in full_message]))
    
    # First write the header bytes with a longer delay
    try:
        # Write first header byte
        bus.write_byte(HUSKYLENS_I2C_ADDR, COMMAND_HEADER)
        time.sleep(0.05)  # 50ms delay after first header
        
        # Write second header byte
        bus.write_byte(HUSKYLENS_I2C_ADDR, COMMAND_HEADER)
        time.sleep(0.05)  # 50ms delay after second header
        
        # Write command and length
        bus.write_byte(HUSKYLENS_I2C_ADDR, command)
        time.sleep(0.01)
        for byte in length_bytes:
            bus.write_byte(HUSKYLENS_I2C_ADDR, byte)
            time.sleep(0.01)
            
        # Write data if any
        for byte in data:
            bus.write_byte(HUSKYLENS_I2C_ADDR, byte)
            time.sleep(0.01)
            
        # Write checksum
        bus.write_byte(HUSKYLENS_I2C_ADDR, checksum)
        time.sleep(0.1)  # Longer delay after complete message
        
        return True
    except Exception as e:
        print("Debug: Send error: {}".format(e))
        return False

def read_response(bus):
    response = []
    try:
        # Wait a bit before reading
        time.sleep(0.1)
        
        # Read until we get a header or timeout
        start_time = time.time()
        while (time.time() - start_time) < 0.5:  # 500ms timeout
            byte = bus.read_byte(HUSKYLENS_I2C_ADDR)
            print("Debug: Read byte: {}".format(hex(byte)))
            
            if byte == COMMAND_HEADER:
                response.append(byte)
                if len(response) == 1:
                    # Got first header byte, wait a bit then continue
                    time.sleep(0.05)
                    continue
                    
                # Try to read the rest of the message
                # Command byte
                command = bus.read_byte(HUSKYLENS_I2C_ADDR)
                response.append(command)
                time.sleep(0.01)
                
                # Length bytes
                length_low = bus.read_byte(HUSKYLENS_I2C_ADDR)
                length_high = bus.read_byte(HUSKYLENS_I2C_ADDR)
                response.extend([length_low, length_high])
                
                length = length_low + (length_high << 8)
                print("Debug: Expected data length: {}".format(length))
                
                # Read data
                for _ in range(length):
                    response.append(bus.read_byte(HUSKYLENS_I2C_ADDR))
                    time.sleep(0.01)
                
                # Read checksum
                checksum = bus.read_byte(HUSKYLENS_I2C_ADDR)
                response.append(checksum)
                
                print("Debug: Full response: {}".format([hex(x) for x in response]))
                return response
                
            time.sleep(0.01)
        
        print("Debug: Timeout waiting for valid response")
        return None
        
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
            
        time.sleep(0.2)  # Wait longer between commands
        
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
        
    print("Debug: Raw data: {}".format([hex(x) for x in data]))
    
    # Need at least headers (2) + command (1) + length (2) + checksum (1)
    if len(data) < 6:
        print("Debug: Response too short")
        return []
        
    # Get data length
    data_length = data[3] + (data[4] << 8)
    print("Debug: Data length from header: {}".format(data_length))
    
    objects = []
    if data_length > 0 and data_length % 10 == 0:  # Each block should be 10 bytes
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
