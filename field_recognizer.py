import cv2

from geometrical import *
import numpy as np
import pytesseract

def construct_board(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    #DEBUG
    #cv2.imshow('gray', gray)
    #cv2.waitKey(0)


    # 2. Split the Sudoku grid into 81 cells
    board_size = 450
    cell_size = board_size // 9 # Each cell size (since it's 9x9)

    # Define a margin to remove the cell borders
    margin = 5
    cells = []
    for i in range(9):
        for j in range(9):
            
            # Crop each cell from the thresholded image, leaving a margin around the borders
            start_row = i * cell_size + margin
            end_row = (i + 1) * cell_size - margin
            start_col = j * cell_size + margin
            end_col = (j + 1) * cell_size - margin

            # Ensure the margins don't go out of bounds
            start_row = max(0, start_row)
            start_col = max(0, start_col)
            end_row = min(gray.shape[0], end_row)
            end_col = min(gray.shape[1], end_col)

            # Crop the cell
            cell = binary[start_row:end_row, start_col:end_col]

            cells.append(cell)
            cv2.imwrite(f'cells/cell_{i}_{j}.png', cell)

    
    board = np.zeros((9, 9))
    valid = ['1\n', '2\n', '3\n', '4\n', '5\n', '6\n', '7\n', '8\n', '9\n']

    for i in range(9):
        for j in range(9):
            number = pytesseract.image_to_string(cells[i*9+j], config='--psm 10 digits')
            #print(f"{number} {type(number)}")
            if number is not None and number in valid:
                board[i][j] = number[0]
            else:
                board[i][j] = 0
    
    return board


if __name__ == '__main__':

    # read the image
    image = cv2.imread('puzzles/puzzle_1_persp.jpeg')

    # de-warp the image
    image = un_warp_sudoku(image)

    # construct the board
    board = construct_board(image)
    print(board)