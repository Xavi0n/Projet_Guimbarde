import smbus
import time
from typing import List

class HuskyLensDebug:
    def __init__(self, bus_number: int = 1, address: int = 0x32):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        time.sleep(2)  # Give device time to initialize
        
    def test_raw_write(self, data: List[int]) -> bool:
        """Test raw I2C write with detailed error."""
        try:
            print(f"Attempting to write: {[hex(x) for x in data]}")
            self.bus.write_i2c_block_data(self.address, data[0], data[1:])
            print(f"✓ Raw write successful")
            return True
        except Exception as e:
            print(f"✗ Raw write failed: {str(e)}")
            return False
            
    def test_raw_read(self, length: int = 1) -> List[int]:
        """Test raw I2C read with detailed error."""
        try:
            data = self.bus.read_i2c_block_data(self.address, 0, length)
            print(f"✓ Raw read successful: {[hex(x) for x in data]}")
            return data
        except Exception as e:
            print(f"✗ Raw read failed: {str(e)}")
            return []

    def force_i2c_mode(self) -> bool:
        """Attempt to force I2C mode through commands."""
        # Command sequence to try forcing I2C mode
        # Different attempts with varying protocols
        commands = [
            # Standard knock
            [0x55, 0xAA, 0x11, 0x00, 0x00, 0x11],
            # Save settings command
            [0x55, 0xAA, 0x10, 0x00, 0x00, 0x10],
            # Alternative protocol command
            [0x55, 0xAA, 0xFF, 0x00, 0x00, 0xFF],
            # Another variant
            [0x55, 0xAA, 0x00, 0x00, 0x00, 0x00]
        ]
        
        print("\nAttempting to force I2C mode:")
        for i, cmd in enumerate(commands, 1):
            print(f"\nTry {i}:")
            self.test_raw_write(cmd)
            time.sleep(0.5)  # Longer delay between attempts
            response = self.test_raw_read(5)
            
            if len(response) >= 5 and (response[0] == 0x55 or response[1] == 0xAA):
                print("Possible successful response!")
                return True
                
            time.sleep(0.5)  # Wait before next attempt
            
        return False

    def test_simple_commands(self):
        """Test very simple I2C commands."""
        print("\nTesting simple I2C commands:")
        
        # Try single byte commands
        for byte in [0x00, 0x55, 0xAA, 0xFF]:
            print(f"\nTesting single byte {hex(byte)}:")
            self.test_raw_write([byte])
            time.sleep(0.1)
            self.test_raw_read(1)
            time.sleep(0.1)

    def run_all_tests(self):
        """Run all diagnostic tests."""
        print("\nHuskyLens I2C Diagnostic Tests (Mode Force Attempt)")
        print("=============================================")
        
        print("\n1. Attempting to force I2C mode:")
        self.force_i2c_mode()
        
        print("\n2. Testing simple commands:")
        self.test_simple_commands()

if __name__ == "__main__":
    print("Starting HuskyLens I2C diagnostics (force mode version)...")
    print("Using I2C bus 1, address 0x32")
    
    debugger = HuskyLensDebug()
    debugger.run_all_tests() 