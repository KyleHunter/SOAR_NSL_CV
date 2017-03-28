'''
*   ImageHandler.py handles basic image taking and processing
*
*   No image processing is done within
*
*   Currently a place holder loading a static image
'''
import cv2


class ImageHandler:

    def __init__(self, testing):
        if not testing:
            print("Error: Not Implemented")
        self.testing, self.image = testing, None

    def resize_image(self, width, height):
        self.image = cv2.resize(self.image, (width, height))

    def take_image(self):
        if self.testing:
            self.image = cv2.imread('simulated_launch_1500ft.jpg', cv2.IMREAD_COLOR)
        else:
            pass

    def show_image(self):
        cv2.imshow('image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
