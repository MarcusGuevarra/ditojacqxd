import cv2


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
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def save_frame(self, filename="snapshot.png"):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite(filename, frame)





