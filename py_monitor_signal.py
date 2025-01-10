import pygame
import sys
import time

def show_on_second_monitor(screen,color_code,resume_time):
    green_color = (0,255,0)
    screen.fill(color_code)
    pygame.display.flip()
    time.sleep(resume_time)
    screen.fill(green_color)
    pygame.display.flip()
    
