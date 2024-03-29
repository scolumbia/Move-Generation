#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Jun  9 18:39:41 2021
Updated BB with unsigned ints.

@author: sophiecolumbia
"""
import numpy as np

# uints to be used in safe unsigned operations
zero = np.uint64(0)
one = np.uint64(1)
two = np.uint64(2)
three = np.uint64(3)
four = np.uint64(4)
five = np.uint64(5)
six = np.uint64(6)
seven = np.uint64(7)
eight = np.uint64(8)
nine = np.uint64(9)
sixteen = np.uint64(16)
eighteen = np.uint64(18)
fifty_six = np.uint64(56)
sixty_three = np.uint64(63)

knightMask = np.uint64(43234889994)
kingMask = np.uint64(460039)
rook_castle = (zero, seven, fifty_six, sixty_three)

fileA = np.uint64(9259542123273814144)
fileH = np.uint64(72340172838076673)
fileAB = np.uint64(13889313184910721216)
fileGH = np.uint64(217020518514230019)
rank1 = np.uint64(255)
rank4 = np.uint64(4278190080)
rank5 = np.uint64(1095216660480)
rank8 = np.uint64(18374686479671623680)
 
rankMasks = [0xff, 0xff00, 0xff0000,
                   0xff000000, 0xff00000000, 0xff0000000000,
                   0xff000000000000, 0xff00000000000000]
rankMasks = [np.uint64(num) for num in rankMasks]
#file A - B
fileMasks = [0x8080808080808080, 0x4040404040404040, 0x2020202020202020,
                   0x1010101010101010, 0x0808080808080808, 0x0404040404040404,
                   0x0202020202020202, 0x0101010101010101]
fileMasks = [np.uint64(num) for num in fileMasks]
 
diagonalMasks = [0x1, 0x102, 0x10204, 0x1020408, 0x102040810, 0x10204081020, 0x1020408102040,
                       0x102040810204080, 0x204081020408000, 0x408102040800000, 0x810204080000000,
                       0x1020408000000000, 0x2040800000000000, 0x4080000000000000, 0x8000000000000000]
diagonalMasks = [np.uint64(num) for num in diagonalMasks]
 
antiDiagonalMasks = [0x80, 0x8040, 0x804020, 0x80402010, 0x8040201008, 0x804020100804, 0x80402010080402,
                           0x8040201008040201, 0x4020100804020100, 0x2010080402010000, 0x1008040201000000,
                           0x804020100000000, 0x402010000000000, 0x201000000000000, 0x100000000000000]
antiDiagonalMasks = [np.uint64(num) for num in antiDiagonalMasks]

class BB2():
    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        '''
        Creates an instance of a set of bitbords.
        Accepts FEN notation of current game's state.
        '''
        self.id = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5,
                       'P': 6, 'N': 7, 'B': 8, 'R': 9, 'Q': 10, 'K': 11}
        self.bb = []
        self.move_history = []
        self.whiteTurn = True
        self.castle_wk = True
        self.castle_wq = True
        self.castle_bk = True
        self.castle_bq = True
        self.parse_fen(fen)
        self.white_in_check = []
        self.black_in_check = []
        
    def test_generate_moves(self):
        '''
        Generates all possible moves (both white and black) and writes them out to separate files.
        '''
        self.whiteTurn = True
        white_moves = ''
        white_moves += self.wpMoves() + self.rMoves()+ self.nMoves() + self.bMoves() + self.kMoves() + self.qMoves() + self.poss_castle_white()
        self.writeMoveList('white_moves.txt', white_moves)

        self.whiteTurn = False
        black_moves = ''
        black_moves += self.bpMoves() + self.rMoves()+ self.nMoves() + self.bMoves() + self.kMoves() + self.qMoves() + self.poss_castle_black()
        self.writeMoveList('black_moves.txt', black_moves)

    def make_move(self):
        '''
        Beginnings for the code that actually makes a move.
        '''
        pass
        self.whiteTurn = not self.whiteTurn

    def generate_moves(self):
        '''
        Generates moves for current color. Returns an empty string if checkmate.
        '''
        checking_pieces = self.check()
        if len(checking_pieces) != 0: #king is in check
            return self.in_check_gen(checking_pieces)
        else:
            return self.reg_gen()
    
    def in_check_gen(self, checking_pieces):
        '''
        Generates possible moves when king is in check.
        Takes checking_pieces (str), result of check function. E.g. b56
        '''
        if self.whiteTurn:
            king_loc = self.king_coords('K')
        else:
            king_loc = self.king_coords('k')
        all_moves = self.reg_gen()
        all_list = [all_moves[i:i+4] for i in range(0, len(all_moves), 4)]
        legal_moves = ''
        # only one piece is attacking
        if len(checking_pieces) == 3:
            if checking_pieces[0].lower() != 'n' and checking_pieces[0].lower() != 'p' and checking_pieces[0].lower() != 'k': #attacking piece is not a knight
                #block the attacking piece
                legal_moves += self.block_check(all_list, checking_pieces, king_loc)
            #capture attacking piece
            legal_moves += self.take_check(all_list, checking_pieces)
        #move king to safety
        legal_moves += self.kMoves()
        return legal_moves
    
    def take_check(self, moves, checking_pieces):
        '''
        Returns as a str the moves in which would result in the checking piece being taken.
        Accepts moves (list of all moves as str) and checking pieces (str)
        '''
        poss = []
        square = checking_pieces[1:]
        for move in moves:
            c = move[2:]
            if c == square:
                poss.append(move)
        return ''.join(poss)
    
    def block_check(self, moves, checking_pieces, king_loc):
        '''
        Returns as a str the moves in which would result in the checking piece's attack being blocked.
        Accepts moves (list of all moves as str) and checking pieces (str)
        '''
        print(checking_pieces)
        print(king_loc)
        legal_moves = ''
        if checking_pieces[0].lower() == 'r' or (checking_pieces[0].lower() == 'q' and (king_loc[0] == checking_pieces[1] or king_loc[1] == checking_pieces[2])):
            #print('looking for block ')
            #same row
            if king_loc[0] == checking_pieces[1]:
                row = king_loc[0]
                for move in moves:
                    if move[2] == row:
                        if (int(king_loc[1]) < int(move[3]) < int(checking_pieces[2])) or (int(checking_pieces[2]) < int(move[3]) < int(king_loc[1])):
                            legal_moves += move
            #same col
            if king_loc[1] == checking_pieces[2]:
                #print('same col')
                col = king_loc[1]
                for move in moves:
                    if move[3] == col:
                        if (int(king_loc[0]) < int(move[2]) < int(checking_pieces[1])) or (int(checking_pieces[1]) < int(move[2]) < int(king_loc[0])):
                            legal_moves += move
        elif checking_pieces[0].lower() == 'b' or checking_pieces[0].lower() == 'q':
            crow = int(checking_pieces[1])
            ccol = int(checking_pieces[2])
            krow = int(king_loc[0])
            kcol = int(king_loc[1])
            #top left
            blocking_squares = []
            if crow < krow and ccol < kcol:
                while crow + 1 != krow:
                    ccol += 1
                    crow += 1
                    blocking_squares.append(str(crow) + str(ccol))
            #bottom left
            elif crow > krow and ccol < kcol:
                while crow - 1 != krow:
                    ccol += 1
                    crow -= 1
                    blocking_squares.append(str(crow) + str(ccol))
            #top right
            elif crow < krow and ccol > kcol:
                while crow + 1 != krow:
                    ccol -= 1
                    crow += 1
                    blocking_squares.append(str(crow) + str(ccol))
            #bottom right
            elif crow > krow and ccol > kcol:
                while crow - 1 != krow:
                        ccol -= 1
                        crow -= 1
                        blocking_squares.append(str(crow) + str(ccol))
            for move in moves:
                if move[-2:] in blocking_squares:
                    legal_moves += move
        return legal_moves
        
    def reg_gen(self):
        '''
        Move generation function for when king is not in check.
        '''
        moves = ''
        if self.whiteTurn:
            moves += self.wpMoves()
        else:
            moves += self.bpMoves()
        moves += self.rMoves()
        moves += self.nMoves()
        moves += self.bMoves()
        moves += self.qMoves()  
        return moves
    
    def check(self):
        '''
        Generates a string with 3 chars denoting each attacking piece (eg P78).
        '''
        self.whiteTurn = not self.whiteTurn
        if self.whiteTurn:
            check_list = self.black_check()
        else:
            check_list = self.white_check()
        self.whiteTurn = not self.whiteTurn
        return check_list
        
    def black_check(self):
        '''
        Finds all moves in which the target is the location of the black king.
        Returns the attack list, str with 3 chars denoting attacking piece.
        '''
        #print('in black check')
        attack_list = ''
        king_loc = self.king_coords('k')
        p = self.wpMoves()
        attack_list += self.attacking_king(p, king_loc, 'P')
        r = self.rMoves()
        attack_list += self.attacking_king(r, king_loc, 'R')
        n = self.nMoves()
        attack_list += self.attacking_king(n, king_loc, 'N')
        b = self.bMoves()
        attack_list += self.attacking_king(b, king_loc, 'B')
        q = self.qMoves()
        attack_list += self.attacking_king(q, king_loc, 'Q')
        return attack_list
        
    def white_check(self):
        '''
        Finds all moves in which the target is the location of the white king.
        Returns the attack list, str with 3 chars denoting attacking piece.
        '''
        attack_list = ''
        king_loc = self.king_coords('K')
        p = self.bpMoves()
        attack_list += self.attacking_king(p, king_loc, 'p')
        r = self.rMoves()
        attack_list += self.attacking_king(r, king_loc, 'r')
        n = self.nMoves()
        attack_list += self.attacking_king(n, king_loc, 'n')
        b = self.bMoves()
        attack_list += self.attacking_king(b, king_loc, 'b')
        q = self.qMoves()
        attack_list += self.attacking_king(q, king_loc, 'q')
        return attack_list
    
    def attacking_king(self, move_list, king_coord, piece_checking):
        '''
        Returns a str, with every 3 chars denoting an attacking piece's type and location.
        '''
        moves = [move_list[i:i+4] for i in range(0, len(move_list), 4)]
        attack_origin = ''
        for move in moves:
            if move[2:] == king_coord:
                #print('attack founbd')
                attack_origin += piece_checking + move[0:2]
        return attack_origin
        
    def king_coords(self, king):
        '''
        Returns string of the xy location of the king based on the passed char ('k' or 'K')
        '''
        index = self.trailingZeros(self.bb[self.id[king]])
        coords = str(7 - index // 8) + str(7 - index % 8)
        return coords
    
    def diagonalMoves(self, s):
        '''
        Helper function for move generation for bishops and queens. Calculates rays of attacks.
        Accepts s, int of # of trailing zeroes of sliding piece to be checked.
        '''
        diagMask = diagonalMasks[(s // 8) + (s % 8)]
        antiMask = antiDiagonalMasks[(s // 8) + 7 - (s % 8)]
        binRep = np.uint64(1 << s)
        occupied = self.getOccupied()
        
        d0 = np.subtract(occupied & diagMask, np.multiply(two, binRep))
        d1 = self.unsignedReverse(np.subtract(self.unsignedReverse(occupied & diagMask), np.multiply(two, self.unsignedReverse(binRep))))
        diagPoss = d0 ^ d1
        a0 = np.subtract(occupied & antiMask, np.multiply(two, binRep))
        a1 = self.unsignedReverse(np.subtract(self.unsignedReverse(occupied & antiMask), np.multiply(two, self.unsignedReverse(binRep))))
        antiPoss = a0 ^ a1
        return (diagPoss & diagMask) | (antiPoss & antiMask)
        
    def rowMoves(self, s):
        '''
        Helper function for move generation for rooks and queens. Calculates rays of attacks.
        Accepts s, int of # of trailing zeroes of sliding piece to be checked.
        '''
        rankMask = rankMasks[s // 8]
        fileMask = fileMasks[7 - s % 8]
        binRep = np.uint64(1 << s)
        occupied = self.getOccupied()
        
        h0 = np.subtract(occupied, np.multiply(two, binRep))
        h1 = self.unsignedReverse(np.subtract(self.unsignedReverse(occupied), np.multiply(two, self.unsignedReverse(binRep))))
        horizPoss = h0 ^ h1
        v0 = np.subtract(occupied & fileMask, np.multiply(two, binRep))
        v1 = self.unsignedReverse(np.subtract(self.unsignedReverse(occupied & fileMask), np.multiply(two, self.unsignedReverse(binRep))))
        vertPoss = v0 ^ v1
        
        return (horizPoss & rankMask) | (vertPoss & fileMask)
    
    def wpMoves(self, history=None, check=False):
        '''
        Generates white pawn moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        check_poss = 0
        P = self.bb[self.id['P']]
        blackPieces = self.getBlackPieces()
        occ = self.getOccupied()
        empty = ~occ
        #capture right diagonal
        x = int((np.left_shift(P, seven)) & blackPieces & occ & ~rank8 & ~fileA)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y) #find index of least 1
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 - 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #capture left diagonal
        x = int((np.left_shift(P, nine)) & blackPieces & occ & ~rank8 & ~fileH)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 + 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move one forward
        x = int((np.left_shift(P, eight)) & empty & ~rank8)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move two forward (pawn still in initial position)
        x = int((np.left_shift(P, sixteen)) & empty & (np.left_shift(empty, eight)) & rank4)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 2) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        # PAWN PROMOTION
        # P, piece promotion (R, B, N, Q), y1, y2 (x coordinates are unneccessary)
        #pawn promotion: capture right
        x = int((np.left_shift(P, seven)) & blackPieces & occ & rank8 & ~fileA)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion right')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 - 1)
            y2 = str(7 - index % 8)
            moveList += 'PR' + y1 + y2 + 'PB' + y1 + y2 + 'PN' + y1 + y2 + 'PQ' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: capture left
        x = int((np.left_shift(P, nine)) & blackPieces & occ & rank8 & ~fileH)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion left')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 + 1)
            y2 = str(7 - index % 8)
            moveList += 'PR' + y1 + y2 + 'PB' + y1 + y2 + 'PN' + y1 + y2 + 'PQ' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: one forward
        x = int((np.left_shift(P, eight)) & ~occ & rank8)
        check_poss |= x
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion forward')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8)
            y2 = str(7 - index % 8)
            moveList += 'PR' + y1 + y2 + 'PB' + y1 + y2 + 'PN' + y1 + y2 + 'PQ' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        # y1,y2, 'WE'
        #en passant to the right
        EP = np.uint64(self.en_passant())
        x = int(np.right_shift(P, one) & self.bb[self.id['p']] & rank5 & ~fileA & EP)
        check_poss |= x
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'WE'
    
    
        #en passant to the left
        x = int(np.left_shift(P, one) & self.bb[self.id['p']] & rank5 & ~fileH & EP)
        check_poss |= x
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'WE'
        #self.writeMoveList('whitePawn.txt', moveList)
        return moveList#, check_poss
    
    def bpMoves(self, history=None):
        '''
        Generates black pawn moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        whitePieces = self.getWhitePieces()
        occ = self.getOccupied()
        empty = ~occ
        p = self.bb[self.id['p']]
        #capture right diagonal
        x = int((np.right_shift(p, seven)) & whitePieces & occ & ~rank1 & ~fileH)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y) #find index of least 1
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8 + 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #capture left diagonal
        x = int((np.right_shift(p, nine)) & whitePieces & occ & ~rank1 & ~fileA)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8 - 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move one forward
        x = int((np.right_shift(p, eight)) & empty & ~rank1)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move two forward (pawn still in initial position)
        x = int((np.right_shift(p, sixteen)) & empty & (np.right_shift(empty, eight)) & rank5)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 2) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        # PAWN PROMOTION
        # P, piece promotion (R, B, N, Q), y1, y2 (x coordinates are unneccessary)
        #pawn promotion: capture right
        x = int((np.right_shift(p, seven)) & whitePieces & occ & rank1 & ~fileH)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion right')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 + 1)
            y2 = str(7 - index % 8)
            moveList += 'pr' + y1 + y2 + 'pb' + y1 + y2 + 'pn' + y1 + y2 + 'pq' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: capture left
        x = int((np.right_shift(p, nine)) & whitePieces & occ & rank1 & ~fileA)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion left')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 - 1)
            y2 = str(7 - index % 8)
            moveList += 'pr' + y1 + y2 + 'pb' + y1 + y2 + 'pn' + y1 + y2 + 'pq' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: one forward
        x = int((np.right_shift(p, eight)) & ~occ & rank1)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            #print('promotion forward')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8)
            y2 = str(7 - index % 8)
            moveList += 'pr' + y1 + y2 + 'pb' + y1 + y2 + 'pn' + y1 + y2 + 'pq' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        # y1,y2, 'BE'
        #always rank 4 to rank 3, all that matters is file
        #en passant to the right
        EP = np.uint64(self.en_passant())
        #print(EP)
        x = int(np.left_shift(p, one) & self.bb[self.id['P']] & rank4 & ~fileH & EP)
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'BE'
    
    
        #en passant to the left
        x = int(np.right_shift(p, one) & self.bb[self.id['P']] & rank4 & ~fileA & EP)
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'BE'
        
        #self.writeMoveList('blackPawn.txt', moveList)
        return moveList
    
    def bMoves(self):
        '''
        Generates bishop moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            B = int(self.bb[self.id['B']])
        else:
            B = int(self.bb[self.id['b']])
        i = B & ~(B - 1)
        while (i != 0):
            iLoc = self.trailingZeros(i)
            poss = int(self.diagonalMoves(iLoc) & ~movePieces)
            #self.drawBin(poss)
            j = poss & ~(poss - 1)
            while (j != 0):
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            B = B & ~i
            i = B & ~(B - 1)
        #self.writeMoveList('black_bishop.txt', moveList)
        return moveList
        
    def nMoves(self):
        '''
        Generates knight moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            N = int(self.bb[self.id['N']])
        else:
            N = int(self.bb[self.id['n']])
        i = N & ~(N - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            if iLoc > 18:
                poss = np.left_shift(knightMask, np.subtract(np.uint64(iLoc), eighteen))
            else:
                poss = np.right_shift(knightMask, np.subtract(eighteen, np.uint64(iLoc)))
            if iLoc % 8 < 4:
                poss = poss & ~fileAB & ~movePieces
            else:
                poss = poss & ~fileGH & ~movePieces
            poss = int(poss)
            #self.drawBin(poss)
            #print()
            j = poss & ~(poss - 1)
            while j != 0:
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            N = N & ~i
            i = N & ~(N - 1)
        #self.writeMoveList('black_knight.txt', moveList)
        return moveList
    
    def rMoves(self):
        '''
        Generates rook moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            R = int(self.bb[self.id['R']])
        else:
            R = int(self.bb[self.id['r']])
        i = R & ~(R - 1)
        while (i != 0):
            iLoc = self.trailingZeros(i)
            poss = int(self.rowMoves(iLoc) & ~movePieces)
            j = poss & ~(poss - 1)
            while (j != 0):
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            R = R & ~i
            i = R & ~(R - 1)
        #self.writeMoveList('black_rook.txt', moveList)
        return moveList
    
    def qMoves(self):
        '''
        Generates queen moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            Q = int(self.bb[self.id['Q']])
        else:
            Q = int(self.bb[self.id['q']])
        i = Q & ~(Q - 1)
        while (i != 0):
            iLoc = self.trailingZeros(i)
            poss = int((self.rowMoves(iLoc) | self.diagonalMoves(iLoc)) & ~movePieces)
            #self.drawBin(poss)
            #print()
            j = poss & ~(poss - 1)
            while (j != 0):
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            Q = Q & ~i
            i = Q & ~(Q - 1)
        #self.writeMoveList('black_queen.txt', moveList)
        return moveList
        
    def kMoves(self):
        '''
        Generates king moves.
        Returns str, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).
        '''
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            K = int(self.bb[self.id['K']])
            safe = ~self.unsafeForWhite()
        else:
            K = int(self.bb[self.id['k']])
            safe = ~self.unsafeForBlack()
        iLoc = self.trailingZeros(K)
        #print(iLoc)
        if iLoc > 9:
            poss = np.left_shift(kingMask, np.subtract(np.uint64(iLoc), nine))
        else:
            poss = np.right_shift(kingMask, np.subtract(nine, np.uint64(iLoc)))
        if iLoc % 8 < 4:
            poss = poss & ~fileAB & ~movePieces
        else:
            poss = poss & ~fileGH & ~movePieces
        poss = int(poss & safe)
        j = poss & ~(poss - 1)
        while j != 0:
            index = self.trailingZeros(j)
            moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
            poss = poss & ~j
            #self.drawBin(poss)
            #print()
            j = poss & ~(poss - 1)
        #self.writeMoveList('black_king.txt', moveList)
        return moveList
    
    
    def en_passant(self):
        '''
        Checks to see if an en passant is possible. 0 if impossible, file mask otherwise.
        '''
        board = int(self.getOccupied())
        if len(self.move_history) > 0:
            #print('ep: 1st if')
            last_move = self.move_history[-1] #grab last move from move list
            if last_move[3].isdigit(): #if last move was a regular move
                #print('ep: 2nd if')
                s = (int(last_move[0]) * 8) + int(last_move[1]) 
                if abs(int(last_move[0]) - int(last_move[2])) == 2 and (board >> s) & 1 == 1:
                    #print('ep: 3rd if')
                    #print(int(last_move[1]))
                    return fileMasks[int(last_move[1])]
        return 0
        
    
    def poss_castle_white(self):
        '''
        "One may not castle out of, through, or into check"
        Calculates white castle moves, if possible.
        '''
        move_list = ''
        occ = self.getOccupied()
        K = self.bb[self.id['K']]
        R = self.bb[self.id['R']]
        attacked = self.unsafeForWhite()
        if attacked & K == 0: #check if king is safe
            if self.castle_wk and (((one << rook_castle[0]) & R) != 0): #can still castle and rook is unmoved
                if ((occ | attacked) & (two | four)) == 0: #neither square being passed through is occupied or under attack
                    move_list += '7476'
            if self.castle_wq and ((one << rook_castle[1]) != 0):
                if (occ | (attacked & ~((one << six)))) & ((((one << four)) | (one << five) | (one << six))) == 0:
                    move_list += '7472'
        #self.writeMoveList('castling_white.txt', move_list)
        return move_list
    
    def poss_castle_black(self):
        '''
        Calculates black castle moves, if possible.
        '''
        move_list = ''
        occ = self.getOccupied()
        k = self.bb[self.id['k']]
        r = self.bb[self.id['r']]
        attacked = self.unsafeForBlack()
        if attacked & k == 0:
            if self.castle_bk and (((one << rook_castle[2]) & r) != 0):
                if ((occ | attacked) & ((np.uint64(1 << 57)) | (np.uint64(1 << 58)))) == 0:
                    move_list += '0406'
            if self.castle_bq and ((one  << rook_castle[3]) != 0):
                if (occ | (attacked & ~np.uint64(1 << 62))) & (((np.uint64(1 << 62)) | np.uint64(1 << 61) | np.uint64(1 << 60))) == 0:
                    move_list += '0402'
        #self.writeMoveList('castling_black.txt', move_list)
        return move_list
    
    def parse_fen(self, fen):
        '''
        Interprets FEN from creation of BB object.
        '''
        fen_elements = fen.split(' ')
        self.readPosition(fen_elements[0])
        self.set_turn(fen_elements[1])
        self.castling_rights(fen_elements[2])
        self.ep_target(fen_elements[3])
    
    def ep_target(self, ep):
        '''
        Adds to move_history the en passant target square from FEN input.
        '''
        if ep == '-':
            return
        col = ord(ep[0]) - 97 #calculate using ASCII value
        row = 8 - int(ep[1])
        if row == 5: #white pawn moved forward 2
            s = str(row + 1) + str(col)+ str(row - 1)+ str(col)
        else:
            s = str(row - 1) + str(col)+ str(row + 1)+ str(col)
        self.move_history.append(s)
    
    def castling_rights(self, c):
        '''
        Sets castling rights based upon FEN.
        '''
        if 'K' in c:
            self.castle_wk = True
        if 'Q' in c:
            self.castle_wq = True
        if 'k' in c:
            self.castle_bk = True
        if 'q' in c:
            self.castle_bq = True
    
    def set_turn(self, turn):
        '''
        Sets turn based upon turn in FEN notation.
        '''
        self.whiteTurn = (turn.lower() == 'w')
    
    def readPosition(self, pos):
        '''
        Generates bitboards based on FEN. Most significant bit is the top left corner of the board (A8)
        and 2nd most sigbit is B8. LSB is H1. Pos is str (FEN board portion)
        '''
        bb = [0 for i in range(12)]
        spot = 2**63
        for char in pos:
            # if char is int, num of spaces
            if char.isdigit():
                val = int(char)
                for i in range(val):
                    spot /= 2
                continue
            # char is a piece, not a line break
            elif char != '/':
                bb[self.id[char]] += int(spot)
            if char != '/':
                spot /= 2
        b = [np.uint64(num) for num in bb]
        self.bb = b
        
    def remove_king(self, king_char):
        '''
        Removes king from BB for calculating safe squares for king to move to.
        king_char: 'k' or 'K', depending upon which color is to be removed.
        Returns int denoting prior king's BB.
        '''
        hold_bb = self.bb[self.id[king_char]]
        self.bb[self.id[king_char]] = zero
        return hold_bb
        
    def restore_king(self, king_bb, king_char):
        '''
        Replaces king on BB. Accepts int denoting prior king's BB and char of which
        king is to be restored.
        '''
        self.bb[self.id[king_char]] = king_bb

    def unsafeForBlack(self):
        '''
        Generates BB of squares unsafe for black king to move to.
        '''
        #remove black king
        k_bb = self.remove_king('k')
        #pawn
        P = self.bb[self.id['P']]
        #pawn capture right
        unsafe = (np.left_shift(P, seven) & ~fileA)
        #pawn capture left
        unsafe |= (np.left_shift(P, nine) & ~fileH)
        
        #knight
        N = int(self.bb[self.id['N']])
        i = N & ~(N - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            if iLoc > 18:
                poss = np.left_shift(knightMask, np.subtract(np.uint64(iLoc), eighteen))
            else:
                poss = np.right_shift(knightMask, np.subtract(eighteen, np.uint64(iLoc)))
            if iLoc % 8 < 4:
                poss = poss & ~fileAB
            else:
                poss = poss & ~fileGH
            unsafe |= poss
            N = N & ~i
            i = N & ~(N - 1)
        
        #bishop/queen
        QB = int(self.bb[self.id['Q']] | self.bb[self.id['B']])
        i = QB & ~(QB - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            poss = self.diagonalMoves(iLoc)
            unsafe |= poss
            QB &= ~i
            i = QB & ~(QB - 1)
        
        #rook/queen
        QR = int(self.bb[self.id['Q']] | self.bb[self.id['R']])
        i = QR & ~(QR - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            poss = self.rowMoves(iLoc)
            unsafe |= poss
            QR &= ~i
            i= QR & ~(QR - 1)
        
        #king
        K = self.bb[self.id['K']]
        iLoc = self.trailingZeros(K)
        if iLoc > 9:
            poss = np.left_shift(kingMask, np.subtract(np.uint64(iLoc), nine))
        else:
            poss = np.right_shift(kingMask, np.subtract(nine, np.uint64(iLoc)))
        if iLoc % 8 < 4:
            poss = poss & ~fileAB
        else:
            poss = poss & ~fileGH
        unsafe |= poss
        self.restore_king(k_bb, 'k')
        return unsafe
    
    
    def piece_type(self, square):
        '''
        Returns the piece type occupying square for check.
        square is int value of square on BB (a power of 2).
        Returns char of piece occupying.
        '''
        for piece, num in self.id.items():
            result = square & self.bb[num]
            if result != 0:
                return piece
            
    
    def unsafeForWhite(self):
        '''
        Generates BB of squares unsafe for white king to move to.
        '''
        #remove white king
        k_bb = self.remove_king('K')
        #pawn
        P = self.bb[self.id['p']]
        #pawn capture right
        unsafe = (np.right_shift(P, seven) & ~fileH)
        #pawn capture left
        unsafe |= (np.right_shift(P, nine) & ~fileA)
        
        #knight
        N = int(self.bb[self.id['n']])
        i = N & ~(N - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            if iLoc > 18:
                poss = np.left_shift(knightMask, np.subtract(np.uint64(iLoc), eighteen))
            else:
                poss = np.right_shift(knightMask, np.subtract(eighteen, np.uint64(iLoc)))
            if iLoc % 8 < 4:
                poss = poss & ~fileAB
            else:
                poss = poss & ~fileGH
            unsafe |= poss
            N = N & ~i
            i = N & ~(N - 1)
        
        #bishop/queen
        QB = int(self.bb[self.id['q']] | self.bb[self.id['b']])
        i = QB & ~(QB - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            poss = self.diagonalMoves(iLoc)
            unsafe |= poss
            QB &= ~i
            i = QB & ~(QB - 1)
        
        #rook/queen
        QR = int(self.bb[self.id['q']] | self.bb[self.id['r']])
        i = QR & ~(QR - 1)
        while i != 0:
            iLoc = self.trailingZeros(i)
            poss = self.rowMoves(iLoc)
            unsafe |= poss
            QR &= ~i
            i= QR & ~(QR - 1)
        
        #king
        K = self.bb[self.id['k']]
        iLoc = self.trailingZeros(K)
        if iLoc > 9:
            poss = np.left_shift(kingMask, np.subtract(np.uint64(iLoc), nine))
        else:
            poss = np.right_shift(kingMask, np.subtract(np.uint64(iLoc), nine))
        if iLoc % 8 < 4:
            poss = poss & ~fileAB
        else:
            poss = poss & ~fileGH
        unsafe |= poss
        self.restore_king(k_bb, 'K')
        return unsafe
        
    def reverseBits(self, n):
        '''
        Reverses the order of bits in an int.
        '''
        return int('{:064b}'.format(n)[::-1], 2)
        
    def unsignedReverse(self, n):
        '''
        Reverses the order of a bits in a uint.
        '''
        #print('type of n passed in unsignedReverse:', type(n))
        return np.uint64(int('{:064b}'.format(n)[::-1], 2))

    def trailingZeros(self, num):
        '''
        Returns the count of the number of trailing zeros in a binary representation of an int.
        '''
        s = bin(num)[2::]
        return len(s) - len(s.rstrip('0'))

    def drawbb(self, piece):
        '''
        Draws bitboard of specified piece in a 2D array.
        Accepts str of specified piece to be drawn.
        '''
        rep = [['' for i in range(8)] for j in range(8)]
        for i in range(64):
            if (int(self.bb[self.id[piece]]) >> i) & 1 == 1:
                rep[7 - i // 8][7 - i % 8] = piece
            elif rep[7 - i // 8][7 - i % 8] == '':
                rep[7 - i // 8][7 - i % 8] = ' '
        for row in rep:
            print(row)
        print()
    
    def getArray(self):
        '''
        Returns 2D array based on the bitboards.
        '''
        arr = [[' ' for i in range(8)] for j in range(8)]
        for p in self.id:
            binary = bin(int(self.bb[self.id[p]]))[2::]
            row = 7
            col = 7
            for i in range(len(binary) - 1, -1, -1):
                if binary[i] == '1':
                    arr[row][col] = p
                if col == 0:
                    col = 7
                    row -= 1
                else:
                    col -= 1
        # for row in arr:
        #     print(row)
        return arr
        
    def drawBin(self, n):
        '''
        Accepts an integer n.
        Draws the BB representation of n.
        '''
        rep = [['0' for i in range(8)] for j in range(8)]
        st = bin(n)[2::]
        r = 7
        ctr = 7
        for c in st[::-1]:
            rep[r][ctr] = c
            ctr -= 1
            if ctr < 0:
                r -= 1
                ctr = 7
        for row in rep:
            print(row)
            
    def getTurn(self):
        '''
        Returns True if white turn, False if black turn.
        '''
        return self.whiteTurn
    
    def changeTurn(self):
        '''
        Changes current color's turn.
        '''
        self.whiteTurn = not self.whiteTurn

    def writeMoveList(self, file, moves):
        '''
        Writes moves to output file, each line has one move with 4 chars.
        '''
        m = 'case_6_'
        out = open('moveGen/' + 'check' + file, 'w')
        for i in range(len(moves)):
            if i % 4 == 0 and i != 0:
                out.write('\n' + moves[i])#, end = '')
            else:
                out.write(moves[i])#, end = '')
        out.close()
        
    def getMyPieces(self):
        '''
        Returns BB of all pieces of color whose move it is.
        '''
        if self.whiteTurn:
            return self.getWhitePieces()
        return self.getBlackPieces()

    def getWhitePieces(self):
        '''
        Returns BB of all white pieces.
        '''
        return (self.bb[self.id['P']] | self.bb[self.id['N']]
                | self.bb[self.id['B']] | self.bb[self.id['Q']]
                | self.bb[self.id['R']] | self.bb[self.id['K']])

    def getBlackPieces(self):
        '''
        Returns BB of all black pieces.
        '''
        return (self.bb[self.id['p']] | self.bb[self.id['n']]
                | self.bb[self.id['b']] | self.bb[self.id['q']]
                | self.bb[self.id['r']] | self.bb[self.id['k']])
    
    def getOccupied(self):
        '''
        Returns BB of all occupied squares.
        '''
        return (self.getWhitePieces() | self.getBlackPieces())
                #| self.bb[self.id['K']] | self.bb[self.id['k']])
    

    
    