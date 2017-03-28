'''
*   ImageProcessor.py handles image processing
*
*   Will differentiate the different tarps
*
'''

import cv2
import numpy as np


class ImageProcessor:

    def __init__(self, ih):
        self.ImageHandler = ih
        self.processed_image, self.grayscale_image, self.hsv_image, self.countours, self.mask = \
            None, None, None, [], None

    def cvt_grayscale(self):
        self.grayscale_image = cv2.cvtColor(self.ImageHandler.image, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.grayscale_image

    def cvt_hsv(self):
        self.hsv_image = cv2.cvtColor(self.ImageHandler.image, cv2.COLOR_BGR2HSV)
        self.processed_image = self.hsv_image

    def filter_hsv(self, lower, upper):
        self.processed_image = cv2.inRange(self.hsv_image, lower, upper)

    def get_hsv_avg(self):
        x, y, _ = self.hsv_image.shape
        h_avg, s_avg, v_avg = np.average(np.average(self.hsv_image, 0), 0)
        h_avg, s_avg, v_avg = int(h_avg), int(s_avg), int(v_avg)
        '''
        h_c, s_c, v_c, h_avg1, s_avg1, v_avg1 = 1, 1, 1, 0, 0, 0
        for i in range(0, x):
            for j in range(0, y):

                if self.hsv_image[i, j, 0] > 50:
                    h_avg1 += self.hsv_image[i, j, 0]
                    h_c += 1

                if self.hsv_image[i, j, 1] > 50:
                    s_avg1 += self.hsv_image[i, j, 1]
                    s_c += 1

                if self.hsv_image[i, j, 2] > 50:
                    v_avg1 += self.hsv_image[i, j, 2]
                    v_c += 1

        #print(int(h_avg1 / h_c) + 5)

        return h_avg1 / h_c, s_avg1 / s_c, v_avg1 / v_c
        '''
        return h_avg, s_avg, v_avg

    def get_background_h_high(self):
        return int(self.get_hsv_avg()[0] + 5)

    def hsv_thresh(self, low, high):
        pass

    def remove_background(self):
        self.cvt_grayscale()
        self.cvt_hsv()
        h_high = self.get_background_h_high()
        self.filter_hsv((h_high, 0, 0), (180, 255, 255))

    def create_tarp_mask(self):
        self.mask = cv2.inRange(self.hsv_image, (20, 0, 0), (180, 255, 255))
        self.processed_image = cv2.bitwise_and(self.hsv_image, self.hsv_image, mask=self.mask)




    def debug(self):
        #cv2.imshow("Original", self.ImageHandler.image)
        cv2.imshow("Processed", self.processed_image)
        #cv2.imshow("Mask", self.mask)
        cv2.waitKey(0)
