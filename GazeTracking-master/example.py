"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import sys


import cv2
import pygame
from pygame import KEYDOWN, K_ESCAPE, K_q, K_BACKSPACE
from pygame.rect import Rect
from pygments.styles.paraiso_dark import BLUE, RED

from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
# screen = pygame.display.set_mode([1280, 720])
screen = pygame.display.set_mode((1280, 720), 0, 32)
screen.fill([0, 0, 0])

base_font = pygame.font.Font(None, 32)
user_text = ''
input_rect = pygame.Rect(900, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive

active = False

blocked = True

while True:
    ret, frame = webcam.read()
    gaze.refresh(frame)
    frame = gaze.annotated_frame()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame, 0)
    # frame = frame.swapaxes(0, 1)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (20, 50))

    move = ""

    if gaze.is_blinking():
        move = "Blinking"
        blocked = True

    elif gaze.is_right():
        move = "Looking right"
        blocked = True

    elif gaze.is_left():
        move = "Looking left"
        blocked = True

    elif gaze.is_center():
        move = "Looking center"
        blocked = False

    font1 = pygame.font.SysFont('chalkduster.ttf', 50)
    img1 = font1.render(move, True, BLUE)
    screen.blit(img1, (20, 50))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == KEYDOWN:
            if blocked is False:
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

            if event.key == K_ESCAPE or event.key == K_q:
                sys.exit(0)
    if active:
        color = color_active
    else:
        color = color_passive

    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    pygame.display.update()

cv2.destroyAllWindows()
