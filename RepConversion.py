#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 20:53:49 2021

@author: sophiecolumbia
"""

class RepConversion():
    
    @staticmethod
    def fileToArray(self, file):
        f = open(file, 'r')
        st = ''
        for line in f:
            st += line.rstrip('\n')
        f.close()
        return self.strToArray(st)
    
    @staticmethod
    def arrayToFEN(arr):
        ctr = 0
        fen = ''
        for line in arr:
            for piece in line:
                if piece == ' ':
                    ctr += 1
                else:
                    if ctr != 0:
                        fen += str(ctr)
                        ctr = 0
                    fen += piece
            if ctr!= 0:
                fen += str(ctr)
                ctr = 0
            fen += '/'
        fen = fen.rstrip('/') 
        return fen
    
    @staticmethod
    def FENtoArray(fen):
        r = 0
        c = 0
        array = [[' ' for i in range(8)] for j in range(8)]
        for f in fen:
            if f == ' ':
                break
            if f == '/':
                r += 1
                c = 0
            elif f.isdigit():
                c += int(f)
            else:
                array[r][c] = f
                c += 1
        return array
            
    @staticmethod
    def strToArray(pos='rnbqkbnrpppppppp                                PPPPPPPPRNBQKBNR'):
        array = [[' ' for i in range(8)] for j in range(8)]
        for i in range(len(pos)):
            array[i // 8][i % 8] = pos[i]
        return array