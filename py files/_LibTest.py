import sys
sys.path.append('/home/debian/HUSKYLENSPython')

import huskylib

huskyLens = HuskyLensLibrary("I2C","",address=0x32)
huskyLens.algorithm("ALGORITHM_FACE_RECOGNITION")

while(1):
    data=huskyLens.blocks()
    x=0
    for i in data:
        x=x+1
        print("Face {} data: {}".format(x,i))
