import cv2
import imutils  # used for resizing the image without losing aspect ratio

capture_nugget = cv2.VideoCapture(0)

# for higher image resolution
capture_nugget.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
capture_nugget.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
capture_nugget.set(cv2.CAP_PROP_FPS, 60)
# automatically open the window in fullscreen
#cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
#cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

currentframe = 1
while True:
    ret, image = capture_nugget.read()
    cv2.imshow('Camera', image)

    if cv2.waitKey(1) == ord('x'):
        orig_name = './original/' + '2_' + str(currentframe) + '.png'
        cv2.imwrite(orig_name, image)
        print('Saved ' + orig_name + ' - Pixel: ' + str(image.shape))


        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edge_image = cv2.Canny(image,70,70)

        # resized to 28 pix with aspect ratio
        resized_image = imutils.resize(gray_image, width=120)
        resized_edge_image = imutils.resize(edge_image, width=120)
        # if 28x28 is strictly needed then use this code:
        # resized_image = cv2.resize(gray_image, (28,28))0


        gray_name = './grayscale/' + '2_' + str(currentframe) + '.png'
        cv2.imwrite(gray_name, resized_image)
        print('Saved ' + gray_name + ' - Pixel: ' + str(resized_image.shape))

        edge_name = './edge/' + '2_' + str(currentframe) + '.png'
        cv2.imwrite(edge_name, resized_edge_image)
        print('Saved ' + edge_name + ' - Pixel: ' + str(resized_edge_image.shape))


        currentframe += 1

    if cv2.waitKey(1) == ord('q'):
        break

capture_nugget.release()
cv2.destroyAllWindows()