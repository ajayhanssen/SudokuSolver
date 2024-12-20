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
    cv2.imwrite('presentation/1_original.jpg', image)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # what if box blurring is used instead of gaussian?
    boxblurred = cv2.boxFilter(gray, -1, (5, 5))
    cv2.imwrite('presentation/2_boxblurred.jpg', boxblurred)

    # what if bilateral blurring is used instead of gaussian?
    bilateralblurred = cv2.bilateralFilter(gray, 5, 75, 75)
    cv2.imwrite('presentation/3_bilateralblurred.jpg', bilateralblurred)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.imwrite('presentation/2_blurred.jpg', blurred)

    # Apply Canny Edge Detection
    edges = cv2.Canny(blurred, 50, 150)
    cv2.imwrite('presentation/3_canny.jpg', edges)

    # presentation only, save image with all the contours
    #contis, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #imgwithcontours = cv2.drawContours(image, contis, -1, (0, 255, 0), 2)
    #cv2.imwrite('presentation/4_contours.jpg', imgwithcontours)

    # Find contours on the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area, descending from biggest to smallest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sudoku_contour = None

    # Iterate through all the contours, looking for one with four points
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:  # Looking for a contour with four points
            sudoku_contour = approx
            break

    # If no contour was found, return None
    if sudoku_contour is None:
        print("No valid Sudoku contour found!")
        return None

    # Order the Sudoku points
    sudoku_contour = sudoku_contour.reshape(4, 2)
    rect = order_points(sudoku_contour)

    max_width = 450
    max_height = 450

    # Destination points for the unwarped image
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # Compute the perspective transform matrix and apply it
    matrix = cv2.getPerspectiveTransform(rect, dst)
    #print(matrix)
    unwarped = cv2.warpPerspective(image, matrix, (max_width, max_height))


    # Save images for documentation purposes

    # blurredrescaled = cv2.resize(blurred, (450, 450), interpolation=cv2.INTER_AREA)
    # cannyrescaled = cv2.resize(edges, (450, 450), interpolation=cv2.INTER_AREA)
    imgwithcontours = cv2.drawContours(image, [sudoku_contour], -1, (0, 255, 0), 4)
    imgwithcontours = cv2.resize(imgwithcontours, (450, 450), interpolation=cv2.INTER_AREA)

    # draw nmbers 1, 2, 3, 4 on the edges of image, clockwise
    # cv2.putText(imgwithcontours, '1', (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '2', (430, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '3', (430, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '4', (5, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # # draw numbers on the corners of the contour clockwise
    # cv2.putText(imgwithcontours, '1', (80, 67), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '2', (403, 63), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '3', (382, 356), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(imgwithcontours, '4', (87, 378), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # cv2.imwrite('progression/1_blurred.jpg', blurredrescaled)
    # cv2.imwrite('progression/2_canny.jpg', cannyrescaled)
    cv2.imwrite('presentation/5_contours.jpg', imgwithcontours)
    # cv2.imwrite('presentation/6_unwarped.jpg', unwarped)
   

    return unwarped

if __name__ == '__main__':
    image = cv2.imread('puzzles/puzzle_1_persp.jpeg')
    image = cv2.imread('puzzles/80512422-w-640.jpg')

    unwarped = un_warp_sudoku(image)
    if unwarped is not None:
        cv2.imshow('Original Sudoku', image)
        cv2.imshow('Unwarped Sudoku', unwarped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Could not unwarp the image.")
