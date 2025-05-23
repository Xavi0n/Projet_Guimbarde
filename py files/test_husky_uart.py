import serial
import time

def test_husky_uart():
    """Test if HuskyLens is in UART mode by trying to communicate over serial"""
    try:
        # Try common UART ports on BeagleBone
        ports = ['/dev/ttyO1', '/dev/ttyO2', '/dev/ttyO4', '/dev/ttyO5']
        
        for port in ports:
            try:
                print("\nTrying port {}...".format(port))
                # HuskyLens default UART settings
                ser = serial.Serial(
                    port=port,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
                
                # Send knock command
                command = bytearray([0x55, 0x55, 0x2C, 0x00, 0x00, 0x2C])
                print("Sending knock command...")
                ser.write(command)
                time.sleep(0.1)
                
                # Read response
                if ser.in_waiting:
                    response = ser.read(ser.in_waiting)
                    print("Got response: {}".format([hex(x) for x in response]))
                    if len(response) > 0 and response[0] != 0:
                        print("Got non-zero response - HuskyLens might be in UART mode!")
                else:
                    print("No response on this port")
                    
                ser.close()
                
            except Exception as e:
                print("Error on {}: {}".format(port, e))
                continue
                
    except Exception as e:
        print("Test failed: {}".format(e))

if __name__ == "__main__":
    test_husky_uart() 