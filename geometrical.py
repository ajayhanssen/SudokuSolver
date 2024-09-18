import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype='float32')

    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def un_warp_sudoku(image):

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny Edge Detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours on the image, second return value is the hierarchy ( which contours are inside which), not useful here
    # cv2.RETR_EXTERNAL retrieves only the outermost contours, cv2.CHAIN_APPROX_SIMPLE removes redundant points and only returns the endpoints of the contour
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area, descending from biggest to smallest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # iterate through all the contours, looking for one with four points (resulting in a rectangle, obviously)
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:  # Looking for a contour with four points
            sudoku_contour = approx
            break

    #cv2.drawContours(image, [sudoku_contour], -1, (0, 255, 0), 3)
    #cv2.imshow('Sudoku Contour', image)
    #cv2.waitKey(0)


    # Order the Sudoku points
    sudoku_contour = sudoku_contour.reshape(4, 2)
    rect = order_points(sudoku_contour)

    # Get the width and height of the new warped image
    width_a = np.linalg.norm(rect[2] - rect[3])
    width_b = np.linalg.norm(rect[1] - rect[0])
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(rect[1] - rect[2])
    height_b = np.linalg.norm(rect[0] - rect[3])
    max_height = max(int(height_a), int(height_b))

    # Destination points for the unwarped image
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # Compute the perspective transform matrix and apply it
    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))

    return warped

if __name__ == '__main__':
    image = cv2.imread('puzzles/puzzle_1.png')
    unwarped = un_warp_sudoku(image)
    cv2.imshow('Unwarped Sudoku', unwarped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()