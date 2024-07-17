import sys

import cv2

currentframe = 0


def camera():
    capture_nugget = cv2.VideoCapture(0)
    # for higher image resolution
    capture_nugget.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    capture_nugget.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture_nugget.set(cv2.CAP_PROP_FPS, 60)

    if not capture_nugget.isOpened():
        sys.exit()

    return  capture_nugget

def filename(mode):
    image_name = './data/' + mode + '/test/2_' + str(currentframe) + '.png'
    return image_name


def save_file(mode, image):
    image_name = filename(mode)
    cv2.imwrite(image_name, image)
    print('Saved ' + image_name)


def capture_image():
    capture_nugget = camera()
    ret, image = capture_nugget.read()
    cv2.imshow('Camera Nugget', image)

    save_file('orig', image)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save_file('gray', gray_image)

    edge_image = cv2.Canny(image, 70, 70)
    save_file('edge', edge_image)

    global currentframe
    currentframe += 1


def close_camera():
    capture_nugget = camera()
    capture_nugget.release()
