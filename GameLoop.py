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
    def __init__(self, array, FEN, outName):
        pygame.init()
        self.converter = RepConversion()
        self.game_display = self.makeDisplay(1600, 1200)
        self.graphics = Graphics(self.game_display, array, FEN, outName)#, self.converter.arr)
        self.bb = BB2(FEN)
        self.mouse = Mouse(self.graphics.coor, self.graphics.square_len)
        self.bb.getArray()
        ##FOR TESTING PURPOSES
        #ans = input('Enter answer file: ')
        #t = Test(array, ans)
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
                            self.graphics.x = movingPiece
                            self.graphics.y = self.mouse.mouse_loc(mousecoor)
                            print("piece moved to ", self.mouse.mouse_loc(mousecoor))
                        else:
                            sq = self.mouse.mouse_loc(mousecoor)
                            if self.graphics.p.at(sq):
                                makingMove = True
                                movingPiece = sq
                            print(movingPiece)
            
            self.graphics.button('Submit Move', 40, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY, self.graphics.submitMove)
            self.graphics.button('Finish', 240, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY, self.graphics.finish)
            self.graphics.button('Capture Image', 440, 720, 150, 50,
                            self.graphics.c.GRAY, self.graphics.c.BRIGHT_GRAY, self.graphics.getJPEG)
            # click = pygame.mouse.get_pressed()  # tuple of 3 elements
    
            pygame.display.update()  # updates entire surface, or flip
            #clock.tick(60)  # frames per second
 
def readIn(file):
    f = open(file, 'r')
    rc = RepConversion()
    line = f.readline().rstrip('\n')
    pos = rc.FENtoArray(line)
    f.close()
    return pos, line

def main():
    name = input('Enter input file: ')
    outName = input('Enter output file: ')
    r = readIn(name)
    array = r[0]
    FEN = r[1]
    gl = GameLoop(array, FEN, outName)

if __name__ == '__main__':
    main()
    