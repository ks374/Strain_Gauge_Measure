import pygame
import sys
import time

def show_on_second_monitor(screen,color_code,resume_time):
    screen.fill(color_code)
    pygame.display.flip()
    time.sleep(resume_time)
    screen.fill(gray_color)
    pygame.draw.circle(screen,circle_color,(screen_width//2,screen_height//2),circle_radius)
    pygame.display.flip()