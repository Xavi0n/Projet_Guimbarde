from smbus import SMBus
import time

HUSKYLENS_ADDR = 0x32

def test_raw_i2c():
    """Test raw I2C communication with HuskyLens"""
    try:
        bus = SMBus(1)
        print("Opened I2C bus 1")
        
        # Try different approaches to wake up the device
        tests = [
            (0x55, "Header byte"),
            (0x00, "Zero byte"),
            (0xFF, "All ones"),
            (0x2C, "Knock command")
        ]
        
        for test_byte, description in tests:
            print("\nTest: {} (0x{:02X})".format(description, test_byte))
            
            try:
                # Try writing the byte
                print("Writing byte...")
                bus.write_byte(HUSKYLENS_ADDR, test_byte)
                time.sleep(0.1)  # Wait 100ms
                
                # Try reading some bytes
                print("Reading response:")
                for i in range(5):
                    try:
                        value = bus.read_byte(HUSKYLENS_ADDR)
                        print("  Byte {}: 0x{:02X}".format(i, value))
                    except Exception as e:
                        print("  Read error: {}".format(e))
                    time.sleep(0.01)
                    
            except Exception as e:
                print("Write error: {}".format(e))
                
            time.sleep(0.5)  # Wait between tests
            
        # Try reading without writing first
        print("\nTesting read-only:")
        for i in range(5):
            try:
                value = bus.read_byte(HUSKYLENS_ADDR)
                print("  Byte {}: 0x{:02X}".format(i, value))
            except Exception as e:
                print("  Read error: {}".format(e))
            time.sleep(0.01)
            
    except Exception as e:
        print("Test failed: {}".format(e))
    finally:
        if 'bus' in locals():
            bus.close()
            print("\nI2C bus closed")

if __name__ == "__main__":
    test_raw_i2c() 