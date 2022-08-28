from threading import Thread
import pygame
from PIL import Image, ImageDraw


pygame.init()  # Initialise pygame
#pygame.mouse.set_visible(False) #hide the mouse cursor

display_info = pygame.display.Info()
#display_width = display_info.current_w
#display_height = display_info.current_h
display_width = 800
display_height = 480

screen = pygame.display.set_mode((display_width,display_height))

background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert() # convert from generic pixel format the pixel format of the user's screen

screenPicture = pygame.display.set_mode((display_info.current_w,display_info.current_h), pygame.FULLSCREEN)  # Full screen
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background

