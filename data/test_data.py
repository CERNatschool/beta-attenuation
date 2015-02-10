#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: testing the Strontium-90 dataset.

"""

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

# Import the JSON library.
import json

#...for the datapoints.
from datapoint import DataPoint

#...for appending to the Python path.
import sys

# Add the cernatschool code directory.
sys.path.append("cernatschool")

#...for the Pixelman time string handling.
from handlers import getPixelmanTimeString

class StrontiumDataTest(unittest.TestCase):

    def setUp(self):
        self.datasets = [
            "0-00_mm",
            "0-23_mm",
            "0-36_mm",
            "0-48_mm",
            "0-60_mm",
            "0-72_mm",
            "0-85_mm",
            "1-01_mm",
            "1-46_mm",
            "3-20_mm"
            ]

    def tearDown(self):
        pass

    def test_datasets_exist(self):

        # The tests.

        self.assertEqual(len(self.datasets), 10)

        # Loop through the datasets.
        for data_point_dir_name in sorted(self.datasets):

            ## The data point wrapper class object instance.
            dp = DataPoint(data_point_dir_name, "../tmp")

            input_path = "data/sr/" + dp.get_input_path()

            lg.info(" * Testing '%s'" % (input_path))

            # Does the input directory exist?
            self.assertEqual(os.path.isdir(input_path), True)

            ## Path to the metadata file.
            metadata_path = (input_path + "/metadata.json").replace("//", "/")
            #
            lg.info(" * Testing '%s'..." % (metadata_path))
            self.assertEqual(os.path.exists(metadata_path), True)

            ## Path to the pixel mask file.
            pixel_mask_path = (input_path + "/masked_pixels.txt").replace("//", "/")
            #
            lg.info(" * Testing '%s'..." % (pixel_mask_path))
            self.assertEqual(os.path.exists(pixel_mask_path), True)

            ## Path to the frames information JSON.
            frames_path = (input_path + "/frames.json").replace("//", "/")
            #
            lg.info(" * Testing '%s'..." % (frames_path))
            self.assertEqual(os.path.exists(frames_path), True)

            ## Path to the clusters information JSON.
            klusters_path = (input_path + "/klusters.json").replace("//", "/")
            #
            lg.info(" * Testing '%s'..." % (klusters_path))
            self.assertEqual(os.path.exists(klusters_path), True)

            lg.info(" *")

    def test_0_00_mm_dataset(self):

        # Load the 0.00 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-00_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.00 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 09:55:15.000000 2013")

    def test_0_23_mm_dataset(self):

        # Load the 0.23 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-23_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.23 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 10:06:21.000000 2013")

    def test_0_36_mm_dataset(self):

        # Load the 0.36 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-36_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.36 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 10:17:01.000000 2013")

    def test_0_48_mm_dataset(self):

        # Load the 0.48 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-48_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.48 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 10:26:37.000000 2013")

    def test_0_60_mm_dataset(self):

        # Load the 0.60 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-60_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.60 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 11:01:00.000000 2013")

    def test_0_72_mm_dataset(self):

        # Load the 0.72 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-72_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.72 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 11:14:55.000000 2013")

    def test_0_85_mm_dataset(self):

        # Load the 0.85 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/0-85_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 0.85 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 10:39:50.000000 2013")

    def test_1_01_mm_dataset(self):

        # Load the 1.01 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/1-01_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 1.01 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 11:23:04.000000 2013")


    def test_1_46_mm_dataset(self):

        # Load the 1.46 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/1-46_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 1.46 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 11:08:11.000000 2013")

    def test_3_20_mm_dataset(self):

        # Load the 3.20 mm dataset JSON.

        ## The frame properties JSON file.
        ff = open("data/sr/3-20_mm/frames.json", "r")
        #
        ## The frame properties JSON object.
        fd = json.load(ff)
        #
        ff.close()

        # Check the number of frames.
        self.assertEqual(len(fd), 600)

        # Check the start time of the first frame.
        start_time = sorted([st["start_time"] for st in fd])[0]
        #
        st, sub, start_time_str = getPixelmanTimeString(start_time)
        lg.info(" * 3.20 mm: '%s'" % (start_time_str))
        lg.info(" *")
        #
        self.assertEqual(start_time_str, "Tue Jul 30 10:52:15.000000 2013")


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_data.log', filemode='w', level=lg.INFO)

    lg.info(" *")
    lg.info(" *======================================*")
    lg.info(" * Logger output from data/test_data.py *")
    lg.info(" *======================================*")
    lg.info("")

    unittest.main()
