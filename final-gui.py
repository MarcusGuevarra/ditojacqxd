import tkinter as tk
from tkinter import messagebox
import camera as cm
import AI_model as ai


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def aimod():
    # Create the main window
    aim = tk.Toplevel(root)
    aim.title("AI model GUI")

    # Set the size of the window
    aim.geometry("750x500")
    aim.resizable(True, True)
    gf.center_window(aim)

    # Create a label
    ailabel = tk.Label(aim, text="Select Image Processing Technique", font=("Arial",14))
    ailabel.pack(pady=30)

    orig_button = tk.Button(aim, text="ORIGINAL", command=ai.original)
    orig_button.pack(pady=30)

    gray_button = tk.Button(aim, text="GRAYSCALE", command=ai.grayscale)
    gray_button.pack(pady=30)

    edge_button = tk.Button(aim, text="EDGE DETECTION", command=ai.edge_detection)
    edge_button.pack(pady=30)

    next_respondent_button = tk.Button(aim, text="Next Respondent", command=aim.destroy)
    next_respondent_button.pack(pady=30)

    aim.mainloop()


# Main window
root = tk.Tk()
root.title("AUTOMATIC FOOD OIL DETECTION")
root.geometry("750x500")
root.resizable(False,False)
center_window(root)

# Title
text_var = tk.StringVar()
text_var.set("AUTOMATIC FOOD OIL DETECTION: AN AI AND IMAGE PROCESSING APPROACH " +
             "FOR QUALITY CONTROL AND DIETARY MONITORING")
label = tk.Label(root, textvariable=text_var, font=("Arial", 16, "bold"), wraplength=500)
label.pack(pady=50)

new_respondent_button = tk.Button(root, text="New Respondent", command=cm.kamera)
new_respondent_button.pack(pady=30)

ai_model_button = tk.Button(root, text="AI_model", command=aimod)
ai_model_button.pack(pady=30)

root.mainloop()
