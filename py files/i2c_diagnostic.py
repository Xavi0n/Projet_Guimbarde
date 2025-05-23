import smbus2
import time
from typing import List

class HuskyLensDebug:
    def __init__(self, bus_number: int = 1, address: int = 0x32):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        
    def test_raw_write(self, data: List[int]) -> bool:
        """Test raw I2C write."""
        try:
            self.bus.write_i2c_block_data(self.address, data[0], data[1:])
            print(f"✓ Raw write successful: {data}")
            return True
        except Exception as e:
            print(f"✗ Raw write failed: {e}")
            return False
            
    def test_raw_read(self, length: int = 1) -> List[int]:
        """Test raw I2C read."""
        try:
            data = self.bus.read_i2c_block_data(self.address, 0, length)
            print(f"✓ Raw read successful: {data}")
            return data
        except Exception as e:
            print(f"✗ Raw read failed: {e}")
            return []
            
    def test_smbus_quick(self) -> bool:
        """Test SMBus quick command."""
        try:
            self.bus.write_quick(self.address)
            print("✓ SMBus quick command successful")
            return True
        except Exception as e:
            print(f"✗ SMBus quick command failed: {e}")
            return False
            
    def test_knock(self) -> bool:
        """Test HuskyLens knock command."""
        knock_command = [0x55, 0xAA, 0x11, 0x00, 0x00, 0x11]  # Knock command
        try:
            self.test_raw_write(knock_command)
            time.sleep(0.1)  # Give device time to respond
            response = self.test_raw_read(5)  # Expected response length
            print(f"Knock response: {response}")
            return len(response) > 0
        except Exception as e:
            print(f"✗ Knock command failed: {e}")
            return False
            
    def run_all_tests(self):
        """Run all diagnostic tests."""
        print("\nHuskyLens I2C Diagnostic Tests")
        print("=============================")
        
        print("\n1. Testing SMBus Quick Command:")
        self.test_smbus_quick()
        
        print("\n2. Testing Raw Write (simple byte):")
        self.test_raw_write([0x00])  # Simple write of zero
        
        print("\n3. Testing Raw Read:")
        self.test_raw_read(1)  # Try to read one byte
        
        print("\n4. Testing Knock Command:")
        self.test_knock()
        
        print("\n5. Testing Protocol Command (request blocks):")
        request_blocks = [0x55, 0xAA, 0x21, 0x00, 0x00, 0x21]  # Request blocks command
        self.test_raw_write(request_blocks)
        time.sleep(0.1)
        self.test_raw_read(5)

if __name__ == "__main__":
    print("Starting HuskyLens I2C diagnostics...")
    print("Using I2C bus 1, address 0x32")
    
    debugger = HuskyLensDebug()
    debugger.run_all_tests() 