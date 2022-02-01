#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 15:27:21 2021

@author: sophiecolumbia
"""

"""
Created on Wed Jun  9 18:39:41 2021

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
    def __init__(self, position='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', whiteTurn = True, move_history = []):
        '''
        Creates an instance of a set of bitbords.

        Parameters
        ----------
        position : str, optional
            DESCRIPTION. The default is 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'.
        whiteTurn : bool, optional
            DESCRIPTION. The default is True. When True, it's white's turn. When False, is black's turn
            

        Returns
        -------
        None.
        '''
        
        self.whiteTurn = whiteTurn
        
        self.id = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5,
                       'P': 6, 'N': 7, 'B': 8, 'R': 9, 'Q': 10, 'K': 11}
        self.bb = self.readPosition(position)
        self.move_history = move_history
        self.castle_wk = True
        self.castle_wq = True
        self.castle_bk = True
        self.castle_bq = True
        

    def makeMove(self):
        self.occupied = self.getOccupied()
        llegal = ~(self.bb[self.id['P']] | self.bb[self.id['P']] | self.bb[self.id['P']] 
                    | self.bb[self.id['P']] | self.bb[self.id['P']] | self.bb[self.id['P']]
                    | self.bb[self.id['P']] )
        l = self.wpMoves()
        l += '\n' + self.bpMoves()
        print('printing all bitboards')
        for p in self.id:
            print('printing ' + p)
            
            self.drawbb(p)
        # p = 0
        # for c in l:
        #     print(c, end = '')
        #     p += 1
        #     if p == 4:
        #         p = 0
        #         print()
        return l
    
    def possibleWhiteMoves(self):
        return
    
    def possibleBlackMoves(self):
        return
    
    def diagonalMoves(self, s):
        '''
        Helper function for move generation for bishops and queens.

        Parameters
        ----------
        s : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

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
    
    def wpMoves(self, history=None):
        '''
        Generates white pawn moves.

        Parameters
        ----------
        history : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        moveList : str
            String, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).

        '''
        moveList = ''
        P = self.bb[self.id['P']]
        blackPieces = self.getBlackPieces()
        occ = self.getOccupied()
        empty = ~occ
        #capture right diagonal
        x = int((np.left_shift(P, seven)) & blackPieces & occ & ~rank8 & ~fileA)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y) #find index of least 1
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 - 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #capture left diagonal
        x = int((np.left_shift(P, nine)) & blackPieces & occ & ~rank8 & ~fileH)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 + 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move one forward
        x = int((np.left_shift(P, eight)) & empty & ~rank8)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move two forward (pawn still in initial position)
        x = int((np.left_shift(P, sixteen)) & empty & (np.left_shift(empty, eight)) & rank4)
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
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            print('promotion right')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 - 1)
            y2 = str(7 - index % 8)
            moveList += 'PR' + y1 + y2 + 'PB' + y1 + y2 + 'PN' + y1 + y2 + 'PQ' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: capture left
        x = int((np.left_shift(P, nine)) & blackPieces & occ & rank8 & ~fileH)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            print('promotion left')
            index = self.trailingZeros(y) #find index of least 1
            y1 = str(7 - index % 8 + 1)
            y2 = str(7 - index % 8)
            moveList += 'PR' + y1 + y2 + 'PB' + y1 + y2 + 'PN' + y1 + y2 + 'PQ' + y1 + y2
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
            
        #pawn promotion: one forward
        x = int((np.left_shift(P, eight)) & ~occ & rank8)
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            print('promotion forward')
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
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'WE'
    
    
        #en passant to the left
        x = int(np.left_shift(P, one) & self.bb[self.id['p']] & rank5 & ~fileH & EP)
        if x != 0:
            #print('en passant found')
            index = self.trailingZeros(x)
            moveList += str(7 - index % 8 + 1) + str(7 - index % 8) + 'WE'
        self.writeMoveList('whitePawn.txt', moveList)
        
        return moveList
    
    def bpMoves(self, history=None):
        '''
        Generates black pawn moves.

        Parameters
        ----------
        history : TYPE, optional
            DESCRIPTION. The default is None.
        turn : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        moveList : str
            String, where each possible move is 4 characters long (oRank, oFile, dRank, dFile).

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
            print('promotion right')
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
            print('promotion left')
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
            print('promotion forward')
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
        
        self.writeMoveList('blackPawn.txt', moveList)
        return moveList
    
    def bMoves(self):
        '''
        Generates bishop moves.

        Returns
        -------
        moveList : TYPE
            DESCRIPTION.

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
        self.writeMoveList('white_bishop.txt', moveList)
        return moveList
        
    def nMoves(self):
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
        self.writeMoveList('white_knight.txt', moveList)
        return moveList
    
    def rMoves(self):
        '''
        Generates rook moves.

        Returns
        -------
        None.

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
        self.writeMoveList('white_rook.txt', moveList)
        return moveList
    
    def qMoves(self):
        '''
        

        Returns
        -------
        None.

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
        self.writeMoveList('white_queen.txt', moveList)
        return moveList
        
    def kMoves(self):
        moveList = ''
        movePieces = self.getMyPieces()
        if self.whiteTurn:
            K = int(self.bb[self.id['K']])
        else:
            K = int(self.bb[self.id['k']])
        iLoc = self.trailingZeros(K)
        #print(iLoc)
        if iLoc > 9:
            poss = np.left_shift(kingMask, np.subtract(np.uint64(iLoc), nine))
        else:
            poss = np.right_shift(kingMask, np.subtract(nine, np.uint64(iLoc)))
            #print(np.subtract(np.uint64(iLoc), nine))
            #print('in first else', poss)
        if iLoc % 8 < 4:
            poss = poss & ~fileAB & ~movePieces
        else:
            poss = poss & ~fileGH & ~movePieces
        poss = int(poss)
        j = poss & ~(poss - 1)
        while j != 0:
            index = self.trailingZeros(j)
            moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
            poss = poss & ~j
            #self.drawBin(poss)
            #print()
            j = poss & ~(poss - 1)
        self.writeMoveList('white_king.txt', moveList)
        return moveList
    
    
    def en_passant(self):
        '''
        Checks to see if an en passant is possible

        Returns
        -------
        None.

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

        Returns
        -------
        move_list : TYPE
            DESCRIPTION.

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
        self.writeMoveList('castling_white.txt', move_list)
        return move_list
    
    def poss_castle_black(self):
        pass
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
        self.writeMoveList('castling_black.txt', move_list)
        return move_list
    
    def readPosition(self, pos):
        '''
        Generates bitboards based on FEN. Most significant bit is the top left corner of the board (A8)
        and 2nd most sigbit is B8. LSB is H1.

        Parameters
        ----------
        pos : str
            Board represented in FEN.

        Returns
        -------
        bb : uint64 list
            Contains 12 integers that each represent a certain piece type.

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
        return b

    def unsafeForBlack(self):
        occ = self.getOccupied()
        
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
        return unsafe
    
    def unsafeForWhite(self):
        occ = self.getOccupied()
        
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
        return unsafe
        
    def reverseBits(self, n):
        '''
        Reverses the order of bits in a number.
        Parameters
        ----------
        n : int
            number whose bits are to be reversed

        Returns
        -------
        int
            Integer resulting from reversal operation.

        '''
        #print('Passed in reverseBits:',n)
        #print('{:064b}'.format(n)[::-1], 2)
        return int('{:064b}'.format(n)[::-1], 2)
        
    def unsignedReverse(self, n):
        #print('type of n passed in unsignedReverse:', type(n))
        return np.uint64(int('{:064b}'.format(n)[::-1], 2))

    def trailingZeros(self, num):
        '''
        Counts the number of trailing zeros in a binary representation of a number.
        Parameters
        ----------
        num : int
            Number to have trailing zeros calculuated.

        Returns
        -------
        int
            Count of trailing zeros.

        '''
        s = bin(num)[2::]
        return len(s) - len(s.rstrip('0'))

    def drawbb(self, piece):
        '''
        Draws bitboard of specified piece in a 2D array.

        Parameters
        ----------
        piece : char
            Specified piece to be drawn (as denoted in FEN).

        Returns
        -------
        None.

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
        # print(n)
        # print(bin(n))
        # print(len(bin(n)) - 2)
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
        return self.whiteTurn
    
    def changeTurn(self):
        self.whiteTurn = not self.whiteTurn

    def writeMoveList(self, file, moves):
        out = open('moveGen/' + 'case_0_' + file, 'w')
        for i in range(len(moves)):
            if i % 4 == 0 and i != 0:
                out.write('\n' + moves[i])#, end = '')
            else:
                out.write(moves[i])#, end = '')
        out.close()
        
    def getMyPieces(self):
        if self.whiteTurn:
            return self.getWhitePieces()
        return self.getBlackPieces()

    def getWhitePieces(self):
        return (self.bb[self.id['P']] | self.bb[self.id['N']]
                | self.bb[self.id['B']] | self.bb[self.id['Q']]
                | self.bb[self.id['R']] | self.bb[self.id['K']])

    def getBlackPieces(self):
        return (self.bb[self.id['p']] | self.bb[self.id['n']]
                | self.bb[self.id['b']] | self.bb[self.id['q']]
                | self.bb[self.id['r']] | self.bb[self.id['k']])
    
    def getOccupied(self):
        return (self.getWhitePieces() | self.getBlackPieces()
                | self.bb[self.id['K']] | self.bb[self.id['k']])
    

    
    