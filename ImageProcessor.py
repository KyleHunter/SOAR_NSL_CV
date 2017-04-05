'''
*   ImageProcessor.py handles image processing
*
*   Will differentiate the different tarps
*
'''

import cv2
import numpy as np
import collections
import warnings
import logging
import os


class ImageProcessor:
    def __init__(self, ih, ei):
        self.ImageHandler = ih
        self.processed_image, self.grayscale_image, self.hsv_image, self.contours, self.mask, self.threshold_image, \
            self.tarp_masks, self.ei, self.scores = None, None, None, [], None, None, [0, 0, 0], ei, []

    def filter_hsv(self, lower, upper):
        self.processed_image = cv2.inRange(self.hsv_image, lower, upper)

    def get_hsv_avg(self):
        h_avg, s_avg, v_avg = np.average(np.average(self.hsv_image, 0), 0)
        h_avg, s_avg, v_avg = int(h_avg), int(s_avg), int(v_avg)
        return h_avg, s_avg, v_avg

    def create_background_mask(self):
        self.hsv_image = self.ImageHandler.cvt_to_hsv()
        h_high = self.get_hsv_avg()[0] + 5
        self.mask = cv2.inRange(self.hsv_image, (h_high, 0, 0), (180, 255, 255))  # Creates mask removing background
        logging.info("Mask(is None): " + str(self.mask is None))
        self.processed_image = cv2.bitwise_and(self.hsv_image, self.hsv_image, mask=self.mask)
        logging.info("processed_image(is None): " + str(self.processed_image is None))
        self.grayscale_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        _, self.threshold_image = cv2.threshold(self.grayscale_image, 1, 255, cv2.THRESH_BINARY)
        logging.info("threshold_image(is None): " + str(self.threshold_image is None))

    def filter_by_size(self, size):
        _, contours, _ = cv2.findContours(self.threshold_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        logging.info("contours(is None): " + str(self.contours is None))
        i = 0
        for c in contours:
            if size[0] < cv2.contourArea(c) < size[1]:
                cv2.drawContours(self.processed_image, contours, i, (255, 255, 255), -1)
            i += 1
        self.grayscale_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        logging.info("grayscale(is None): " + str(self.grayscale_image is None))
        _, self.mask = cv2.threshold(self.grayscale_image, 254, 255, cv2.THRESH_BINARY)
        logging.info("mask(is None): " + str(self.mask is None))
        # Creates mask without background & foreground outside of size

    def get_tarps(self):
        temp = cv2.bitwise_and(self.hsv_image, self.hsv_image, mask=self.mask)  # Masks off background on HSV image
        logging.info("temp(is None): " + str(temp is None))
        self.processed_image = temp
        y, x, _ = temp.shape

        hues = temp[:, :, 0]
        hues = hues[np.nonzero(hues)]
        counter = collections.Counter(hues)
        tarp_hues = self.get_section_means(counter.most_common(50))

        if len(tarp_hues) == 3:
            for i in range(0, 3):  # y, b, r
                self.tarp_masks[i] = cv2.inRange(self.processed_image,
                                                 (int(tarp_hues[i] - 10), 0, 0), (int(tarp_hues[i] + 10), 255, 255))
            logging.info("Perfect, 3 bins found")
        else:
            logging.info("Too many bins found..")

    def save_tarps(self, counter, size):
        files = ['yellow', 'blue', 'red']
        s, cnt_areas = 0, [0, 0, 0]
        os.makedirs("out/" + str(counter))

        for i in range(0, 3):
            img = self.ImageHandler.out_image.copy()
            _, cnts, _ = cv2.findContours(self.tarp_masks[i].copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            logging.info("cnts(is None): " + str(cnts is None))
            h = 0

            for c in cnts:
                if cv2.contourArea(c) > size * 0.2:
                    cv2.drawContours(img, cnts, h, (0, 255, 0), 2)
                    cnt_areas[s] = cv2.contourArea(c)
                h += 1
            s += 1

            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

            cv2.imwrite("out/" + str(counter) + "/" + str(files[i]) + ".png", img)
        score = np.ptp(cnt_areas)
        self.scores.append(score)
        logging.info("File: " + str(counter) + " Score: " + str(score))

    @staticmethod
    def get_section_numbers(coll):
        nums = [coll[x][0] for x in range(0, len(coll)) if coll[x][1] > 30]  #  Only gets Hues with frequency > 30
        nums = np.sort(nums)
        means = np.zeros((50, 50))
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

    def get_section_means(self, coll):
        nums = self.get_section_numbers(coll)
        nums[nums == 0] = np.nan
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            val = np.nanmean(nums, axis=1)
        val = val[~np.isnan(val)]
        return val

    def debug(self):
        cv2.imshow("Processed", self.processed_image)
        cv2.waitKey(0)
