import tkinter as tk
#from cameranugget import camera, capture_image, currentframe, close_camera
from AImodel import edge_detection, original, grayscale

# Create the main window
root = tk.Tk()
root.title("AUTOMATIC FOOD OIL DETECTION")

# Set the size of the window
root.geometry("750x500")
root.resizable(True,True)

# Create a label
label = tk.Label(root, text="Select which type of images to process through the AI:")
label.pack(pady=20)


def image_modes():
    original_button = tk.Button(root, text="ORIGINAL", command=original)
    original_button.pack(pady=30)

    gray_button = tk.Button(root, text="GRAYSCALE", command=grayscale)
    gray_button.pack(pady=30)

    edge_button = tk.Button(root, text="EDGE DETECTION", command=edge_detection)
    edge_button.pack(pady=30)


# Run the application
root.mainloop()

