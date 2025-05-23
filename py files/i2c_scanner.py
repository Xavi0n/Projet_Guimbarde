from smbus import SMBus

def scan_i2c_bus(bus_number=1):
    print(f"Scanning I2C bus {bus_number}...")
    bus = SMBus(bus_number)
    
    found_devices = []
    
    for address in range(0x03, 0x78):
        try:
            bus.read_byte(address)
            found_devices.append(address)
            print(f"Found device at address: 0x{address:02X}")
        except Exception as e:
            pass
            
    bus.close()
    
    if not found_devices:
        print("No I2C devices found")
    else:
        print("\nFound devices at addresses:")
        for addr in found_devices:
            print(f"0x{addr:02X}")
            
if __name__ == "__main__":
    # Try both common I2C bus numbers
    try:
        scan_i2c_bus(1)  # Most common on newer systems
    except Exception as e:
        print(f"Error on bus 1: {e}")
        try:
            scan_i2c_bus(0)  # Sometimes used on older systems
        except Exception as e:
            print(f"Error on bus 0: {e}") 