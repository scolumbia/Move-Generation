#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 11:56:19 2021

@author: sophiecolumbia
"""

import pygame
import sys
from Graphics import Graphics
from Graphics import Mouse
from RepConversion import RepConversion
from BB2 import BB2
from Test import Test

class GameLoop():
    def __init__(self, array):
        pygame.init()
        self.converter = RepConversion()
        self.game_display = self.makeDisplay(1600, 1200)
        self.graphics = Graphics(self.game_display, array)#, self.converter.arr)
        self.bb = BB2(self.converter.arrayToFEN(self.graphics.getPositionArray()))
        self.mouse = Mouse(self.graphics.coor, self.graphics.square_len)
        self.bb.getArray()
        ##FOR TESTING PURPOSES
        #ans = input('Enter answer file: ')
        #t = Test(array, ans)
        self.bb.makeMove()
        self.game_loop()
        
    def makeDisplay(self, display_width, display_height):
        game_display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('Chess')  # title of game
        #clock = pygame.time.Clock()  # game clock
        return game_display   
    
    
    def game_loop(self):
        makingMove = False
        movingPiece = ()
        while True:
            for event in pygame.event.get():  # gets any event
                if event.type == pygame.QUIT:  # x of window
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousecoor = pygame.mouse.get_pos()
                    if self.mouse.in_board(mousecoor):
                        if makingMove:
                            makingMove = False
                            self.graphics.move_piece((movingPiece), (self.mouse.mouse_loc(mousecoor)))
                            # for line in self.graphics.p.pos_arr:
                            #     print(line)
                            # print()
                            #print("move done at", mouse.mouse_loc(mousecoor))
                        else:
                            sq = self.mouse.mouse_loc(mousecoor)
                            if self.graphics.p.at(sq):
                                makingMove = True
                                movingPiece = sq
                            #print(movingPiece)
            
            self.graphics.button('Undo', 40, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY, self.graphics.undo)
            self.graphics.button('Redo', 240, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY)
            self.graphics.button('New Game', 440, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY)
            self.graphics.button('Flip', 640, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY)
            self.graphics.button('Capture Image', 840, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY, self.graphics.getJPEG)
            # click = pygame.mouse.get_pressed()  # tuple of 3 elements
    
            pygame.display.update()  # updates entire surface, or flip
            #clock.tick(60)  # frames per second
# game_intro()
 
def readIn(file):
    f = open(file, 'r')
    rc = RepConversion()
    line = f.readline().rstrip('\n')
    pos = rc.FENtoArray(line)
    f.close()
    return pos

if __name__ == '__main__':
    name = input('Enter input file: ')
    array = readIn(name)
    gl = GameLoop(array)







# def game_intro():
#     intro = True
#     while intro:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         game_display.fill(WHITE)
#         TextSurf, TextRect = text_objects('Chess', large_txt)
#         TextRect.center = (display_width / 2, display_height / 2)
#         game_display.blit(TextSurf, TextRect)
#         pygame.display.update()
#         clock.tick(15)
