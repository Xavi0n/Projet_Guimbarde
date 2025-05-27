import time

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
    
    try:
        # Send the entire message in a single I2C transaction
        bus.write_i2c_block_data(HUSKYLENS_I2C_ADDR, full_message[0], full_message[1:])
        time.sleep(0.1)  # Wait for processing
        return True
    except Exception as e:
        print("Debug: Send error: {}".format(e))
        return False

def read_response(bus):
    response = []
    try:
        # Wait a bit before reading
        time.sleep(0.1)
        
        # Try to read the response in blocks
        try:
            # First try to read the header and command (5 bytes)
            initial_block = bus.read_i2c_block_data(HUSKYLENS_I2C_ADDR, 0, 5)
            print("Debug: Initial block read: {}".format([hex(x) for x in initial_block]))
            
            if len(initial_block) >= 5 and initial_block[0] == COMMAND_HEADER:
                response.extend(initial_block)
                
                # Get the length from the response
                length = initial_block[3] + (initial_block[4] << 8)
                print("Debug: Expected data length: {}".format(length))
                
                if length > 0:
                    # Read the data and checksum
                    data_block = bus.read_i2c_block_data(HUSKYLENS_I2C_ADDR, 0, length + 1)
                    response.extend(data_block)
                
                print("Debug: Full response: {}".format([hex(x) for x in response]))
                return response
                
        except Exception as e:
            print("Debug: Block read failed: {}".format(e))
            return None
            
    except Exception as e:
        print("Debug: Read error: {}".format(e))
        return None 