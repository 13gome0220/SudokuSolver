#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
#Gilbert Gomez
#6025927


import time

ROW = "ABCDEFGHI"
COL = "123456789"
totalConflicts = 0 # Total amount of conflicts or illegal values around a open space.
isNextValuevalid = True #Forward checking global variable to be accessed recursively, if the next value is not valid, then we should skip it and try the next one.
def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def isvalid(board, key, value):
    global totalConflicts
    global isNextValuevalid
    isNextValuevalid = True # resetting for next iteration
    conflictCount = 0
    for letter in ROW:
        if value != 9: #Making sure not to reach number 10 accidentally.
                if board[str(letter + key[1])] == value+1:
                    isNextValuevalid = False
                    #print(isNextValuevalid)
        if board[str(letter + key[1])] == value:
            conflictCount += 1 # Counts the amount of conflicts around a open space.
            return False

    for number in COL:
        if value != 9:
                if board[key[0] + number] == value+1:
                    isNextValuevalid = False
                    # print(isNextValuevalid)
        if board[key[0] + number] == value:
            conflictCount += 1
            return False
    
    #Checking the 3x3 box
    box_row = ROW.find(key[0]) // 3
    box_col = COL.find(key[1]) // 3
    
    for i in range(box_row*3, box_row*3 + 3):
        for j in range(box_col*3, box_col*3 + 3):
            if value != 9:
                if board[ROW[i] + COL[j]] == value+1:
                    isNextValuevalid = False
                    #print(isNextValuevalid)
            
                #print(isNextValuevalid)
            if board[ROW[i] + COL[j]] == value:
                conflictCount += 1
                return False
        
    if (conflictCount == 0):
        return True
    else:
        totalConflicts = conflictCount
        return False


def solve(board):
    openSpace = checkEmpty(board)
    if openSpace == None:
        return True
    currentConflicts = totalConflicts
    for i in range(1,10):
            if isvalid(board, openSpace, i):
                if (currentConflicts >= totalConflicts): #Minimal remaining value hueristic, if the number of conflicts is higher than before, 
                                                         #then we know that the current value is the minimal remaining value; and assign it.
                    board[openSpace] = i
                    if solve(board):
                        return True
           # print (isNextValuevalid)
            if not isNextValuevalid: # Forward checking, if the next value is not valid, then we should skip it and try the next one.
                i+=2
            currentConflicts = totalConflicts
            board[openSpace] = 0
            
    return False
  

# Recursive backtracking algorithm.
def backtracking(board):
    """Takes a board and returns solved board."""
    solve(board)

    solved_board = board

    return solved_board



def checkEmpty(board):
    """Takes a board and returns a set of keys with 0s as values on sudoku board."""

    for cell in board:
        for i in ROW:
            if board[i + cell[1]] == 0:
                return str(i + cell[1])
        for i in COL:
            if board[cell[0] + i] == 0:
                return str(cell[0] + i)
        
    return None
        


if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudoku_boards.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")


    # Solve each board using backtracking
    start_time = time.time()
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        print_board(board)

        # Solve with backtracking
        solved_board = backtracking(board)
        
        # Print solved board. TODO: Comment this out when timing runs.
        print("SOLVED BOARD")
        print_board(solved_board)
        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')
    
    print("Finishing all boards in file.")
    print("Time Elasped: %f" % (time.time() - start_time))