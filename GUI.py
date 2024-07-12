import tkinter as tk
from camerapy2 import capture

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Set the size of the window
root.geometry("750x500")
root.resizable(True,True)

# Create a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

# Create a button
def on_button_click():
    capture()


button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=20)

# Run the application
root.mainloop()
