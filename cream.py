import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

from geometrical import *
from field_recognizer import *
from solver import *

LARGEFONT = ('Verdana', 20)

class SudokoSolverApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Sudoku Solver')

        container = ttk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, CamPage, LoadPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainPage(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='SudokuSolver', font=LARGEFONT)
        label.pack(pady=10, padx=10)

        cam_button = ttk.Button(self, text='Camera', command=lambda: controller.show_frame(CamPage))
        cam_button.pack(fill=tk.BOTH, expand=tk.TRUE)

        load_button = ttk.Button(self, text='Load Image', command=lambda: controller.show_frame(LoadPage))
        load_button.pack(fill=tk.BOTH, expand=tk.TRUE)

        credits = ttk.Label(self, text='Made by: Thöni, Unterhuber, Peer', font=('Verdana', 7))
        credits.pack(pady=10, padx=10, side=tk.LEFT)

class CamPage(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.cap = cv2.VideoCapture(0)  # Initialize the camera

        label = ttk.Label(self, text='Camera Page', font=('Helvetica', 18, 'bold'))
        label.pack(pady=10, padx=10)

        # Left frame for video and recognition results
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')  # Anchor to top-left (north-west)

        # Video output at the top left
        self.video_label = ttk.Label(left_frame)
        self.video_label.pack()

        # "Scan" button below the video output
        scan_button = ttk.Button(left_frame, text='Scan', command=self.scan)
        scan_button.pack(pady=5)

        # Output for recognized field below the scan button
        self.placeholder1 = ttk.Label(left_frame, text="Recognized field output here", relief=tk.SUNKEN)
        self.placeholder1.pack(pady=10)

        # "Solve" button below the recognized field output
        solve_button = ttk.Button(left_frame, text='Solve', command=self.solve)
        solve_button.pack(pady=5)

        # Right frame for solved matrix output
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, anchor='ne')  # Anchor to top-right (north-east)

        # Placeholder2 for solved matrix output
        self.placeholder2 = ttk.Label(right_frame, text="Solved matrix will appear here", relief=tk.SUNKEN)
        self.placeholder2.pack(pady=10, padx=10)

        # Bottom frame for back button
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10, anchor='se')  # Anchor to bottom-right (south-east)

        # "Back" button at the bottom-right corner
        back_button = ttk.Button(bottom_frame, text='Back', command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.after(25, self.update_frame)  # Update every 25 ms

    def scan(self):
    # Capture the current frame
        ret, frame = self.cap.read()
        if ret:
        # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        try:
            # Attempt to unwarp the Sudoku image
            self.unwarped = un_warp_sudoku(frame)

            
            # Check if the result is None or a valid image
            if self.unwarped is None:
                print("Unwarp failed. Please check the image or contour detection.")
                return
            

            
            # Convert to PIL Image object
            img = Image.fromarray(self.unwarped)
            
            # Check and print the mode and size of the image
            print(f"Image mode: {img.mode}, size: {img.size}")
            
            # Resize the image for display
            img = img.resize((300, 300))
            
            # Create a PhotoImage object for display
            imgtk = ImageTk.PhotoImage(image=img)

            # Display the image in the placeholders
            #scanned sudoku
            self.placeholder1.imgtk = imgtk
            self.placeholder1.configure(image=imgtk)


            #matrix output
            self.placeholder2.imgtk = imgtk
            self.placeholder2.configure(image=imgtk)

        except Exception as e:
            print(f"Error processing the frame: {e}")
        else:
            print("Failed to capture frame from the camera.")


    def solve(self):
        # Your solve logic here
        field =  construct_board(self.unwarped)
        if solve(field):
            print("Solved!")
            print(field)
        else:
            print("No solution exists") 


    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

class LoadPage(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Load Image Page', font=LARGEFONT)
        label.pack(pady=10, padx=10)

        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(MainPage))
        back_button.pack(fill=tk.BOTH, expand=tk.TRUE)


if __name__ == '__main__':
    app = SudokoSolverApp()
    app.mainloop()