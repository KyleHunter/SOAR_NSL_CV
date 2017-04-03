'''
*   ImageHandler.py handles basic image taking and processing
*
*   Handles all color conversions, outputs to out_image
*
*   Currently a place holder loading a static image
'''
import cv2


class ImageHandler:
    def __init__(self, testing, ei):
        self.testing, self.out_image, self._original_image, self.ei = testing, None, None, ei

    def is_blurry(self):
        focus = cv2.Laplacian(self.cvt_to_grayscale(), cv2.CV_64F).var()
        if focus < 50:
            return True
        else:
            return False

    def take_image(self):
        if self.testing:
            self._original_image = cv2.imread('tarps.jpg', cv2.IMREAD_COLOR)
            self.out_image = self._original_image
        else:
            cap = cv2.VideoCapture(0)
            _, self._original_image = cap.read()
            self.out_image = self._original_image

    def show_image(self):
        cv2.imshow('image', self.out_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cvt_to_grayscale(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2GRAY)

    def cvt_to_hsv(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2HSV)
