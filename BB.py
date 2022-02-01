#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 18:39:41 2021

@author: sophiecolumbia
"""


class BB():
    def __init__(self, position='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', flip=False):
        '''
        Creates an instance of a set of bitbords.

        Parameters
        ----------
        position : TYPE, optional
            DESCRIPTION. The default is 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'.
        flip : TYPE, optional
            DESCRIPTION. The default is False. When False, white is on bottom
            and is the player's color.
            When True, the board is flipped and the bottom is black and the
            player's color.

        Returns
        -------
        None.

        '''
        self.fileA = 9259542123273814144
        self.fileH = 72340172838076673
        self.fileAB = 13889313184910721216
        self.fileGH = 217020518514230019
        self.rank1 = 255
        self.rank4 = 4278190080
        self.rank5 = 1095216660480
        self.rank8 = 18374686479671623680
        
        #rank 1 - 8
        self.rankMasks = [0xff, 0xff00, 0xff0000,
                          0xff000000, 0xff00000000, 0xff0000000000,
                          0xff000000000000, 0xff00000000000000]
       #file A - B
        self.fileMasks = [0x8080808080808080, 0x4040404040404040, 0x2020202020202020,
                          0x1010101010101010, 0x0808080808080808, 0x0404040404040404,
                          0x0202020202020202, 0x0101010101010101]
        #top left to bottom right
        # self.diagonalMasks = [0x8000000000000000, 0x4080000000000000, 0x2040800000000000,
        #                       0x1020408000000000, 0x0810204080000000, 0x0408102040800000, 
        #                       0x0204081020408000, 0x0102040810204080, 0x0001020408102040,
        #                       0x0000010204081020, 0x8000000102040810, 0x0000000001020408,
        #                       0x0000000000010204, 0x0000000000000102, 0x0000000000000001]
        
        # #top right to bottom left
        # self.antiDiagonalMasks = [0x0100000000000000, 0x0201000000000000, 0x0402010000000000,
        #                           0x0804020100000000, 0x1008040201000000, 0x2010080402010000,
        #                           0x4020100804020100, 0x8040201008040201, 0x0080402010080402,
        #                           0x0000804020100804, 0x0000008040201008, 0x0000000080402010,
        #                           0x0000000000804020, 0x0000000000008040, 0x0000000000000080]
        self.diagonalMasks = [0x1, 0x102, 0x10204, 0x1020408, 0x102040810, 0x10204081020, 0x1020408102040,
	0x102040810204080, 0x204081020408000, 0x408102040800000, 0x810204080000000,
	0x1020408000000000, 0x2040800000000000, 0x4080000000000000, 0x8000000000000000]
        
        self.antiDiagonalMasks = [0x80, 0x8040, 0x804020, 0x80402010, 0x8040201008, 0x804020100804, 0x80402010080402,
	0x8040201008040201, 0x4020100804020100, 0x2010080402010000, 0x1008040201000000,
	0x804020100000000, 0x402010000000000, 0x201000000000000, 0x100000000000000]
        
        self.flip = flip
        
        self.id = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5,
                       'P': 6, 'N': 7, 'B': 8, 'R': 9, 'Q': 10, 'K': 11}
        self.bb = self.readPosition(position)
        

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
        #print('in helper function diagonalMoves')
        # binRep = 1 << s
        # occupied = self.getOccupied()
        # diagPoss = (((occupied & self.diagonalMasks[(s // 8) + (s % 8)]) - (2 * binRep)) 
        #             ^ self.reverseBits(self.reverseBits(occupied & self.diagonalMasks[(s // 8) + (s % 8)]) - (2 * self.reverseBits(binRep))))
        # antiPoss = (((occupied & self.antiDiagonalMasks[(s // 8) + 7 - (s % 8)]) - (2 * binRep)) 
        #     ^ self.reverseBits(self.reverseBits(occupied & self.antiDiagonalMasks[(s // 8) + 7 - (s % 8)]) - (2 * self.reverseBits(binRep))))
        # return (diagPoss & self.diagonalMasks[(s // 8) + (s % 8)]) | (antiPoss & self.antiDiagonalMasks[(s // 8) + 7 - (s % 8)])
        print('s:',s)
        binRep = 1 << s
        print('bin:',binRep)
        occupied = self.getOccupied()
        diagPoss = (((occupied & self.diagonalMasks[(7 - s // 8) + (7 - s % 8)]) - (2 * binRep)) 
                    ^ self.reverseBits(self.reverseBits(occupied & self.diagonalMasks[(7 - s // 8) + (7 - s % 8)]) - (2 * self.reverseBits(binRep))))
        antiPoss = (((occupied & self.antiDiagonalMasks[(7 - s // 8) + 7 - (7 - s % 8)]) - (2 * binRep)) 
            ^ self.reverseBits(self.reverseBits(occupied & self.antiDiagonalMasks[(7 - s // 8) + 7 - (7 - s % 8)]) - (2 * self.reverseBits(binRep))))
        print('Index:', (7 - s // 8) + (7 - s % 8))
        #self.drawBin(diagPoss & self.diagonalMasks[(7 - s // 8) + (7 - s % 8)]) | (antiPoss & self.antiDiagonalMasks[(7 - s // 8) + 7 - (7 - s % 8)])
        return (diagPoss & self.diagonalMasks[(7 - s // 8) + (7 - s % 8)]) | (antiPoss & self.antiDiagonalMasks[(7 - s // 8) + 7 - (7 - s % 8)])
        
    def rowMoves(self, s):
        # binRep = 1 << s
        # occupied = self.getOccupied()
        # horizPoss = (occupied - 2 * binRep) ^ self.reverseBits(self.reverseBits(occupied) - 2 * self.reverseBits(binRep))
        # vertPoss = ((occupied & self.fileMasks[s % 8]) - (2 * binRep)) ^ self.reverseBits(self.reverseBits(occupied & self.fileMasks[s % 8]) - (2 * self.reverseBits(binRep)))
        # print('Index:', (7 - s // 8) + (7 - s % 8))
        # return (horizPoss & self.rankMasks[s / 8]) | (vertPoss & self.fileMasks[s % 8])
        print('s:', s)
        binRep = 1 << s
        print('bin:',binRep)
        occupied = self.getOccupied()
        print()
        horizPoss = (occupied - 2 * binRep) ^ self.reverseBits(self.reverseBits(occupied) - 2 * self.reverseBits(binRep))
        vertPoss = ((occupied & self.fileMasks[7 - s % 8]) - (2 * binRep)) ^ self.reverseBits(self.reverseBits(occupied & self.fileMasks[7 - s % 8]) - (2 * self.reverseBits(binRep)))
        self.drawBin((horizPoss & self.rankMasks[s // 8]) | (vertPoss & self.fileMasks[7 - s % 8]))
        return (horizPoss & self.rankMasks[s // 8]) | (vertPoss & self.fileMasks[7 - s % 8])
    
    def wpMoves(self, history=None, turn=''): #turn = 'w' or 'b'
        '''
        Generates white pawn moves.

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
        blackPieces = self.getBlackPieces()
        occ = self.getOccupied()
        empty = ~occ
        #capture right diagonal
        x = (self.bb[self.id['P']] << 7) & blackPieces & occ & ~self.rank8 & ~self.fileA
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y) #find index of least 1
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 - 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #capture left diagonal
        x = (self.bb[self.id['P']] << 9) & blackPieces & occ & ~self.rank8 & ~self.fileH
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8 + 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move one forward
        x = (self.bb[self.id['P']] << 8) & empty & ~self.rank8
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 1) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move two forward (pawn still in initial position)
        x = (self.bb[self.id['P']] << 16) & empty & (empty << 8) & self.rank4
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 + 2) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        self.writeMoveList('whitePawn.txt', moveList)
        return moveList
    
    def bpMoves(self, history=None, turn=''):
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
        #capture right diagonal
        x = (self.bb[self.id['p']] >> 7) & whitePieces & occ & ~self.rank1 & ~self.fileH
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y) #find index of least 1
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8 + 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #capture left diagonal
        x = (self.bb[self.id['p']] >> 9) & whitePieces & occ & ~self.rank1 & ~self.fileA
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8 - 1) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move one forward
        x = (self.bb[self.id['p']] >> 8) & empty & ~self.rank1
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 1) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        
        #move two forward (pawn still in initial position)
        x = (self.bb[self.id['p']] >> 16) & empty & (empty >> 8) & self.rank5
        y = x & ~(x - 1) #grab first 1
        while y != 0:
            index = self.trailingZeros(y)
            moveList += str(7 - index // 8 - 2) + str(7 - index % 8) + str(7 - index // 8) + str(7 - index % 8)
            x &= ~y #remove least 1
            y = x & ~(x - 1) #find next least 1
        self.writeMoveList('blackPawn.txt', moveList)
        return moveList
    
    def wbMoves(self):
        '''
        Generates white bishop moves.

        Returns
        -------
        moveList : TYPE
            DESCRIPTION.

        '''
        moveList = ''
        whitePieces = self.getWhitePieces()
        B = self.bb[self.id['B']]
        i = B & ~(B - 1)
        while (i != 0):
            iLoc = self.trailingZeros(i)
            poss = self.diagonalMoves(iLoc) & ~whitePieces
            self.drawBin(poss)
            j = poss & ~(poss - 1)
            while (j != 0):
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            B = B & ~i
            i = B & ~(B - 1)
        return moveList
        
    def wrMoves(self):
        '''
        Generates white rook moves.

        Returns
        -------
        None.

        '''
        moveList = ''
        whitePieces = self.getWhitePieces()
        R = self.bb[self.id['R']]
        i = R & ~(R - 1)
        while (i != 0):
            iLoc = self.trailingZeros(i)
            poss = self.rowMoves(iLoc) & ~whitePieces
            j = poss & ~(poss - 1)
            print()
            self.drawBin(poss)
            while (j != 0):
                index = self.trailingZeros(j)
                moveList += str(7 - iLoc // 8) + str(7 - iLoc % 8) + str(7 - index // 8) + str(7 - index % 8)
                poss = poss & ~j
                j = poss & ~(poss - 1)
            R = R & ~i
            i = R & ~(R - 1)
        return moveList
        
    
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
        bb : TYPE
            DESCRIPTION.

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
        # for b in bb:
        #     print(b)
        return bb


        
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
        return int('{:08b}'.format(n)[::-1], 2)

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

    #TODO: check 7- for col
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
            if (self.bb[self.id[piece]] >> i) & 1 == 1:
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
            binary = bin(self.bb[self.id[p]])[2::]
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

    def writeMoveList(self, file, moves):
        out = open('moveGen/' + file, 'w')
        for i in range(len(moves)):
            if i % 4 == 0 and i != 0:
                out.write('\n' + moves[i])#, end = '')
            else:
                out.write(moves[i])#, end = '')
        out.close()

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
    
    