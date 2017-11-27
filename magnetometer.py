# This file uses the sense hat magnetometer, it displays the value on the
# LED array

import numpy as np
from time import sleep
from sense_hat import SenseHat

# Flag to enable/disable debug print statements
debug_flag = False

def take_reading(hat, debug):
    """
    Take a reading of the magnetic flux density from the
    sense hat's magnetometer. Gets the raw x/y/z values and
    returns the magnitude of that vector in mico Teslas (uT).
    """

    # Get a dictionary of floats indexed by x/y/z
    # representing magnetic flux density in micro Teslas (uT)
    raw_data = hat.get_compass_raw()
    if debug:
        print("x: {x}, y: {y}, z: {z}".format(**raw_data))

    # Convert raw X Y Z data into a numpy array to represent a vector
    vector = np.array([raw_data['x'],raw_data['y'],raw_data['z']])
    if debug:
        print("vector: ", vector)

    # Calculate magnitude of magnetic intensity vector by taking the
    # square root of the dot product of the vector with itself.
    # This represents uT as a single number
    magnitude = np.sqrt(vector.dot(vector))
    if debug:
        print("magnitude: ", magnitude)

    return magnitude

def record_data(hat, delay, debug):
    """
    Runs a loop to take multiple measurements
    hat - SenseHat
    delay - time in seconds to pause between measurements
    debug - T/F flag to enable debug print statements
    """
    # List to store samples of magnetic flux density
    recorded_data = []

    for i in range (0, 20):
        # Use sense hat LED matrix to display progress
        # One iteration lights one pixel on LED starting at (0,0)
        # TODO there has to be a better way to do this
        if i < 8:
            hat.set_pixel(i,0,0,255,0)
        elif i < 16:
            x = i - 8
            hat.set_pixel(x,1,0,255,0)
        elif i < 24:
            x = i - 16
            hat.set_pixel(x,2,0,255,0)
        elif i < 32:
            x = i - 24
            hat.set_pixel(x,3,0,255,0)
            
        # Get a reading from the magnetometer and add it to the list of data
        recorded_data.append(take_reading(hat, False))
        # Wait before taking another measurement
        sleep(delay)

    # TODO figure how we ignore at least the first 10-12 readings.
    # It seems to take that many to settle in on stable value
    print("Recorded magnetic flux densities (uT):")
    print(recorded_data)

hat = SenseHat()

#Configure IMU so only the compass is active
hat.set_imu_config(True, False, False)

event = hat.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))
if event.action == "pressed":
    record_data(hat, 0.5, debug_flag)

hat.clear()
