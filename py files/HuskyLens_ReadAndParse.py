from huskylib import HuskyLensLibrary

def main():
    huskylens = HuskyLensLibrary("I2C", 0x32)
    huskylens.algorithm("ALGORITHM_OBJECT_RECOGNITION")

    objects = huskylens.requestAll()
    if not objects:
        return  # No output if no objects

    for obj in objects:
        print(f"{obj.x} {obj.y} {obj.width} {obj.height} {obj.ID}")

if __name__ == "__main__":
    main()
