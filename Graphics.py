#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 19:03:17 2021

@author: sophiecolumbia
"""
import pygame


class Graphics():

    def __init__(self, game_display, pos_array):
        '''
        Constructor for Graphics. Accepts the display object of the game to write
        graphics to, as well as a 2D string array of the current position of pieces starting 
        from the upper left corner
        '''
        pygame.init()
        
        self.c = Colors()
        self.t = Text()
        
        self.width = game_display.get_size()[0]
        self.height = game_display.get_size()[1]
        self.game_display = game_display
        self.coor = (40, 30) #top left corner of board
        self.square_len = 75
        self.p = Pieces(pos_array) #2d array of strings, each representing a piece. Space for empty squares
        self.board = Board(self.square_len, self.coor, game_display)
        
        self.init_screen()
    
    def getPositionArray(self):
        return self.p.getPos_Arr()
    
    def init_screen(self):
        '''
        Initializes the screen and calls necessary functions to do so.
        '''
        self.game_display.fill(self.c.WHITE)  # before you have images
        self.draw_labels()
        self.board.draw_board()
        self.p.draw_all(self.board)
        self.init_gamelog()
        pygame.display.update()

    def init_gamelog(self):
        '''
        Draws the game log on game display.
        '''
        board_height = self.square_len * 8
        end_board = self.coor[0] + board_height
        wh = (150, board_height - 20)
        c = (((self.width + end_board) / 2) - (wh[0] / 2), 50)
        log = pygame.Surface(wh)
        log.fill(self.c.NAVY)
        self.game_display.blit(log, c)

        TextSurf, TextRect = self.t.text_objects('Game Log', self.t.small_txt)
        TextRect.center = (c[0] + (wh[0] / 2), (c[1] - 25))
        self.game_display.blit(TextSurf, TextRect)

    def draw_labels(self):
        '''
        Draws alpabetical letters on botton and numbers on side.
        '''
        bottom_letters = 'abcdefgh'
        y = (8 * self.square_len) + self.coor[1] + (self.square_len / 5)  # stays constant
        x = (self.square_len / 2) + self.coor[0]
        for letter in bottom_letters:
            TextSurf, TextRect = self.t.text_objects(letter, self.t.med_txt)
            TextRect.center = (x, y)
            self.game_display.blit(TextSurf, TextRect)
            x += self.square_len

        side_numbers = '12345678'
        x = self.coor[0] - (self.square_len / 5)
        y = (self.square_len / 2) + self.coor[1]
        for num in side_numbers[::-1]:  # reverse string
            TextSurf, TextRect = self.t.text_objects(num, self.t.med_txt)
            TextRect.center = (x, y)
            self.game_display.blit(TextSurf, TextRect)
            y += self.square_len

    def button(self, msg, x, y, w, h, inact, act, action=None):
        '''
        Accepts message for button to display, the x and y position, the
        button's width and height, the inactive color, and the active color
        '''
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()  # tuple of 3 elements

        if (x < mouse[0] < x + w and y < mouse[1] < y + h):
            pygame.draw.rect(self.game_display, act, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(self.game_display, inact, (x, y, w, h))

        textSurf, textRect = self.t.text_objects(msg, self.t.med_txt)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.game_display.blit(textSurf, textRect)

    def undo(self):
        return None
    
    def getJPEG(self):
        filename = input('Enter file name (.jpeg only): ')
        path = 'images/'
        pygame.image.save(self.board.surf, path + filename)#'boardstate.jpeg')
    
    def move_piece(self, init, to):
        '''
        Accepts two tuples, the init and to. Move piece from init to to. Each tuple
        contains row and column value.
        '''
        self.board.draw_square(init[0], init[1])
        self.board.draw_square(to[0], to[1])
        self.p.move(init, to, self.board)
    
    def updateFromBB(self, array):
        self.p.drawAll(arr=array)



class Pieces():
    def __init__(self, pos_array):
        '''
        Accepts a 2D array of strings representative of starting board state
        '''
        self.pos_arr = pos_array
        self.image = pygame.image.load('pieces.png')
        self.image = pygame.transform.scale(self.image, (600, 350))
    
    def getPos_Arr(self):
        return self.pos_arr
    
    def draw_all(self, board, arr=None):
        '''
        Accepts board object that will have all pieces drawn on according to
        the pos_array if an alternative 2d array is not passed.
        '''
        if arr is None:
            arr = self.pos_arr
        for row in range(len(arr)):
            for col in range(len(arr)):
                self.draw(arr[row][col], (row, col), board)
                
    def at(self, coor):
        '''
        Accepts space on board represented as a tuple (row, col).
        Returns True if square is occupied, False otherwise
        '''
        return self.pos_arr[coor[0]][coor[1]] != ' '
        
    def move(self, init, to, board):
        '''
        Accpts tuples init and to, coordinates of the piece before the move and
        after the move. Also accepts board object of which to draw on. 
        Makes move appear on screen.
        '''
        #change pos arr
        moving_piece = self.pos_arr[init[0]][init[1]]
        if moving_piece == ' ':
            return
        self.pos_arr[init[0]][init[1]] = ' '
        self.pos_arr[to[0]][to[1]] = moving_piece
        #blit onto surf
        self.draw(moving_piece, to, board)
    
    def draw(self, piece, dest, board):
        '''
        Accepts piece (string of the piece being moved is), dest (tuple of where
                                                                  the piece is moving to),
        and board object to draw on. 
        Draws the moving piece at its destination.
        '''
        x = dest[1] * board.sq_len
        y = dest[0] * board.sq_len + (board.sq_len / 10)
        w = self.image.get_width() / 10
        space = self.image.get_width() / 12
        h = self.image.get_height() / 4
        if piece == 'r':
            crop = (space * 2 + w * 2, h, w, h)
        elif piece == 'R':
            crop = (space * 2 + w * 2, h * 2 + h/4 , w, h)
        elif piece == 'n':
            crop = (space * 4 + w * 4, h, w, h)
        elif piece == 'N':
            crop = (space * 4 + w * 4, h * 2 + h/4, w, h)
        elif piece == 'b':
            crop = (w * 3 + space * 3, h, w, h)
        elif piece == 'B':
            crop = (w * 3 + space * 3, h * 2 + h/4, w, h)
        elif piece == 'q':
            crop = (w + space, h, w, h)
        elif piece == 'Q':
            crop = (w + space, h * 2 + h/4, w, h)
        elif piece == 'k':
            crop = (0, h, w, h)
        elif piece == 'K':
            crop = (0, h * 2 + h/4, w, h)
        elif piece == 'p':
            crop = (5 * space + 5 * w, h, w, h)
        elif piece == 'P':
            crop = (5 * space + 5 * w, h * 2 + h/4, w, h)
        if piece != ' ':
            board.surf.blit(self.image, (x + ((board.sq_len - w) / 2), y + ((board.sq_len - h) / 2)), crop)
            board.surf.blit(self.image, (x + ((board.sq_len - w) / 2), y + ((board.sq_len - h) / 2)), crop)
        board.update()


 
class Board():
    def __init__(self, sq_len, coor, game_display):
        '''
        Accept int of the length of each square on the board, the coordinates of
        the top left corner of the board as a tuple, and the game display.
        '''
        self.c = Colors()
        self.coor = coor
        self.game_display = game_display
        self.sq_len = sq_len
        self.surf = pygame.Surface((sq_len * 8, sq_len * 8))
        self.draw_board()
        
    def update(self):
        '''
        Updates the board so that changes are visible.
        '''
        self.game_display.blit(self.surf, self.coor)
        
    def draw_board(self):
        '''
        Takes in the tuple containing top left coordinates of board.
        Draws entire board.
        '''
        for row in range(8):
            for col in range(8):
                self.draw_square(row, col)
        self.game_display.blit(self.surf, self.coor)
                
    def draw_square(self, row, col):
        '''
        Takes two int values, row and col. Note: top left corner of board is 0, 0
        Draws a square of the correct color in the specified row and column
        '''
        if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
            pygame.draw.rect(self.surf, self.c.LIGHT_BROWN, (self.sq_len * col,
                                                                  + self.sq_len * row,
                                                                  self.sq_len, self.sq_len))
        else:
            pygame.draw.rect(self.surf, self.c.DARK_BROWN, (self.sq_len * col,
                                                                  + self.sq_len * row,
                                                                  self.sq_len, self.sq_len))
        self.update()
     
            
class Mouse():
    def __init__(self, coor, sq_len):
        '''
        Accept tuple of coordinates top left of board and the length of each square.
        '''
        self.board_start = coor
        self.sq_len = sq_len
    
    def mouse_loc(self, loc):
        '''
        Accept tuple of click's coordinates.
        Returns tuple of the row and column the click occured in.
        '''
        row = (loc[1] - self.board_start[1]) // self.sq_len
        col = (loc[0] - self.board_start[0]) // self.sq_len
        return (row, col)

    def in_board(self, loc):
        '''
        Accept tuple of click's coordinates.
        Returns T/F based on whether or not a square on board was clicked.
        '''
        return (self.board_start[0] < loc[0] < self.board_start[0] + 8 * self.sq_len
                        and self.board_start[1] < loc[1] < self.board_start[1] + 8 * self.sq_len)
    

class Button():
    def __init__(self):
        return
    
class Colors():
    '''
    Class that is a holder for color's RGB values
    '''
    def __init__(self):
        self.BLACK = (0, 0, 0)  # RGB
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.DARK_BROWN = (139, 69, 19)
        self.LIGHT_BROWN = (205, 133, 63)
        self.GRAY = (100, 116, 132)
        self.BRIGHT_GRAY = (124, 140, 166)
        self.NAVY = (1, 37, 94)
        
        
class Text():
    '''
    Class that deals with text and its font for pygame.
    '''
    def __init__(self):
        self.small_txt = pygame.font.Font('freesansbold.ttf', 15)
        self.med_txt = pygame.font.Font('freesansbold.ttf', 20)
        self.large_txt = pygame.font.Font('freesansbold.ttf', 30)
        self.c = Colors()
        
    def text_objects(self, text, font):
        '''
        Accepts text to be displayed and the desired font.
        Returns two items: the text surface and the rectangle of the text
        '''
        textSurface = font.render(text, True, self.c.BLACK)
        return textSurface, textSurface.get_rect()
    