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

def on_button_click_1():
    capture()

def on_button_click_2():
    capture()

def on_button_click_3():
    capture()




button_1 = tk.Button(root, text="Click Me", command=on_button_click_1)
button_1.pack(pady=30)

button_2 = tk.Button(root, text="Click Me", command=on_button_click_2)
button_2.pack(pady=30)

button_3 = tk.Button(root, text="Click Me", command=on_button_click_3)
button_3.pack(pady=30)


# Run the application
root.mainloop()
