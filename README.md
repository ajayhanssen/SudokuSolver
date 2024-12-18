# SudokuSolver

SudokuSolver is an advanced Python-based application for recognizing and solving Sudoku puzzles. It combines computer vision techniques, optical character recognition (OCR), and algorithmic problem-solving to deliver an end-to-end solution for Sudoku puzzles.

## Quick file overview
Run each of these fiels to run example usage.
- **app.py**:
  - Main file, combining all the scripts below. Contains the GUI.
- **geometrical.py**:
  - Detects sudoku puzzle and de-warps it.
- **field_recognizer.py**:
  - Splits grid into cells and uses OCR to detect the numbers.
- **solver.py**:
  - Contains solving algorithm to solve any (solvable) sudoku puzzle

## Features

- **Computer Vision for Puzzle Recognition**:
  - Detects and extracts Sudoku grids from images.
  - Applies perspective transformations to unwarp the grid.
- **Optical Character Recognition (OCR)**:
  - Recognizes digits within the Sudoku grid using Tesseract OCR.
- **Solving Algorithm**:
  - Implements a backtracking algorithm to solve the recognized Sudoku puzzle.
- **Graphical User Interface (GUI)**:
  - Built with `Tkinter` and `ttkbootstrap`, offering an intuitive interface for camera and image-based puzzle solving.
- **Visualization Tools**:
  - Displays detected edges, unwarped grids, and solved puzzles.

---

## Requirements

The following dependencies are required to run the project:

- Python 3.7 or higher
- Libraries:
  - `numpy`
  - `opencv-python`
  - `pytesseract`
  - `ttkbootstrap`
  - `Pillow`

Install them via pip:
```bash
pip install requirements.txt
