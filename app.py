import tkinter as tk
from tkinter import ttk, filedialog  # Import filedialog for open file dialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2

from geometrical import *
from field_recognizer import *
from solver import *

LARGEFONT = ('Verdana', 20)
TEXTFONT = ImageFont.truetype("arial.ttf", 20)  # Define a font object for PIL drawing (replace with a valid font path)
original_field = None

class SudokuSolverApp(tb.Window):  # Inherit from ttkbootstrap.Window for theme support

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Sudoku Solver')
        self.geometry('1000x1000')  # Set a fixed window size
        self.resizable(False, False)  # Disable window resizing
        self.themename = kwargs.pop("themename", "solar")  # Set default theme to 'solar' if not provided
        self.style.theme_use(self.themename)  # Apply the selected theme

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
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout for the main frame
        self.grid_columnconfigure(0, weight=1)  # Center alignment for elements
        self.grid_columnconfigure(1, weight=1)  # Equal space for left and right buttons
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Center alignment for elements
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Main title
        label = ttk.Label(self, text='SudokuSolver', font=LARGEFONT)
        label.grid(row=0, column=1, pady=(50, 20), padx=10)  # Positioned at the top center

        # Camera button on the left
        cam_button = ttk.Button(self, text='Camera', command=lambda: controller.show_frame(CamPage))
        cam_button.grid(row=1, column=0, sticky='e', padx=(20, 10), ipadx=20, ipady=10)  # Positioned on the left

        # Load Image button on the right
        load_button = ttk.Button(self, text='Load Image', command=lambda: controller.show_frame(LoadPage))
        load_button.grid(row=1, column=2, sticky='w', padx=(10, 20), ipadx=20, ipady=10)  # Positioned on the right

        # Exit button in the bottom center
        exit_button = ttk.Button(self, text='Exit', command=self.controller.quit)
        exit_button.grid(row=2, column=1, pady=(10, 20), ipadx=20, ipady=10)  # Positioned at the bottom center

        # Credits label at the very bottom center
        credits = ttk.Label(self, text='Made by: Thöni, Unterhuber, Peer', font=('Verdana', 7))
        credits.grid(row=3, column=1, pady=(10, 30), sticky='s')  # Positioned at the bottom center


class CamPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cap = cv2.VideoCapture(0)  # Initialize the camera

        # Main title
        label = ttk.Label(self, text='Camera Page', font=('Helvetica', 18, 'bold'))
        label.pack(pady=20, padx=20)  # Increased padding for the title

        # Left frame for video and recognition results
        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, padx=30, pady=30, anchor='nw')  # Increased padding around left frame
        left_frame.grid_columnconfigure(0, weight=1)  # Center alignment for elements in left frame

        try:
            placeholder_image = Image.open("placeholder.jpg")  # Load the placeholder image
            placeholder_image = placeholder_image.resize((350, 350))  # Resize placeholder image to match
            empty_photo = ImageTk.PhotoImage(placeholder_image)  # Convert to ImageTk
        except Exception as e:
            print(f"Error loading placeholder image: {e}")
            # If loading fails, create a blank image instead
            empty_image = Image.new('RGB', (350, 350), (240, 240, 240))  # Blank image (gray background)
            empty_photo = ImageTk.PhotoImage(empty_image)

        self.empty_photo = empty_photo  # Store placeholder image for reuse

        # Video output at the top left
        self.video_label = ttk.Label(left_frame, relief=tk.SUNKEN, image=empty_photo)  # Use placeholder image
        self.video_label.image = empty_photo  # Keep reference to avoid garbage collection
        self.video_label.grid(row=0, column=0, padx=10, pady=10)

        # "Scan" button below the video output
        scan_button = ttk.Button(left_frame, text='Scan', command=self.scan)
        scan_button.grid(row=1, column=0, pady=5)

        # Output for recognized field below the scan button
        self.placeholder1 = ttk.Label(left_frame, text="Recognized field output here", relief=tk.SUNKEN,
                                      image=empty_photo)  # Use placeholder image as initial placeholder
        self.placeholder1.image = empty_photo  # Keep reference to avoid garbage collection
        self.placeholder1.grid(row=2, column=0, pady=10)

        # "Solve recognized puzzle" button below the recognized field output
        solve_recognized_button = ttk.Button(left_frame, text='Solve recognized puzzle', command=self.solve)
        solve_recognized_button.grid(row=3, column=0, pady=5)

        # Right frame for solved matrix output
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, padx=30, pady=30, anchor='ne')  # Increased padding around right frame
        right_frame.grid_columnconfigure(0, weight=1)  # Center alignment for elements in right frame

        # Placeholder2 for solved matrix output
        self.placeholder2 = ttk.Label(right_frame, text="Solved matrix will appear here", relief=tk.SUNKEN,
                                      image=empty_photo)  # Use placeholder image as initial placeholder
        self.placeholder2.image = empty_photo  # Keep reference to avoid garbage collection
        self.placeholder2.grid(row=0, column=0, pady=10, padx=10)

        # Bottom frame for navigation buttons
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)  # Padding around the bottom frame

        # "Back to Main Screen" button at the bottom-right corner
        back_button = ttk.Button(bottom_frame, text='Home', command=lambda: controller.show_frame(MainPage))
        back_button.pack(side=tk.LEFT, padx=10, pady=10)  # Positioned to the right with padding

        # Update frame
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame for displaying in Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        else:
            # Show the placeholder if no camera detected
            self.video_label.configure(image=self.empty_photo)
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
            img = img.resize((350, 350))
            
            # Create a PhotoImage object for display
            imgtk = ImageTk.PhotoImage(image=img)

            # Display the image in the placeholders
            # Scanned sudoku
            self.placeholder1.imgtk = imgtk
            self.placeholder1.configure(image=imgtk)

            # Matrix output (Initial recognized field without solving)
            self.placeholder2.imgtk = imgtk
            self.placeholder2.configure(image=imgtk)

        except Exception as e:
            print(f"Error processing the frame: {e}")
        else:
            print("Failed to capture frame from the camera.")

    def solve(self):
        global original_field  # Use the global variable
        try:
            # Solve the Sudoku
            field = construct_board(self.unwarped)
            original_field = field.copy()  # Save a copy of the original field
            print(field)
            if not solve(field):
                print("No solution exists")
                return

            # Convert recognized field to an image
            recognized_img = Image.fromarray(self.unwarped)
            recognized_img = recognized_img.resize((350, 350))

            # Create a transparent overlay image
            overlay = Image.new('RGBA', (350, 350), (255, 255, 255, 0))

            # Increase the font size for bigger numbers
            bigger_text_font = ImageFont.truetype("arial.ttf", 25)  # Increase the font size to 25

            # Draw the solved numbers onto the overlay image
            draw = ImageDraw.Draw(overlay)
            for i in range(9):
                for j in range(9):
                    if field[i][j] != 0 and not self.is_original_number(i, j):
                        # Ensure numbers are cast to integers and drawn bigger
                        draw.text((j * 38 + 10, i * 38 + 5), str(int(field[i][j])), fill=(255, 0, 0, 255), font=bigger_text_font)

            # Combine the recognized field with the transparent overlay
            combined = Image.alpha_composite(recognized_img.convert('RGBA'), overlay)

            # Display the combined image in the second placeholder
            imgtk = ImageTk.PhotoImage(image=combined)
            self.placeholder2.imgtk = imgtk
            self.placeholder2.configure(image=imgtk)

        except Exception as e:
            print(f"Error solving the Sudoku: {e}")


    def is_original_number(self, row, col):
        # Check if original_field is set and not None
        if original_field is not None:
            # Logic to determine if the number is part of the original puzzle
            return original_field[row][col] != 0
        return False

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

class LoadPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title label
        label = ttk.Label(self, text='Load Image Page', font=('Helvetica', 18, 'bold'))
        label.pack(pady=10, padx=10)

        # Button to open file dialog
        open_button = ttk.Button(self, text='Open Image', command=self.open_file)
        open_button.pack(pady=10)

        # Placeholder for the loaded image
        self.image_label = ttk.Label(self, text='No Image Loaded', relief=tk.SUNKEN)
        self.image_label.pack(pady=10, padx=10)

        # Recognize button
        recognize_button = ttk.Button(self, text='Recognize Puzzle', command=self.recognize_puzzle)
        recognize_button.pack(pady=10)

        # Solve button
        solve_button = ttk.Button(self, text='Solve Puzzle', command=self.solve_puzzle)
        solve_button.pack(pady=10)

        # Back button
        back_button = ttk.Button(self, text='Back to Main Screen', command=lambda: controller.show_frame(MainPage))
        back_button.pack(pady=10)

    def open_file(self):
        # Open a file dialog and select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                # Open the selected image file
                loaded_image = Image.open(file_path)
                loaded_image = loaded_image.resize((350, 350))  # Resize to fit the label
                self.loaded_image = loaded_image  # Store the loaded image for later use

                # Convert to ImageTk and display in the label
                img = ImageTk.PhotoImage(loaded_image)
                self.image_label.configure(image=img, text="")
                self.image_label.image = img  # Keep reference to avoid garbage collection

            except Exception as e:
                print(f"Error loading image: {e}")

    def recognize_puzzle(self):
        try:
            # Ensure an image is loaded
            if not hasattr(self, 'loaded_image'):
                print("No image loaded")
                return

            # Convert loaded image to numpy array
            img_array = np.array(self.loaded_image.convert('RGB'))

            # Process the loaded image to recognize Sudoku puzzle
            self.unwarped = un_warp_sudoku(img_array)
            if self.unwarped is None:
                print("Failed to recognize Sudoku puzzle")
                return

            # Display the recognized Sudoku in the image_label
            img = Image.fromarray(self.unwarped)
            img = img.resize((350, 350))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk  # Keep reference to avoid garbage collection

            print("Puzzle recognized successfully.")

        except Exception as e:
            print(f"Error recognizing puzzle: {e}")

    def solve_puzzle(self):
        global original_field  # Use the global variable
        try:
            # Ensure the puzzle has been recognized before solving
            if not hasattr(self, 'unwarped'):
                print("No puzzle recognized to solve")
                return

            # Construct the Sudoku board from the recognized puzzle
            field = construct_board(self.unwarped)
            original_field = field.copy()  # Save a copy of the original field

            if not solve(field):
                print("No solution exists")
                return

            # Convert recognized field to an image
            recognized_img = Image.fromarray(self.unwarped)
            recognized_img = recognized_img.resize((350, 350))

            # Create a transparent overlay image
            overlay = Image.new('RGBA', (350, 350), (255, 255, 255, 0))

            # Increase the font size for bigger numbers
            bigger_text_font = ImageFont.truetype("arial.ttf", 25)  # Increase the font size to 25

            # Draw the solved numbers onto the overlay image
            draw = ImageDraw.Draw(overlay)
            for i in range(9):
                for j in range(9):
                    if field[i][j] != 0 and not self.is_original_number(i, j):
                        # Ensure numbers are cast to integers and drawn bigger
                        draw.text((j * 38 + 15, i * 38 + 10), str(int(field[i][j])), fill=(255, 0, 0, 255), font=bigger_text_font)

            # Combine the recognized field with the transparent overlay
            combined = Image.alpha_composite(recognized_img.convert('RGBA'), overlay)

            # Display the combined image in the image_label
            imgtk = ImageTk.PhotoImage(image=combined)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

            print("Sudoku solved and overlay applied.")

        except Exception as e:
            print(f"Error solving the Sudoku: {e}")

    def is_original_number(self, row, col):
        # Check if original_field is set and not None
        if original_field is not None:
            # Logic to determine if the number is part of the original puzzle
            return original_field[row][col] != 0
        return False

if __name__ == "__main__":
    app = SudokuSolverApp()
    app.mainloop()
