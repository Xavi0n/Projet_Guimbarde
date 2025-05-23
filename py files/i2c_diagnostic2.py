import smbus
import time
from typing import List

class HuskyLensDebug:
    def __init__(self, bus_number: int = 1, address: int = 0x32):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        time.sleep(2)  # Give device time to initialize
        
    def calculate_checksum(self, data: List[int]) -> int:
        """Calculate checksum for HuskyLens protocol."""
        return sum(data) & 0xFF
        
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
            
    def test_protocol_version(self) -> bool:
        """Test reading protocol version."""
        cmd = [0x55, 0xAA, 0x01, 0x00, 0x00, 0x01]  # Protocol version command
        try:
            print("\nTesting protocol version command:")
            if not self.test_raw_write(cmd):
                return False
                
            time.sleep(0.1)
            response = self.test_raw_read(5)
            
            if len(response) >= 5:
                print(f"Protocol response analysis:")
                print(f"Header1: {hex(response[0])} (expected 0x55)")
                print(f"Header2: {hex(response[1])} (expected 0xAA)")
                print(f"Command: {hex(response[2])}")
                print(f"Length:  {hex(response[3])}")
                print(f"Checksum: {hex(response[4])}")
                
            return len(response) > 0 and response[0] == 0x55 and response[1] == 0xAA
        except Exception as e:
            print(f"✗ Protocol version test failed: {str(e)}")
            return False
            
    def test_request_knock(self) -> bool:
        """Test knock command with improved error handling."""
        knock_cmd = [0x55, 0xAA, 0x11, 0x00, 0x00, 0x11]
        try:
            print("\nTesting knock command with improved handling:")
            if not self.test_raw_write(knock_cmd):
                return False
                
            time.sleep(0.1)
            response = self.test_raw_read(5)
            
            if len(response) >= 5:
                print(f"Knock response analysis:")
                print(f"Header1: {hex(response[0])} (expected 0x55)")
                print(f"Header2: {hex(response[1])} (expected 0xAA)")
                print(f"Command: {hex(response[2])}")
                print(f"Length:  {hex(response[3])}")
                print(f"Checksum: {hex(response[4])}")
                
            return len(response) > 0
        except Exception as e:
            print(f"✗ Knock command failed: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all diagnostic tests."""
        print("\nHuskyLens I2C Diagnostic Tests (Extended)")
        print("=====================================")
        
        print("\n1. Testing Protocol Version:")
        self.test_protocol_version()
        
        print("\n2. Testing Knock Command:")
        self.test_request_knock()

if __name__ == "__main__":
    print("Starting HuskyLens I2C diagnostics (extended version)...")
    print("Using I2C bus 1, address 0x32")
    
    debugger = HuskyLensDebug()
    debugger.run_all_tests() 