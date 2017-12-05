# This file uses the sense hat magnetometer, it displays the value on the
# LED array

import numpy as np
from time import sleep
from sense_hat import SenseHat

# Flag to enable/disable debug print statements
debug_flag = False

# Number of samples to skip while the magnetometer 
# settles in on actual value
skip_sample = 12

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

def find_mean(recorded_data_list):
    list_size = len(recorded_data_list)
    total_of_numbers = 0

    for x in recorded_data_list:
        total_of_numbers = total_of_numbers + x

    if list_size > 0:
        mean = total_of_numbers / list_size
        return mean
    else:
        return 0
        

def record_data(hat, delay, debug):
    """
    Runs a loop to take multiple measurements
    hat - SenseHat
    delay - time in seconds to pause between measurements
    debug - T/F flag to enable debug print statements
    """
    # List to store samples of magnetic flux density
    recorded_data = []

    # Display red S when starting recording
    hat.show_letter('S', [255,0,0])
    
    for i in range (0, 20):
        # Since it takes the magnetometer multiple samples to settle
        # on a value do not record data until values settle
        if i >= skip_sample:
            # Display green R when recording
            hat.show_letter('R', [0,255,0])
            # Get a reading from the magnetometer and add it to the list of data
            recorded_data.append(take_reading(hat, debug))
        else:
            take_reading(hat, debug)
        
        # Wait before taking another measurement
        sleep(delay)

    print("Recorded magnetic flux densities (uT):")
    print(recorded_data)

    mean = find_mean(recorded_data)
    print("average magnetic flux density (uT):")
    print(mean)

hat = SenseHat()

#Configure IMU so only the compass is active
hat.set_imu_config(True, False, False)

# Display blue W when waiting for button press to start recording
hat.show_letter('W', [0,0,255])

# Once any joystick button press is received start recording
event = hat.stick.wait_for_event()
if event.action == "pressed":
    record_data(hat, 0.5, debug_flag)

hat.clear()
