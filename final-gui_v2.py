import tkinter as tk
from tkinter import Button
from PIL import Image, ImageTk
from kamera import Camera
import AI_model as ai


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.camera = None
        self.camera_run = False

        self.canvas = tk.Canvas(window)
        self.canvas.pack()

        self.btn_start_camera = Button(window, text="Start Camera", width=50, command=self.start_camera)
        self.btn_start_camera.pack(anchor=tk.CENTER, expand=True)

        self.btn_snapshot = Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.ai_model_button = tk.Button(root, text="AI model", width=50, command=lambda: [self.window.withdraw(), self.aimod()])
        self.ai_model_button.pack(anchor=tk.CENTER, expand=True)

        self.btn_quit = Button(window, text="Exit", width=50, command=self.quit)
        self.btn_quit.pack(anchor=tk.CENTER, expand=True)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def start_camera(self):
        if self.camera is None:
            self.camera = Camera(width=640, height=480, fps=60)
            self.canvas.config(width=self.camera.width, height=self.camera.height)

        if not self.camera_run:
            self.camera_run = True
            self.update()

    def update(self):
        if self.camera and self.camera_run:
            ret, frame = self.camera.get_frame()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.window.after(int(1000 / self.camera.fps), self.update)

    def snapshot(self):
        if self.camera:
            self.camera.save_frame()

    def quit(self):
        self.on_closing()
        self.window.quit()

    def aimod(self):
        # Create the main window
        aim = tk.Toplevel(root)
        aim.title("AI model GUI")

        # Set the size of the window
        aim.geometry("750x500")
        aim.resizable(True, True)

        # Create a label
        ai_label = tk.Label(aim, text="Select Image Processing Technique for the AI dataset", font=("Arial", 14))
        ai_label.pack(pady=30)

        orig_button = tk.Button(aim, text="ORIGINAL", command=ai.original)
        orig_button.pack(pady=30)

        gray_button = tk.Button(aim, text="GRAYSCALE", command=ai.grayscale)
        gray_button.pack(pady=30)

        edge_button = tk.Button(aim, text="EDGE DETECTION", command=ai.edge_detection)
        edge_button.pack(pady=30)

        next_respondent_button = tk.Button(aim, text="Next Respondent", command=lambda: [aim.destroy(), self.window.deiconify(), self.camera.new_respondent()])
        next_respondent_button.pack(pady=30)

        aim.mainloop()

    def on_closing(self):
        if self.camera:
            del self.camera
        self.window.destroy()


root = tk.Tk()
app = CameraApp(root, "Automatic Oil Detection")

