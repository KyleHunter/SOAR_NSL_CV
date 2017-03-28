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
        self.processed_image, self.grayscale_image, self.hsv_image, self.countours = None, None, None, []

    def cvt_grayscale(self):
        self.grayscale_image = cv2.cvtColor(self.ImageHandler.image, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.grayscale_image

    def cvt_hsv(self):
        self.hsv_image = cv2.cvtColor(self.ImageHandler.image, cv2.COLOR_BGR2HSV)
        self.processed_image = self.hsv_image

    def filter_hsv(self, lower, upper):
        self.mask = cv2.inRange(self.hsv_image, lower, upper)
        self.processed_image = self.mask

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

    def threshold(self, pixels):
        pass

    def remove_background(self):
        self.cvt_grayscale()
        self.cvt_hsv()
        h_high = self.get_background_h_high()
        self.filter_hsv((h_high, 0, 0), (180, 255, 255))

    def filter_size(self, pixel_size):
        _, cnt, _ = cv2.findContours(self.processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt:
            if cv2.contourArea(c) > pixel_size:
                self.countours.append(c)

        cv2.drawContours(self.ImageHandler.image, self.countours, -1, (150, 200), 1)

    def debug(self):
        cv2.imshow("Original", self.ImageHandler.image)
        cv2.imshow("Processed", self.processed_image)
        cv2.waitKey(0)
