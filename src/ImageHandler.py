'''
*   ImageHandler.py handles basic image taking and processing
*
*   Handles all color conversions, outputs to out_image
*
*   Currently a place holder loading a static image
'''
import cv2
import numpy as np
import logging

main_logger = logging.getLogger("SOAR.main_logger")


class ImageHandler:
    def __init__(self, testing, ei):
        self.testing, self.out_image, self._original_image, self.ei, self.blur_thresh = testing, None, None, ei, 100
        self.take_image()

    def camera_error(self):
        if self.is_valid_image():# Try catch for usb TODO
            main_logger.info("Camera took valid image, no error")
            return False
        else:
            return True

    def is_blurry(self):
        focus = cv2.Laplacian(self.cvt_to_grayscale(), cv2.CV_64F).var()
        if focus < self.blur_thresh:
            self.blur_thresh += 20  # Ensure we at least take some pics..
            main_logger.info("Blurry image, blur_thresh = " + str(self.blur_thresh))
            return True
        else:
            self.blur_thresh = 100
            main_logger.info("Clear image, blur_thresh = " + str(self.blur_thresh))
            return False

    def is_valid_image(self):
        self.take_image()
        if np.mean(self.out_image) > 20:
            return True
        else:
            return False

    def take_image(self):
        if self.testing:
            self._original_image = cv2.imread('tarps.jpg', cv2.IMREAD_COLOR)
            self.out_image = self._original_image
            return True
        else:
            cap = cv2.VideoCapture(0)
            for i in range(0, 10):  # First couple frames are garbage
                _, self._original_image = cap.read()
            self.out_image = self._original_image
            cap.release()
            return not self.is_blurry()

    def show_image(self):
        cv2.imshow('image', self.out_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cvt_to_grayscale(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2GRAY)

    def cvt_to_hsv(self):
        return cv2.cvtColor(self._original_image, cv2.COLOR_BGR2HSV)
