#!/usr/bin/env python

"""

 CERN@school - Perform the analysis.

 See the README.md for more information.

"""

# Import the code needed to manage files.
import os, inspect

#..for the sake of argument(s).
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for the MATH.
import numpy as np

from plotting.attenuation import DataPoint, DataPoints, AttenuationPlot


#
# The main program.
#
if __name__=="__main__":

    print("==================================")
    print("  CERN@school - Perform Analysis  ")
    print("==================================")

    # Get the datafile path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",  help="Path to the input dataset.")
    parser.add_argument("outputPath", help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data.
    datapath = args.inputPath
    #
    ## The input data JSON.
    input_json_path = (datapath + "/beta_results.json").replace("//", "/")
    #
    # Check if the input JSON exists. If it doesn't, quit.
    if not os.path.exists(input_json_path):
        raise IOError("* ERROR: '%s' does not exist!" % (input_json_path))

    ## The output path.
    outputpath = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Set the logging level to DEBUG.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=outputpath + '/log_perform-analysis.log', filemode='w', level=level)

    print("*")
    print("* Results JSON        : '%s'" % (input_json_path))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    ## The path to the analysis results directory.
    results_path = ("%s/results/" % (outputpath)).replace("//", "/")
    #
    if os.path.isdir(results_path):
        rmtree(results_path)
        lg.info(" * Removing directory '%s'..." % (results_path))
    os.mkdir(results_path)
    lg.info(" * Creating directory '%s'..." % (results_path))


    # Load the input data.

    rjf = open(input_json_path, "r")
    #
    ## The results JSON information.
    rjd = json.load(rjf)
    #
    rjf.close()

    ## The assumed number of particles attempting to penetrate the material.
    #
    # Taken from the number of beta candidates detected without any material
    # present (i.e. the 0.00 [mm] dataset.
    B_0 = rjd['0.0']

    # Remove the baseline datapoint from the dataset.
    # Remember, this had no material involved and so should not be considered
    # part of the estimate of \mu.
    del rjd['0.0']

    ## A list of datapoints.
    dps = []

    # Populate the datapoint list.
    for key, val in rjd.iteritems():
        dps.append(DataPoint(float(key), float(val), B_0))

    # Sort the list by thickness.
    dps = sorted(dps)

    ## The points to plot in the results plot.
    points = DataPoints(dps)

    # Create the plot.
    attplot = AttenuationPlot(points, x_label='$d_{i}$', y_label='$\ln \, B_{i}$', x_max = 3.5, fig_height = 6.0)

    attplot.save_plot(results_path, "att")

    # Create the results page.

    ## The results page text.
    ipg = ""
    ipg += "<!DOCTYPE html>\n"
    ipg += "<html>\n"
    ipg += "  <head>\n"
    ipg += "    <title>Beta Attenuation: the results.</title>\n"
    ipg += "  </head>\n"
    ipg += "  <body>\n"
    ipg += "    <h1>CERN@school: Beta Attenuation Results</h1>\n"
    ipg += "    <table>\n"
    ipg += "      <tr>\n"
    ipg += "      <td><img src='att.png' /></td>\n"
    ipg += "      <td>\n"
    ipg += "        &mu; = (%5.3f &pm; %5.3f) <br />\n" % \
        (points.get_estimated_attenuation_coefficient(), \
         points.get_error_on_the_estimated_attenuation_coefficient())
    ipg += "        <br />\n"
    ipg += "        &lt; x &gt; = (%5.3f &pm; %5.3f) <br />\n" % \
        (points.get_estimated_mean_free_path(), \
         points.get_error_on_the_estimated_mean_free_path())
    ipg += "        <br />\n"
    ipg += "        &chi;<sup>2</sup> = %6.4f (N<sub>free.</sub> = %d)\n" % \
        (points.get_chi_squared_fit_value(), \
         points.get_chi_squared_fit_dof())
    ipg += "        <br />\n"
    ipg += "        <br />\n"
    ipg += points.write_html_table()
    ipg += "      </td>\n"
    ipg += "      </tr>\n"
    ipg += "    </table>\n"
    ipg += "  </body>\n"
    ipg += "</html>"

    ## The name of the file to write the results page to.
    index_page_name = (results_path + "/index.html").replace("//", "/")

    ## The text file for the HTML page.
    f = open(index_page_name, "w")
    f.write(ipg)
    f.close()

    ## The name of the file to write the LaTeX results table to.
    table_file_name = (results_path + "/table.tex").replace("//", "/")

    # The .tex file for the LaTeX table entries.
    f = open(table_file_name, "w")
    f.write(points.write_latex_table())
    f.close()

    # Now you can view "index.html" to see your results!
    print("*")
    print("* Sorting complete.")
    print("* View your results by opening '%s' in a browser, e.g." % (index_page_name))
    print("* firefox %s &" % (index_page_name))
