import os

def check_uart_config():
    """Check the configuration of UART pins on BeagleBone Blue"""
    print("Checking UART Configuration")
    print("==========================")
    
    # Check direct device nodes
    uart_devices = {
        'UART0': '/dev/ttyO0',
        'UART1': '/dev/ttyO1',
        'UART2': '/dev/ttyO2',
        'UART3': '/dev/ttyO3',
        'UART4': '/dev/ttyO4',
        'UART5': '/dev/ttyO5'
    }
    
    # Check each UART
    for uart_name, device_path in uart_devices.items():
        print(f"\nChecking {uart_name}:")
        print("-" * 20)
        
        # Check if the UART device exists
        if os.path.exists(device_path):
            print(f"✓ {uart_name} device exists at {device_path}")
            
            # Get the symlink target
            try:
                real_path = os.path.realpath(device_path)
                print(f"→ Symlinked to: {real_path}")
            except Exception as e:
                print(f"Could not resolve symlink: {e}")
            
            # Check permissions
            try:
                stats = os.stat(device_path)
                print(f"Permissions: {oct(stats.st_mode)[-3:]}")
                print(f"Owner: {stats.st_uid}, Group: {stats.st_gid}")
            except Exception as e:
                print(f"Could not get permissions: {e}")
                
        else:
            print(f"✗ {uart_name} device not found at {device_path}")
            
        # Check if the port is in use
        try:
            result = os.popen(f"lsof | grep {os.path.basename(device_path)}").read()
            if result:
                print(f"Port is currently in use by:")
                print(result)
            else:
                print("Port is not in use by any process")
        except Exception as e:
            print(f"Could not check port usage: {e}")

if __name__ == "__main__":
    check_uart_config() 