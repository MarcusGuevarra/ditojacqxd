import tkinter as tk
# import camerapy2

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Set the size of the window
root.geometry("750x500")
root.resizable(True,True)

# Create a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

from AImodel import edge_detection, original, grayscale

button_1 = tk.Button(root, text="EDGE DETECTION", command=edge_detection)
button_1.pack(pady=30)

button_2 = tk.Button(root, text="GRAYSCALE", command=grayscale)
button_2.pack(pady=30)

button_3 = tk.Button(root, text="ORIGINAL", command=original)
button_3.pack(pady=30)


# Run the application
root.mainloop()
