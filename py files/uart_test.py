import serial
import time

def test_uart_connection(port='/dev/ttyO1', baudrate=9600):
    """
    Test UART communication with HuskyLens
    Default port is ttyO1 which is UART1 on BeagleBone Blue
    """
    try:
        # Open serial connection
        print(f"Opening {port} at {baudrate} baud...")
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        if not ser.is_open:
            ser.open()
        
        print("Serial port opened successfully")
        
        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Send header sequence (0x55 0xAA 0x11 0x00 0x00 0x11)
        # This requests the current algorithm from HuskyLens
        header = bytes([0x55, 0xAA, 0x11, 0x00, 0x00, 0x11])
        print("\nSending header sequence:", ' '.join(f'0x{b:02X}' for b in header))
        ser.write(header)
        ser.flush()
        
        # Wait for response
        time.sleep(0.1)
        
        # Read response
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print("\nReceived response:", ' '.join(f'0x{b:02X}' for b in response))
        else:
            print("\nNo response received")
            
        # Try reading raw data
        print("\nTrying to read raw data...")
        for _ in range(3):
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                print("Raw data:", ' '.join(f'0x{b:02X}' for b in data))
            time.sleep(0.1)
            
        ser.close()
        print("\nSerial port closed")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed after error")

def main():
    # Test different UART ports available on BeagleBone Blue
    uart_ports = [
        '/dev/ttyO1',  # UART1
        '/dev/ttyO2',  # UART2
        '/dev/ttyO4',  # UART4
        '/dev/ttyO5'   # UART5
    ]
    
    print("Testing UART communication with HuskyLens")
    print("=========================================")
    
    for port in uart_ports:
        print(f"\nTesting port: {port}")
        print("-" * 40)
        test_uart_connection(port)
        time.sleep(1)

if __name__ == "__main__":
    main() 