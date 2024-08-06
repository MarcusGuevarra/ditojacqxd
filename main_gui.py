import tkinter as tk
from tkinter import Button, Label, messagebox
from PIL import Image, ImageTk
from camera import Camera
from AI_model import original, edge_detection, grayscale


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
        window.geometry("642x590")
        center_window(window)
        self.camera = None
        self.camera_run = False

        self.canvas = tk.Canvas(window)
        self.canvas.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas.config(width=642, height=480)

        self.btn_start_camera = Button(window, text="Start Camera", underline=6, command=self.start_camera)
        self.btn_start_camera.grid(row=2, column=1, columnspan=3, sticky='nsew')
        window.bind('<c>', self.start_camera)
        window.bind('<C>', self.start_camera)

        self.btn_snapshot = Button(window, text="Snapshot", underline=0, command=self.snapshot)
        self.btn_snapshot.grid(row=3, column=0, columnspan=3, sticky='nsew')
        window.bind('<s>', self.snapshot)
        window.bind('<S>', self.snapshot)

        self.ai_model_button = Button(window, text="AI Model", underline=0,
                                      command=lambda: [self.window.withdraw(), self.aimodel()])
        self.ai_model_button.grid(row=4, column=0, columnspan=3, sticky='nsew')
        window.bind('<a>', lambda event: [self.window.withdraw(), self.aimodel()])
        window.bind('<A>', lambda event: [self.window.withdraw(), self.aimodel()])

        self.btn_quit = Button(window, text="Exit", underline=1, command=self.quit)
        self.btn_quit.grid(row=5, column=0, columnspan=3, sticky='nsew')
        window.bind('<x>', self.quit)
        window.bind('<X>', self.quit)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def start_camera(self, event=None):
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

    def snapshot(self, event=None):
        if self.camera:
            self.camera.save_frame()
        messagebox.showinfo('Information', 'Images Saved')

    def quit(self, event=None):
        thesis_title = ('Automatic Food Oil Detection: An AI and Image Processing Approach'
                        + ' for Quality Control and Dietary Monitoring')
        messagebox.showinfo('Thesis Title', thesis_title)
        self.on_closing()
        self.window.quit()

    def aimodel(self, event=None):
        aim = tk.Tk()
        aim.title("AI model")
        aim.geometry("690x150")
        center_window(aim)
        aim.focus_set()
        aim.grab_set()
        frame = tk.Frame(aim, padx='10', pady='10')
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ai_label = Label(aim, text="Select Image Processing Technique", font=("", 15))
        ai_label.grid(row=1, column=0, columnspan=3, pady=5)

        desc_label = Label(aim, text="This indicates the type of images that the AI will use " +
                                     "as a dataset for its training and testing.",
                                     font=("", 9))
        desc_label.grid(row=2, column=0, columnspan=3, pady=3)

        orig_button = Button(aim, width=30, text="ORIGINAL", underline=0, command=original)
        orig_button.grid(row=3, column=0, pady=5, padx=5)
        aim.bind('<o>', original)
        aim.bind('<O>', original)

        gray_button = Button(aim, width=30, text="GRAYSCALE", underline=0, command=grayscale)
        gray_button.grid(row=3, column=1, pady=5, padx=5)
        aim.bind('<g>', grayscale)
        aim.bind('<G>', grayscale)

        edge_button = Button(aim, width=30, text="EDGE DETECTION", underline=0, command=edge_detection)
        edge_button.grid(row=3, column=2, pady=5, padx=5)
        aim.bind('<e>', edge_detection)
        aim.bind('<E>', edge_detection)

        next_respondent_button = Button(aim, width=60, text="Next Respondent", underline=0,
                                        command=lambda: [aim.destroy(), self.window.deiconify(), self.camera.new_respondent()])
        next_respondent_button.grid(row=4, column=0, columnspan=3, pady=5, padx=5)
        aim.bind('<n>', lambda event: [aim.destroy(), self.window.deiconify(), self.camera.new_respondent(event=None)])
        aim.bind('<N>', lambda event: [aim.destroy(), self.window.deiconify(), self.camera.new_respondent(event=None)])

        aim.mainloop()

    def on_closing(self):
        if self.camera:
            del self.camera
        self.window.destroy()


root = tk.Tk()
app = CameraApp(root, "Automatic Food Oil Detection")

