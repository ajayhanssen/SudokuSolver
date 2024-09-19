import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

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
        label = ttk.Label(self, text='Camera Page', font=LARGEFONT)
        label.pack(pady=10, padx=10)

        back_button = ttk.Button(self, text='Back', command=lambda: controller.show_frame(MainPage))
        back_button.pack(fill=tk.BOTH, expand=tk.TRUE)

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