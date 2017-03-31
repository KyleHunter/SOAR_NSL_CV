'''
*   ImageProcessor.py handles image processing
*
*   Will differentiate the different tarps
*
'''

import cv2
import numpy as np
import collections


class ImageProcessor:
    def __init__(self, ih):
        self.ImageHandler = ih
        self.processed_image, self.grayscale_image, self.hsv_image, self.contours, self.mask, self.threshold_image, \
            self.red_mask, self.blue_mask, self.yellow_mask = None, None, None, [], None, None, None, None, None

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
        return h_avg, s_avg, v_avg

    def get_background_h_high(self):
        return int(self.get_hsv_avg()[0] + 5)

    def hsv_thresh(self, low, high):
        pass

    def create_tarp_mask(self):
        self.cvt_grayscale()
        self.cvt_hsv()
        h_high = self.get_background_h_high()
        self.mask = cv2.inRange(self.hsv_image, (h_high, 0, 0), (180, 255, 255))
        self.processed_image = cv2.bitwise_and(self.hsv_image, self.hsv_image, mask=self.mask)
        self.grayscale_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        _, self.threshold_image = cv2.threshold(self.grayscale_image, 1, 255, cv2.THRESH_BINARY)

    def filter_by_size(self, size):
        _, contours, _ = cv2.findContours(self.threshold_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for c in contours:
            if cv2.contourArea(c) in range(size[0], size[1]):
                cv2.drawContours(self.processed_image, contours, i, (255, 255, 255), -1)
            i += 1
        self.grayscale_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        _, self.mask = cv2.threshold(self.grayscale_image, 254, 255, cv2.THRESH_BINARY)

    def get_tarps(self):
        temp = cv2.bitwise_and(self.hsv_image, self.hsv_image, mask=self.mask)
        y, x, _ = temp.shape
        self.processed_image = temp
        temp = cv2.resize(temp, (int(x * 0.5), int(y * 0.5)))
        x, y, _ = temp.shape
        mylist = []
        for i in range(0, x):
            for j in range(0, y):
                if temp[i, j, 0] != 0:
                    mylist.append(temp[i, j, 0])

        counter = collections.Counter(mylist)

        tarp_hues = self.get_section_means(counter.most_common(50))
        if len(tarp_hues) == 3:
            print('Thank God')

            self.yellow_mask = cv2.inRange(self.processed_image,
                                           (int(tarp_hues[0] - 10), 0, 0), (int(tarp_hues[0] + 10), 255, 255))

            self.blue_mask = cv2.inRange(self.processed_image,
                                         (int(tarp_hues[1] - 10), 0, 0), (int(tarp_hues[1] + 10), 255, 255))

            self.red_mask = cv2.inRange(self.processed_image,
                                        (int(tarp_hues[2] - 10), 0, 0), (int(tarp_hues[2] + 10), 255, 255))

    def save_tarps(self):
        yellow = self.ImageHandler.image.copy()
        _, cnts, _ = cv2.findContours(self.yellow_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(yellow, cnts, -1, (0, 255, 0), 2)

        cv2.imwrite("out/yellow.png", yellow)

        blue = self.ImageHandler.image.copy()
        _, cnts, _ = cv2.findContours(self.blue_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(blue, cnts, -1, (0, 255, 0), 2)

        cv2.imwrite("out/blue.png", blue)

        red = self.ImageHandler.image.copy()
        _, cnts, _ = cv2.findContours(self.red_mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(red, cnts, -1, (0, 255, 0), 2)

        cv2.imwrite("out/red.png", red)

    def get_section_means(self, coll):
        nums = self.get_section_numbers(coll)
        nums[nums == 0] = np.nan
        val = np.nanmean(nums, axis=1)
        val = val[~np.isnan(val)]
        return val

    def get_section_numbers(self, coll):
        nums = [coll[x][0] for x in range(0, len(coll)) if coll[x][1] > 30]
        nums = np.sort(nums)
        means = np.zeros((10, 10))
        i, j = 0, 0
        for s in range(0, len(nums) - 1):
            if nums[s + 1] in range(nums[s] - 5, nums[s] + 5):
                means[i, j] = nums[s]
                j += 1
            else:
                means[i, j] = nums[s]
                i += 1
                j = 0
                means[i, j] = nums[s]
        return means

    def debug(self):
        # cv2.imshow("Original", self.ImageHandler.image)
        cv2.imshow("Processed", self.processed_image)
        # cv2.imshow("ssa", self.edges)
        # cv2.imshow("Mask", self.mask)
        cv2.waitKey(0)
