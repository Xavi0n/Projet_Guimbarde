from huskylib import HuskyLensLibrary

def main():
    huskylens = HuskyLensLibrary("I2C", 0x32)
    huskylens.algorthim("ALGORITHM_OBJECT_RECOGNITION")

    print("Requesting data from HuskyLens...")  # Debug line
    objects = huskylens.requestAll()
    print("Raw objects:", objects)  # Debug line

    if not objects:
        print("No blocks received.")
        return

    for obj in objects:
        print(f"{obj.x} {obj.y} {obj.width} {obj.height} {obj.ID}")

if __name__ == "__main__":
    main()

