#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 19:28:05 2021

@author: sophiecolumbia
"""

import pygame

class Text():
    def __init__(self):
        self.small_txt = pygame.font.Font('freesansbold.ttf', 15)
        self.med_txt = pygame.font.Font('freesansbold.ttf', 20)
        self.large_txt = pygame.font.Font('freesansbold.ttf',30)
        self.BLACK = (0,0,0)
        
    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.BLACK)
        return textSurface, textSurface.get_rect()

    # def message_display(self, text):
    #     display_width, display_height = 2
        
    #     TextSurf, TextRect = self.text_objects(text, self.large_txt)
    #     TextRect.center = (display_width / 2, display_height / 2)
    #     game_display.blit(TextSurf, TextRect)
    #     pygame.display.update()