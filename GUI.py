import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("AUTOMATIC FOOD OIL DETECTION")

# Set the size of the window
root.geometry("750x500")
root.resizable(True,True)

# Create a label
label = tk.Label(root, text="Select which type of images to process through the AI:")
label.pack(pady=20)

from camerapy2 import capture_image

camera_button = tk.Button(root, text="CAPTURE", command=capture_image)
camera_button.pack(pady=30)

from AImodel import edge_detection, original, grayscale

original_button = tk.Button(root, text="ORIGINAL", command=original)
original_button.pack(pady=30)

gray_button = tk.Button(root, text="GRAYSCALE", command=grayscale)
gray_button.pack(pady=30)

edge_button = tk.Button(root, text="EDGE DETECTION", command=edge_detection)
edge_button.pack(pady=30)

# Run the application
root.mainloop()
