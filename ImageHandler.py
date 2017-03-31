'''
*   ImageHandler.py handles basic image taking and processing
*
*   Handles all color conversions, outputs to out_image
*
*   Currently a place holder loading a static image
'''
import cv2


class ImageHandler:

    def __init__(self, testing):
        if not testing:
            print("Error: Not Implemented")
        self.testing, self.out_image, self._original_image = testing, None, None

    def take_image(self):
        if self.testing:
            self._original_image = cv2.imread('simulated_launch_1500ft.jpg', cv2.IMREAD_COLOR)
            self.out_image = self._original_image
        else:
            pass

    def show_image(self):
        cv2.imshow('image', self.out_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cvt_to_grayscale(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2GRAY)

    def cvt_to_hsv(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2HSV)
