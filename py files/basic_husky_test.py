from smbus import SMBus
import time

HUSKYLENS_ADDR = 0x32
COMMAND_HEADER = 0x55
COMMAND_REQUEST_KNOCK = 0x2C

def test_husky_communication():
    bus = SMBus(1)
    try:
        print("Starting basic HuskyLens communication tests...")
        
        # Test 1: Simple read
        print("\nTest 1: Simple read")
        try:
            value = bus.read_byte(HUSKYLENS_ADDR)
            print(f"Read value: 0x{value:02X}")
        except Exception as e:
            print(f"Read error: {e}")
            
        time.sleep(0.1)
        
        # Test 2: Write single header byte
        print("\nTest 2: Write single header")
        try:
            bus.write_byte(HUSKYLENS_ADDR, COMMAND_HEADER)
            print("Write successful")
            time.sleep(0.1)
            value = bus.read_byte(HUSKYLENS_ADDR)
            print(f"Response: 0x{value:02X}")
        except Exception as e:
            print(f"Write error: {e}")
            
        time.sleep(0.1)
        
        # Test 3: Write knock sequence byte by byte
        print("\nTest 3: Write knock sequence byte by byte")
        sequence = [COMMAND_HEADER, COMMAND_HEADER, COMMAND_REQUEST_KNOCK, 0x00, 0x00]
        try:
            print("Sending:", [f"0x{x:02X}" for x in sequence])
            for byte in sequence:
                bus.write_byte(HUSKYLENS_ADDR, byte)
                time.sleep(0.01)
            print("Write successful")
            
            # Read response
            print("Reading response:")
            for i in range(5):
                try:
                    value = bus.read_byte(HUSKYLENS_ADDR)
                    print(f"Byte {i}: 0x{value:02X}")
                except Exception as e:
                    print(f"Read error at byte {i}: {e}")
                time.sleep(0.01)
        except Exception as e:
            print(f"Sequence error: {e}")
            
        # Test 4: Write knock command as block
        print("\nTest 4: Write knock command as block")
        try:
            bus.write_i2c_block_data(HUSKYLENS_ADDR, COMMAND_HEADER, sequence[1:])
            print("Block write successful")
            
            # Read response
            print("Reading response:")
            for i in range(5):
                try:
                    value = bus.read_byte(HUSKYLENS_ADDR)
                    print(f"Byte {i}: 0x{value:02X}")
                except Exception as e:
                    print(f"Read error at byte {i}: {e}")
                time.sleep(0.01)
        except Exception as e:
            print(f"Block write error: {e}")
            
    finally:
        bus.close()
        print("\nTests completed")

if __name__ == "__main__":
    test_husky_communication() 