#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 21:12:25 2021

@author: sophiecolumbia
"""

from RepConversion import RepConversion
from BB import BB
import filecmp

class Test():
    def __init__(self, t, expected):
        '''
        Accepts string names of input file and answers file respectively.
        '''
        self.conv = RepConversion()
        self.readFile(t)
        n = self.sortExpected(expected)
        #print(filecmp.cmp('output.txt', n, False))
        self.compareFiles(n, 'output.txt')
        
    def readFile(self, file):
        '''
        Accepts input file.
        '''
        f = open(file, 'r')
        out = open('output.txt', 'w')
        cases = int(f.readline())
        pos = [[] for j in range(8)]
        for c in range(cases):
            f.readline()
            for i in range(8):
                line = f.readline().rstrip('\n')
                pos[i] = [char for char in line]
            l = self.runCase(pos)
            for move in l:
                out.write(str(move) + '\n')
            out.write('\n')
        f.close()
    
    def runCase(self, posArr):
        bitb = BB(position = self.conv.arrayToFEN(posArr))
        moves = bitb.makeMove()
        #print('printing moves: ' + moves + ' done.')
        l = []
        for move in range(len(moves) // 4):
            l.append((moves[move * 4: 4 * move + 4]))
        return sorted(l)
    
    def sortExpected(self, exp):
        name = 'sorted_answer.txt'
        rIn = open(exp, 'r')
        wOut = open(name, 'w')
        l = []
        for line in rIn:
            if line == '\n':
                l.sort()
                for element in l:
                    wOut.write(element + '\n')
                wOut.write('\n')
                l = []
            else:
                l.append(line.rstrip('\n'))
        return name
    
    def compareFiles(self, ans, myout):
        b = filecmp.cmp(ans, myout, False)
        if b:
            print('Success.')
            return
        aList = []
        oList = []
        aF = open(ans, 'r')
        curr = []
        for line in aF:
            if line == '\n':
                aList.append(curr)
                curr = []
            else:
                curr.append(line.rstrip('\n'))
        oF = open(myout, 'r')
        curr = []
        for line in oF:
            if line == '\n':
                oList.append(curr)
                curr = []
            else:
                curr.append(line.rstrip('\n'))
        aF.close()
        oF.close()
        # for line in aList:
        #     print(line)
        # print()
        # for line in oList:
        #     print(line)
        self.compareLists(aList, oList)
            
    def compareLists(self, aList, oList):
        '''
        aList is what the list move moves should be, oList is what move generation found.
        Uses set differences to find missing or superfluous moves generated.
        '''
        if len(aList) == len(oList):
            print('Overall number of cases are equal.')
            wrongCases = []
            for i in range(len(aList)):
                if aList[i] != oList[i]:
                    print('Case', i, 'failed.')
                    if len(aList[i]) != len(aList[i]):
                        print('Moves in case', i, ': answer = ',
                              len(aList[i]), 'output = ', len(oList[i]))
                    a_o = list(set(aList[i]) - set(oList[i]))
                    o_a = list(set(oList[i]) - set(aList[i]))
                    if len(a_o) != 0:
                        print('Missing moves in output:', a_o)
                    if len(o_a) != 0:
                        print('Wrong moves in output:', o_a)
                else: print('Case', i, 'passed.')
        else:
            print('Overall number of cases don\'t match')
        