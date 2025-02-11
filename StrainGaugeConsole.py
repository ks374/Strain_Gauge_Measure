'''
Name: Let monkey sit still: python console
Author: Chenghang Zhang
Date: 1/7/2025
Exp: Get Serial.print output from Arduino (StrainGauge_V3_Analog.ino). 
'''


import serial
import time
from py_monitor_signal import show_on_second_monitor
import pygame

def get_cur_timing(line,val):
    line_temp = line.split(':')
    if line_temp[0] == "Time elapsed":
        value = line_temp[1].strip()
        return value
    else:
        return val
	
def get_reading_number(line):
    line_temp = line.split(':')
    if line_temp[0] == "Cur_voltage":
        value = line_temp[1].strip()
        return value
    else:
        return 0

def write_number(outfile,time,voltage):
     with open(outfile, 'a') as file:
            file.write(f"{time},{voltage},\n")

if __name__ == "__main__":
    # Set up the serial port
    global screen_width,screen_height,circle_radius,circle_color,gray_color
    
    serial_port = 'COM7'  # Update with your serial port (e.g., COM3 for Windows)
    baud_rate = 9600             # Match this with the Arduino's baud rate
    output_file = 'arduino_output_20250130_longrecording.txt'

    Number_reading_Mode = 1

    total_session_num = 1
    total_sit_fail_num = 0
    success_rate = 0
    
    screen_width, screen_height = 1024, 768
    circle_color = (128,128,128)
    circle_radius = 20

    cur_time = 0

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)
    green_color = (180, 255, 180)
    gray_color = (128,128,128)
    red_color = (255,180,180)
    #Show green color by default:
    screen.fill(gray_color)
    pygame.draw.circle(screen,circle_color,(screen_width//2,screen_height//2),circle_radius)
    pygame.display.flip()

    try:
        # Open the serial connection
        with open(output_file, 'a') as file:
            file.write(f"Experiment start. \n")
        with serial.Serial(serial_port, baud_rate, timeout=10) as ser:
            print(f"Listening on {serial_port} at {baud_rate} baud.")
            Session_conclude_flag = 0
            # Open the file for recording
            while 1:
                # Read a line from the serial port
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()

                    if Number_reading_Mode == 1:
                        cur_time = get_cur_timing(line,cur_time)
                        cur_voltage = get_reading_number(line)
                        if cur_voltage != 0:
                            write_number(output_file,cur_time,cur_voltage)
                        
                    line = line.split('-')
                    #Check for incorrect message encoding: 
                    try:
                        line0 = int(line[0])
                    except:
                        print("Caught voltage writing, write and reboot.")
                        continue
                    line2 = line[1]
                    if line0 == 1:
                        total_session_num += 1
                    if line0 == 2:
                        if Session_conclude_flag == 1:
                            continue
                        else:
                            Session_conclude_flag = 1
                            print(f"Received: {line}\n")
                            total_sit_fail_num += 1
                            show_on_second_monitor(screen,red_color,1.5)
                    if line0 == 3:
                        if Session_conclude_flag == 1:
                            continue
                        else:
                            Session_conclude_flag = 1
                            show_on_second_monitor(screen,gray_color,1.5)
                            print(f"Received: {line}\n")
                            continue
                    if line0 == 4:
                        Session_conclude_flag = 0
                        success_rate = (total_session_num-total_sit_fail_num)/total_session_num
                        print(f"Current sitting still: {total_session_num-total_sit_fail_num} / {total_session_num}, success rate: {success_rate}\n")
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
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
