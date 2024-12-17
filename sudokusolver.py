import numpy as np
import cv2
from geometrical import *
from field_recognizer import *
from solver import *

image = cv2.imread('puzzles/puzzle_1_persp.jpeg')
image = cv2.imread('puzzles/80512422-w-640.jpg')

cv2.imshow('Original Image', image)
cv2.waitKey(0)

image = un_warp_sudoku(image)
board = construct_board(image)

if solve(board):
    print("Solved!")
    print(board)
else:
    print("No solution exists")