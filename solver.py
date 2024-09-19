import numpy as np

def is_valid(board, row, col, num):
    
    if num in board[row,:]:
        return False
    
    if num in board[:,col]:
        return False
    
    box_row = row // 3 * 3
    box_col = col // 3 * 3

    if num in board[box_row:box_row+3, box_col:box_col+3]:
        return False
    
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    else:
        row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False

if __name__ == '__main__':
    board = np.array([[3, 0, 0, 0, 8, 0, 0, 0, 6],
                      [0, 1, 0, 0, 0, 6, 0, 2, 0],
                      [0, 0, 4, 7, 0, 0, 5, 0, 0],
                      [0, 4, 0, 0, 1, 0, 9, 0, 0],
                      [6, 0, 0, 2, 0, 4, 0, 0, 1],
                      [0, 0, 3, 0, 6, 0, 0, 5, 0],
                      [0, 0, 8, 0, 0, 3, 6, 0, 0],
                      [0, 2, 0, 4, 0, 0, 0, 1, 0],
                      [5, 0, 0, 0, 2, 0, 0, 0, 7]])

    
    if solve(board):
        print("Solved!")
        print(board)
    else:
        print("No solution exists")