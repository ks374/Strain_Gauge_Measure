import pygame
import sys
import time

def show_on_second_monitor(screen,color_code,resume_time):
    screen_width,screen_height = screen.get_size()
    screen.fill(color_code)
    pygame.display.flip()
    time.sleep(resume_time)
    screen.fill((128,128,128))
    pygame.draw.circle(screen,(255, 255, 255),(screen_width//2,screen_height//2),50)
    #pygame.draw.circle(screen,circle_color,(screen_width//2,screen_height//2),circle_radius)
    pygame.display.flip()
