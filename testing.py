#Python Script for Parsing and Displaying Anemometer Sensor Data

#The following key points are used for processing (taken from Firmware):
#1.Reading 4 bytes of data from the sensor.
#2.Using a checksum function to verify the integrity of the data.
#3.Combining high and low bytes to form a reading.
#4.Converting raw sensor values to human-readable format.


import serial
import struct
import time

# Define the commands based on your firmware code
VELOCITY_READ_COMMAND = bytes([1, 0, 0, 1])
TEMP_READ_COMMAND = bytes([2, 0, 0, 2])
VELRAW_READ_COMMAND = bytes([9, 0, 0, 9])

# Function to calculate checksum
def calculate_checksum(data):
    checksum = data[0]
    for byte in data[1:-1]:
        checksum ^= byte
    return checksum

# Function to convert raw data to human-readable format
def parse_data(data, conversion_type):
    if calculate_checksum(data) != data[-1]:
        return "Invalid checksum"
    
    raw_value = (data[0] << 8) | data[1]  # Combine high and low bytes
    if conversion_type == "velocity":
        reading = raw_value * 0.001  # Assuming raw value is in mm/s
    elif conversion_type == "temperature":
        reading = raw_value * 0.01  # Assuming raw value is in hundredths of a degree
    else:
        reading = raw_value  # Default conversion
    
    return reading

# Initialize serial communication
ser = serial.Serial('COM17', 19200, timeout=1)  # Adjust COM port as necessary

def request_data(command):
    ser.write(command)
    response = ser.read(4)  # Read 4 bytes of response
    return response

def main():
    while True:
        raw_velocity_data = request_data(VELRAW_READ_COMMAND)
        filtered_velocity_data = request_data(VELOCITY_READ_COMMAND)
        temperature_data = request_data(TEMP_READ_COMMAND)
        
        raw_velocity = parse_data(raw_velocity_data, "velocity")
        filtered_velocity = parse_data(filtered_velocity_data, "velocity")
        temperature = parse_data(temperature_data, "temperature")
        
        print(f"Raw Velocity: {raw_velocity} m/s")
        print(f"Filtered Velocity: {filtered_velocity} m/s")
        print(f"Temperature: {temperature} °C")
        
        ser.flushInput()
       time.sleep(1)

if __name__ == "__main__":
    main()
