#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg

#...for the JSON.
import json

#...for the Pixelman dataset wrapper.
from dataset import Dataset

class FrameTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_asciixyc_frame(self):

        ## The dataset wrapper.
        ds = Dataset("data/sr/3-20_mm/ASCIIxyC/")

        ## The frame metadata.
        fmd = None
        #
        with open("data/sr/3-20_mm/metadata.json", "r") as fmdf:
            fmd = json.load(fmdf, fmd)
        #
        lat, lon, alt = fmd[0]['lat'], fmd[0]['lon'], fmd[0]['alt']

        ## The pixel mask.
        pixel_mask = {}

        with open("data/sr/3-20_mm/masked_pixels.txt", "r") as mpf:
            rows = mpf.readlines()
            for row in rows:
                vals = [int(val) for val in row.strip().split("\t")]
                x = vals[0]; y = vals[1]; X = (256*y) + x; C = 1
                pixel_mask[X] = C

        ## The frames from the dataset.
        frames = ds.getFrames((lat, lon, alt), pixelmask=pixel_mask)

        # The tests
        #-----------
        #
        # The number of frames.
        self.assertEqual(len(frames), 600)
        #
        # Spatial information.
        self.assertEqual(frames[0].getLatitude(),  51.261015)
        self.assertEqual(frames[0].getLongitude(), -1.084127)
        self.assertEqual(frames[0].getAltitude(),  48.0     )
        #
        self.assertEqual(frames[0].getRoll(), 0.0)
        self.assertEqual(frames[0].getPitch(), 0.0)
        self.assertEqual(frames[0].getYaw(), 0.0)
        #
        self.assertEqual(frames[0].getOmegax(), 0.0)
        self.assertEqual(frames[0].getOmegay(), 0.0)
        self.assertEqual(frames[0].getOmegaz(), 0.0)
        #
        # Temporal information.
        self.assertEqual(frames[0].getStartTime(), 1375181535.850145)
        self.assertEqual(frames[0].getStartTimeSec(), 1375181535)
        self.assertEqual(frames[0].getStartTimeSubSec(), 850145)
        self.assertEqual(frames[0].getEndTime(), 1375181536.350145)
        self.assertEqual(frames[0].getEndTimeSec(), 1375181536)
        self.assertEqual(frames[0].getEndTimeSubSec(), 350145)
        self.assertEqual(frames[0].getAcqTime(), 0.5)
        #
        # Detector information.
        self.assertEqual(frames[0].getChipId(), "E09-W0211")
        #
        self.assertEqual(frames[0].getBiasVoltage(), 94.5)
        self.assertEqual(frames[0].getIKrum(), 1)
        #
        self.assertEqual(frames[0].getDetx(), 0.0)
        self.assertEqual(frames[0].getDety(), 0.0)
        self.assertEqual(frames[0].getDetz(), 0.0)
        self.assertEqual(frames[0].getDetEulera(), 0.0)
        self.assertEqual(frames[0].getDetEulerb(), 0.0)
        self.assertEqual(frames[0].getDetEulerc(), 0.0)
        #
        # Payload information.
        self.assertEqual(frames[0].getWidth(), 256)
        self.assertEqual(frames[0].getHeight(), 256)
        self.assertEqual(frames[0].getFormat(), 4114)
        self.assertEqual(frames[0].getRawNumberOfPixels(), 1)
        self.assertEqual(frames[0].getOccupancy(), 1)
        self.assertAlmostEqual(frames[0].getOccupancyPc(), 0.000015, places=6)
        self.assertEqual(frames[0].getNumberOfUnmaskedPixels(), 1)
        #
        self.assertEqual(frames[0].isMC(), False)

        # The masked pixels.
        self.assertEqual(frames[0].getNumberOfMaskedPixels(), 0)

        #
        # Cluster information.
        self.assertEqual(frames[0].getNumberOfKlusters(), 1)
        self.assertEqual(frames[0].getNumberOfGammas(), 1)
        self.assertEqual(frames[0].getNumberOfMonopixels(), 1)
        self.assertEqual(frames[0].getNumberOfBipixels(), 0)
        self.assertEqual(frames[0].getNumberOfTripixelGammas(), 0)
        self.assertEqual(frames[0].getNumberOfTetrapixelGammas(), 0)
        self.assertEqual(frames[0].getNumberOfNonGammas(), 0)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_frame.log', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("===============================================")
    lg.info(" Logger output from cernatschool/test_frame.py ")
    lg.info("===============================================")
    lg.info("")

    unittest.main()
