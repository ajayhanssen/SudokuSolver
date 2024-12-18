import cv2
import numpy as np

#####################################################################
### Failed attempt at using hough lines to detect the puzzle grid ###
###     look at geometrical.py for the correct implementation     ###
#####################################################################


# Load an image
original_puzzle = cv2.imread('puzzles/puzzle_1_persp.jpeg')

# Convert the image to grayscale
gs_puzzle = cv2.cvtColor(original_puzzle, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur
blurred_puzzle = cv2.GaussianBlur(gs_puzzle, (5, 5), 0)

# Apply Canny Edge Detection
edges = cv2.Canny(blurred_puzzle, 100, 200)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
print(f'num edges: {len(edges)}')

kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)

# Detect lines in the image using Hough Lines ( if those damn parameters wold work)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=200, minLineLength=200, maxLineGap=20)
# Draw lines on original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(original_puzzle, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Hough Lines', original_puzzle)
cv2.imwrite('presentation/hough_lines.jpg', original_puzzle)
cv2.waitKey(0)


vertical_lines = []
horizontal_lines = []

for line in lines:
    x1, y1, x2, y2 = line[0]
    if abs(x2 - x1) > abs(y2 - y1):
        horizontal_lines.append(line)
    else:
        vertical_lines.append(line)

print(f'num lines: {len(lines)}')