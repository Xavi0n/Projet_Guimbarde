import os

def check_uart_config():
    """Check the configuration of UART pins on BeagleBone Blue"""
    print("Checking UART Configuration")
    print("==========================")
    
    # Check if config files exist
    uart_paths = {
        'UART1': '/sys/devices/platform/ocp/48022000.serial/tty/ttyO1',
        'UART2': '/sys/devices/platform/ocp/48024000.serial/tty/ttyO2',
        'UART4': '/sys/devices/platform/ocp/481a8000.serial/tty/ttyO4',
        'UART5': '/sys/devices/platform/ocp/481aa000.serial/tty/ttyO5'
    }
    
    # Check each UART
    for uart_name, base_path in uart_paths.items():
        print(f"\nChecking {uart_name}:")
        print("-" * 20)
        
        # Check if the UART device exists
        if os.path.exists(base_path):
            print(f"✓ {uart_name} device exists")
            
            # Try to read current settings
            try:
                with open(f"{base_path}/dev", 'r') as f:
                    dev_info = f.read().strip()
                print(f"Device info: {dev_info}")
            except Exception as e:
                print(f"Could not read device info: {e}")
                
        else:
            print(f"✗ {uart_name} device not found at {base_path}")
            
        # Check if the port is in use
        try:
            result = os.popen(f"lsof | grep ttyO{uart_name[-1]}").read()
            if result:
                print(f"Port is currently in use by:")
                print(result)
            else:
                print("Port is not in use by any process")
        except Exception as e:
            print(f"Could not check port usage: {e}")

if __name__ == "__main__":
    check_uart_config() 