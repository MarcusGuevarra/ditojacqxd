import cv2
import shutil
import os

currentframe = 1
respondent = 0
def kamera():
    capture_nugget = cv2.VideoCapture(0)

    # for higher image resolution
    capture_nugget.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    capture_nugget.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture_nugget.set(cv2.CAP_PROP_FPS, 60)

    while True:
        ret, image = capture_nugget.read()
        cv2.imshow('Camera', image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('x'):
            saving('orig', image)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            saving('gray', gray_image)

            edge_image = cv2.Canny(image, 70, 70)
            saving('edge', edge_image)

            global currentframe
            currentframe += 1


        elif key == ord('t'):
            global respondent
            print("New respondent")
            respondent += 1
            continue

        elif key == ord('q'):
            break

    capture_nugget.release()
    cv2.destroyAllWindows()


def filename(mode):
    folder = './data/' + mode + '/survey_data/' + str(respondent) + '/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_name = folder + '2_' + str(currentframe) + '.png'
    return image_name


def saving(mode, image):
    image_name = filename(mode)
    cv2.imwrite(image_name, image)
    print('Saved ' + image_name)
