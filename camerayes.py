import cv2
import os

currentframe = 1
respondent = 0

class Camera:
    def __init__(self, video_source=0, width=1080, height=1080, fps=60):
        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps

        self.vid = cv2.VideoCapture(self.video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        # Set camera properties
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.vid.set(cv2.CAP_PROP_FPS, self.fps)

    def get_frame(self):
        if self.vid.isOpened():
            ret, image = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def save_frame(self):
        ret, image = self.vid.read()
        if ret:
            self.saving('orig', image)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.saving('gray', gray_image)

            edge_image = cv2.Canny(image, 70, 70)
            self.saving('edge', edge_image)

            global currentframe
            currentframe += 1

    def imagename(self, mode):
        folder = './data/' + mode + '/survey_data/' + str(respondent) + '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        image_name = folder + '2_' + str(currentframe) + '.png'
        return image_name

    def saving(self, mode, image):
        image_name = self.imagename(mode)
        ret, image = self.vid.read()
        if ret:
            cv2.imwrite(image_name, image)
            print('Saved ' + image_name)

    def new_respondent(self):
        global respondent
        print("New respondent")
        respondent += 1
