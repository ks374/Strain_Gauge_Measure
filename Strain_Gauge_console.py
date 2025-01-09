'''
Name: Let monkey sit still: python console
Author: Chenghang Zhang
Date: 1/7/2025
Exp: Get Serial.print output from Arduino (StrainGauge_V3_Analog.ino). 
'''


import serial
import time
import py_monitor_signal
import pygame

if __name__ == "__main__":
    # Set up the serial port
    serial_port = 'COM7'  # Update with your serial port (e.g., COM3 for Windows)
    baud_rate = 9600             # Match this with the Arduino's baud rate
    output_file = 'arduino_output.txt'

    total_session_num = 0
    total_sit_fail_num = 0
    success_rate = 0

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)
    green_color = (0, 255, 0)
    red_color = (255,0,0)

    try:
        # Open the serial connection
        with open(output_file, 'a') as file:
            file.write(f"Experiment start. \n")
        with serial.Serial(serial_port, baud_rate, timeout=10) as ser:
            print(f"Listening on {serial_port} at {baud_rate} baud.")
            
            # Open the file for recording
            while 1:
                # Read a line from the serial port
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Received: {line}\n")
                    line = line.split('-')
                    line2 = line[1]
                    line = int(line[0])
                    total_session_num += 1
                    if line == 1:
                        show_on_second_monitor(screen,red_color)
                    if line == 3:
                        print(line2)
                        continue
                    if line == 2:
                        total_sit_fail_num += 1
                        show_on_second_monitor(screen,green_color)
                    success_rate = (total_session_num-total_sit_fail_num)/total_session_num
                    print(f"Current sitting still: {total_session_num-total_sit_fail_num} / {total_session_num}, success rate: {success_rate}\n")
    except serial.SerialException as e:
        print(f"Error: {e}\n")
        with open(output_file, 'a') as file:
            file.write(f"Sitting still: {total_session_num-total_sit_fail_num} / {total_session_num}, success rate: {success_rate}\n")
            file.write(f"Experiment incomplete, Error: {e}\n")
    except KeyboardInterrupt:
        print("Stopped by user.")
        with open(output_file, 'a') as file:
            file.write(f"Sitting still: {total_session_num-total_sit_fail_num} / {total_session_num}, success rate: {success_rate}\n")
            file.write(f"Experiment incomplete, User interruped\n")
    finally:
        print(f"Output saved to {output_file}.")
        with open(output_file, 'a') as file:
            file.write(f"Sitting still: {total_session_num-total_sit_fail_num} / {total_session_num}, success rate: {success_rate}\n")
            file.write(f"Experiment end. \n")
        pygame.quit()
