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
        self.compareLists(aList, oList)

    def newCompare(self, expertList, genList):
        answerSet = set()
        genSet = set()
        for move in expertList:
            answerSet.add(move)
        for move in genList:
            genSet.add(move)
            if move not in answerSet:
                print('Move ' + move + 'was generated but is not in answer set')
        extraExpert = answerSet - genSet
        extraGen = genSet - answerSet
        print('Moves given by expert but not generated:')
        print(extraExpert)
        print('Moves given by engine but not expert:')
        print(extraGen)
            
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

def convertAlgebraic(algFile):
        f = open(algFile, 'r')
        out = open(algFile+'CONVERTED', 'w')
        fileLines = f.readlines()
        for line in fileLines:
            line = line.lower()
            sq1 = line[0:2]
            sq2 = line[2:4]
            w1 = match(sq1)
            w2 = match(sq2)
            move = w1 + w2 + '\n'
            out.write(move)
        f.close()
        out.close()     

def match(p):
    if (p == 'a1'):
        c = '70'
    elif (p == 'a2'):
        c = '60'
    elif (p == 'a3'):
        c = '50'
    elif (p == 'a4'):
        c = '40'
    elif (p == 'a5'):
        c = '30'
    elif (p == 'a6'):
        c = '20'
    elif (p == 'a7'):
        c = '10'
    elif (p == 'a8'):
        c = '00'
    elif (p == 'b1'):
        c = '71'
    elif (p == 'b2'):
        c = '61'
    elif (p == 'b3'):
        c = '51'
    elif (p == 'b4'):
        c = '41'
    elif (p == 'b5'):
        c = '31'
    elif (p == 'b6'):
        c = '21'
    elif (p == 'b7'):
        c = '11'
    elif (p == 'b8'): #DONE
        c = '01'
    elif (p == 'c1'):
        c = '72'
    elif (p == 'c2'):
        c = '62'
    elif (p == 'c3'):
        c = '52'
    elif (p == 'c4'):
        c = '42'
    elif (p == 'c5'):
        c = '32'
    elif (p == 'c6'):
        c = '22'
    elif (p == 'c7'):
        c = '12'
    elif (p == 'c8'):
        c = '02'
    elif (p == 'd1'):
        c = '73'
    elif (p == 'd2'):
        c = '63'
    elif (p == 'd3'):
        c = '53'
    elif (p == 'd4'):
        c = '43'
    elif (p == 'd5'):
        c = '33'
    elif (p == 'd6'):
        c = '23'
    elif (p == 'd7'):
        c = '13'
    elif (p == 'd8'):
        c = '03'
    elif (p == 'e1'):
        c = '74'
    elif (p == 'e2'):
        c = '64'
    elif (p == 'e3'):
        c = '54'
    elif (p == 'e4'):
        c = '44'
    elif (p == 'e5'):
        c = '34'
    elif (p == 'e6'):
        c = '24'
    elif (p == 'e7'):
        c = '14'
    elif (p == 'e8'):
        c = '04'
    elif (p == 'f1'): 
        c = '75'
    elif (p == 'f2'):
        c = '65'
    elif (p == 'f3'):
        c = '55'
    elif (p == 'f4'):
        c = '45'
    elif (p == 'f5'):
        c = '35'
    elif (p == 'f6'):
        c = '25'
    elif (p == 'f7'):
        c = '15'
    elif (p == 'f8'):
        c = '05'
    elif (p == 'g1'):
        c = '76'
    elif (p == 'g2'):
        c = '66'
    elif (p == 'g3'):
        c = '56'
    elif (p == 'g4'):
        c = '46'
    elif (p == 'g5'):
        c = '36'
    elif (p == 'g6'):
        c = '26'
    elif (p == 'g7'):
        c = '16'
    elif (p == 'g8'):
        c = '06'
    elif (p == 'h1'):
        c = '77'
    elif (p == 'h2'):
        c = '67'
    elif (p == 'h3'):
        c = '57'
    elif (p == 'h4'):
        c = '47'
    elif (p == 'h5'):
        c = '37'
    elif (p == 'h6'):
        c = '27'
    elif (p == 'h7'):
        c = '17'
    elif (p == 'h8'):
        c = '07'
    else:
        c = p
    return c

def main():
    name = input('Enter input file: ')
    convertAlgebraic(name)
    

if __name__ == '__main__':
    main()