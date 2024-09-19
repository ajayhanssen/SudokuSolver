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
        self.cap = cv2.VideoCapture(0)  # initialize the camera

        label = ttk.Label(self, text='Camera Page', font=LARGEFONT)
        label.pack(pady=10, padx=10)


        # left frame for camera view
        left_frame = ttk.Frame(self)
        left_frame.pack(pady=10, padx=10, side=tk.LEFT)

        self.video_label = ttk.Label(left_frame)
        self.video_label.pack()

        self.placeholder1 = ttk.Label(left_frame)
        self.placeholder1.pack(pady=10, padx=10, expand=tk.TRUE)


        # right frame for scan button
        right_frame = ttk.Frame(self)
        right_frame.pack(pady=10, padx=10, side=tk.RIGHT)

        scan_button = ttk.Button(right_frame, text='Scan', command=self.scan)
        scan_button.pack(pady=10, padx=10)

        self.placeholder2 = ttk.Label(right_frame)
        self.placeholder2.pack(pady=10, padx=10, expand=tk.TRUE)


        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10, padx=10, side=tk.BOTTOM, expand=tk.TRUE)

        back_button = ttk.Button(bottom_frame, text='Back', command=lambda: controller.show_frame(MainPage))
        back_button.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.update_frame()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original_img = cv2.imread('puzzles/puzzle_1_persp.jpeg') #-----------------------------testing only

            frame = cv2.resize(frame, (320, 240))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.after(25, self.update_frame)  # Update every 10 ms
    
    def scan(self):
        
        img = Image.fromarray(un_warp_sudoku(self.original_img))
        self.unwarped_img = img
        img = img.resize((320, 320))
        imgtk = ImageTk.PhotoImage(image=img)

        self.placeholder1.imgtk = imgtk
        self.placeholder1.configure(image=imgtk)

        self.placeholder2.imgtk = imgtk
        self.placeholder2.configure(image=imgtk)

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