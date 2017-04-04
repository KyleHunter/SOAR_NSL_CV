# SOAR_NSL_CV

## About
- Code to aim a camera from a lander ejected from alt. of 1 mile to a point on the ground
- Competing in the 2016-2017 NASA NSL ([NASA student Launch](http://www.usfsoar.com/projects/nsl-2016-2017/))
- Built by students in SOAR ([Society Of Aeronautics and Rockety](http://www.usfsoar.com/)) at USF ([University of South Florida](http://www.usf.edu/))

## Error Codes
##### Format: Red:Red:Red:Green 
- 1000: No communications between Arduino and Raspberry Pi
- 1100: Very dark image taken. Maybe lens cap on (Seriously?), lens focus off, usb cable disconnected, ect..
- 1110: No communications with 10DOF board
- 0110: No Communications with GPS 
- 0001(Flashing): No error, searching for GPS fix
- 1010: No clue, bad exception error
- 0001(Solid): No error, GPS fixed
- 1111(Solid): Waiting for start command
