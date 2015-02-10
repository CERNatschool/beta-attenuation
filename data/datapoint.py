#!/usr/bin/env python
# -*- coding: utf-8 -*-


#...for the logging.
import logging as lg


class DataPoint:

    def __init__(self, path_to_subdir, outputpath):
        """
        Constructor.
        @param [in] path_to_subdir The path to the sub-directory.
        @param [in] outputpath The output path to write to.
        """

        ## The full path to the (input) sub-directory.
        self.__full_path = path_to_subdir.replace("//", "/")

        ## The name of the sub-diractory.
        self.__subdir_name = path_to_subdir.split("/")[-1]

        self.__subdir_path = (outputpath + "/" + self.__subdir_name).replace("//", "/")

        ## The unit of the dataset's measurement.
        self.__unit = str(self.__subdir_name.split("_")[-1])

        ## The value of the dataset's measurement.
        self.__value = float(self.__subdir_name.split("_")[0].replace("-", "."))

        lg.debug(" *")
        lg.debug(" * Initialising DataPoint object from '%s':" % (self.__full_path))
        lg.debug(" *")
        lg.debug(" *--> Measurement: %f [%s]" % (self.__value, self.__unit))
        lg.debug(" *")

    def __lt__(self, other):
        return self.__value < other.__value

    def get_name(self):
        return self.__subdir_name

    def get_input_path(self):
        return self.__full_path

    def get_output_path(self):
        return self.__subdir_path

    def get_value(self):
        return self.__value

    def get_unit(self):
        return self.__unit
