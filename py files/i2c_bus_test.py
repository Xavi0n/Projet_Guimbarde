from smbus import SMBus
import time

HUSKYLENS_ADDR = 0x32

def test_i2c_bus(bus_number):
    """Test a specific I2C bus"""
    try:
        print("\n=== Testing I2C Bus {} ===".format(bus_number))
        bus = SMBus(bus_number)
        
        # Try to write and read
        print("Attempting communication...")
        
        # First just try to read
        print("Reading without write:")
        try:
            value = bus.read_byte(HUSKYLENS_ADDR)
            print("  Read value: 0x{:02X}".format(value))
        except Exception as e:
            print("  Read error: {}".format(e))
            
        # Now try write then read
        print("\nTesting write then read:")
        try:
            # Write header bytes
            print("Writing header bytes...")
            bus.write_byte(HUSKYLENS_ADDR, 0x55)
            time.sleep(0.05)
            bus.write_byte(HUSKYLENS_ADDR, 0x55)
            time.sleep(0.05)
            
            # Read response
            print("Reading response:")
            for i in range(3):
                try:
                    value = bus.read_byte(HUSKYLENS_ADDR)
                    print("  Byte {}: 0x{:02X}".format(i, value))
                except Exception as e:
                    print("  Read error: {}".format(e))
                time.sleep(0.01)
                
        except Exception as e:
            print("Write error: {}".format(e))
            
        bus.close()
        print("Bus {} closed".format(bus_number))
        
    except Exception as e:
        print("Failed to open bus {}: {}".format(bus_number, e))

def main():
    print("Testing all possible I2C buses...")
    
    # BeagleBone Blue typically has I2C buses 0, 1, and 2
    for bus_number in range(3):
        test_i2c_bus(bus_number)
        time.sleep(0.5)  # Wait between bus tests

if __name__ == "__main__":
    main() 