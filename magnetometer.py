# This file uses the sense hat magnetometer, it displays the value on the
# LED array

import numpy as np
from time import sleep, localtime, strftime 
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

def input_mag_temp():
    """
    Imputs the magnet temperature from the command line for
    the experiment run. Stores it in mag_temp or sets the
    use_ambient flag
    """
    mag_temp = input("Enter the magnet temperature (F) or amb for ambient: ")
    print("Read value: " + mag_temp)

    if mag_temp != "amb":
        mag_tempF = float(mag_temp)
        # convert from F to C
        mag_tempF = (mag_tempF - 32)/1.8
        mag_temp = str(mag_tempF)
        
    print("mag_temp = " + mag_temp)
    return mag_temp

def write_to_file(temp, mag_temp, recorded_data, mean):
    """
    Writes recorded data to a file
    temp, recorded_data, and mean are all data passed
    in to be written to a file named for the date/time
    the test was completed
    """
    # Get current time
    date_time = strftime("%Y-%m-%d_%H.%M.%S", localtime())

    # Get magnet temp
    if mag_temp == "amb":
        magnet_tempC = temp
    else:
        magnet_tempC = mag_temp
    
    print(date_time)
    print("Ambient temperature (degrees C):")
    print(temp)
    print("Magnet temperature (degrees C): ")
    print(magnet_tempC)
    print("Recorded magnetic flux densities (uT):")
    print(recorded_data)
    print("Average magnetic flux density (uT):")
    print(mean)
    
    # Open file
    file = open(date_time, 'w')
    
    # Write time and date to file
    file.write("Current date & time: ")
    file.write(date_time + '\n\n')
    
    # Write ambient temperature to file
    file.write("Ambient temperature (degrees C): ")
    file.write(str(temp) + '\n\n')

    # Write magnet temperature
    file.write("Magnet temperature (degrees C): ")
    file.write(str(magnet_tempC) + '\n\n')
    
    # Write recorded data to file
    file.write("Recorded magnetic flux densities (uT): ")
    file.write(str(recorded_data) + '\n\n')  
    
    # Write mean to file
    file.write("Average magnetic flux density (uT): ")
    file.write(str(mean) + '\n')

    # Close file
    file.close()

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

    mean = find_mean(recorded_data)

    # Get the ambient temperature in degrees C
    temp = hat.get_temperature()

    # Flag to use the ambient temp as the magnet temp
    use_ambient = False

    mag_temp = input_mag_temp()

    write_to_file(temp, mag_temp, recorded_data, mean)


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
