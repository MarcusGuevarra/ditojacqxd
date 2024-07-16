import cv2

capture_nugget = cv2.VideoCapture(0)

# for higher image resolution
capture_nugget.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
capture_nugget.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
capture_nugget.set(cv2.CAP_PROP_FPS, 60)

def filename(mode, currentframe):
    image_name = './data/' + mode + '/2_' + str(currentframe) + '.png'
    return image_name

currentframe = 1
while True:
    ret, image = capture_nugget.read()
    cv2.imshow('Camera', image)

    if cv2.waitKey(1) == ord('x'):
        orig_name = filename('orig', currentframe)
        cv2.imwrite(orig_name, image)
        print('Saved ' + orig_name)


        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edge_image = cv2.Canny(image,70,70)


        gray_name = filename('gray', currentframe)
        cv2.imwrite(gray_name, gray_image)
        print('Saved ' + gray_name)

        edge_name = filename('edge', currentframe)
        cv2.imwrite(edge_name, edge_image)
        print('Saved ' + edge_name)


        currentframe += 1

    if cv2.waitKey(1) == ord('q'):
        break

capture_nugget.release()
cv2.destroyAllWindows()