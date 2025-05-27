from huskylensPythonLibrary import HuskyLensLibrary


my_Var= HuskyLensLibrary("I2C","",address=0x32)

# Check if HuskyLens can recieve commands
print(my_Var.command_request_knock())
# Get all the current blocks on screen
blocks=my_Var.command_request_blocks()
# Print the data
print(blocks)