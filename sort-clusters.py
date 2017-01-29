#!/usr/bin/env python

"""

 CERN@school - Sorting Clusters

 See the README.md for more information.

"""

# Import the code needed to manage files.
import os, inspect, glob, argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree, copyfile

# Import the JSON library.
import json

# Import the plotting libraries.
import pylab as plt

# For plotting etc.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

# Get the path of the current directory
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

from cernatschool.datavals import TRIPIXEL_RADIUS, TETRAPIXEL_RADIUS

from data.datapoint import DataPoint

#
# The main program.
#
if __name__=="__main__":

    print("===============================")
    print("  CERN@school - Sort Clusters  ")
    print("===============================")

    # Get the datafile path from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",  help="Path to the input dataset.")
    parser.add_argument("outputPath", help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

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
    lg.basicConfig(filename=outputpath + '/log_sort-clusters.log', filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output file         : '%s'" % (outputpath))
    print("*")

    # Loop over the datasets to get the JSONs.

    ## A list of the data points.
    data_points = []

    for entry in sorted(glob.glob((datapath + "/*").replace("//", "/"))):
        if os.path.isdir(entry):
            data_points.append(DataPoint(entry, outputpath))

    # Sort the data points.
    data_points = sorted(data_points)

    ## Dictionary for the results JSON.
    beta_results = {}

    # Create the subdirectories.
    for dp in data_points:

        print("* Processing '%s'." % (dp.get_name()))
        print("*--> Input:  '%s'." % (dp.get_input_path()))
        print("*--> Output: '%s'." % (dp.get_output_path()))
        print("*")

        # If it exists, delete it.
        if os.path.isdir(dp.get_output_path()):
            rmtree(dp.get_output_path())
            #lg.info(" * Skipping directory '%s'..." % (dp.get_output_path()))
            #print(" * Skipping directory '%s'..." % (dp.get_output_path()))
            #continue
        os.mkdir(dp.get_output_path())
        lg.info(" * Creating directory '%s'..." % (dp.get_output_path()))
        lg.info("")

        ## The cluster properties JSON file - FIXME: check it exists...
        kluster_json_path = (dp.get_input_path() + "/klusters.json").replace("//", "/")
        #
        if not os.path.exists(kluster_json_path):
            raise IOError("* ERROR! '%s' doesn't exist." % (kluster_json_path))

        kf = open(kluster_json_path, "r")
        #
        kd = json.load(kf)
        kf.close()

        ## Dictionary of the clusters { id:type }.
        ks = {}

        ## Dictionary of the cluster sizes { id:size }.
        ksizes = {}

        ## Dictionary of the cluster radii { id:radius }.
        krads = {}

        ## Dictionary of the cluster densities { id:density }.
        kdens = {}

        ## Dictionary of the cluster linearity { id:linearity }.
        klins = {}

        ## Dictionary of the clusters' fraction of inner pixels { id:innerfrac }.
        kinners = {}

        ## Dictionary of the cluster total counts { id:totalcounts }.
        kttcs = {}

        ## Dictionary of the clusters' max. count value { id:maxcounts }.
        kmxcs = {}

        ## List of the cluster types.
        alltypes = ["None", "Edge", "Alpha", "Beta", "Gamma"]

        ## The number of edge clusters.
        n_edge_klusters = 0

        # Loop over the klusters.
        for k in kd:

            # Add to the cluster property dictionaries.
            ksizes[k["id"]] = k["size"]
            krads[k["id"]]  = k["radius_uw"]
            kdens[k["id"]]  = k["density_uw"]
            klins[k["id"]]  = k["lin_linearity"]
            kinners[k["id"]] = k["innerfrac"]
            kttcs[k["id"]] = k["totalcounts"]
            kmxcs[k["id"]] = k["maxcounts"]

            # Check if the cluster is on the edge of the frame.
            if k["xmin"] <= 0.1 or k["xmax"] >= 254.9 or k["ymin"] <= 0.1 or k["ymax"] >= 254.9:
                ks[k["id"]] = "Edge"
                n_edge_klusters += 1
                continue

            # Everything but gamma (or edge) is a beta (Strontium-90 data only!).
            if   k['size'] == 1:
                ks[k['id']] = "Gamma"
            elif k['size'] == 2:
                ks[k['id']] = "Gamma"
            elif k['size'] == 3:
                if k['radius_uw'] <= TRIPIXEL_RADIUS:
                    ks[k['id']] = "Gamma"
                else:
                    ks[k['id']] = "Beta"
            elif k['size'] == 4:
                if k['radius_uw'] <= TETRAPIXEL_RADIUS:
                    ks[k['id']] = "Gamma"
                else:
                    ks[k['id']] = "Beta"
            else:
                ks[k['id']] = "Beta"

        lg.info(" *")
        lg.info(" * SUMMARY:")
        lg.info(" *")
        for cid, ctype in ks.iteritems():
            lg.info(" * %s is '%s'." % (str(cid), str(ctype)))
        print("*")
        print("* Sorted %d clusters!" % (len(ks)))

        ## Path to the sorting HTML page.
        homepage_name = (dp.get_output_path() + "/index.html").replace("//", "/")

        ## The index page for the sorted clusters.
        pg = ""

        pg += "<!DOCTYPE html>\n"
        pg += "<html>\n"
        pg += "  <head>\n"
        pg += "    <title>Cluster sorting: %4.2f [%s]</title>\n" % (dp.get_value(), dp.get_unit())
        pg += "  </head>\n"
        pg += "  <body>\n"
        pg += "    <h1>CERN@school: Cluster Sorting for %4.2f [%s]</h1>\n" % (dp.get_value(), dp.get_unit())
        pg += "    <p>Back to the <a href='../index.html'>datasets home</a>.</p>\n"
        pg += "    <h2>Dataset summary</h2>\n"
        pg += "    <p>\n"
        pg += "      <ul>\n"
        pg += "        <li>Dataset path = '%s'</li>\n" % (dp.get_input_path())
        pg += "        <li>Number of clusters = %d</li>\n" % (len(kd))
        pg += "      </ul>\n"
        pg += "    </p>\n"
        pg += "    <h2>Cluster types</h2>\n"

        pg += "    <p>\n"

        # Make this into a table.
        pg += "      <table>\n"
        pg += "        <tr><th>Type</th><th colspan=\"2\">Clusters</th><th>%</th></tr>\n"

        # Loop over the cluster types.
        for typename in sorted(alltypes):

            ## The number of clusters of this type.
            numtype = 0

            for kl, ktype in ks.iteritems():
                if ktype == typename:
                    numtype += 1

            # Write the entry on the sorting homepage table.
            pg += "          <tr>"
            pg += "<td><a href=\"%s.html\">%s</a></td>" % (typename, typename)
            pg += "<td style=\"text-align:right\">%d</td>" % (numtype)
            pg += "<td>"

            if typename != "Edge":
                perc = 100.0 * (numtype) / (len(ks) - n_edge_klusters)
                for i in range(int(perc)):
                    pg += "|"
                pg += "</td>"
                pg += "<td style=\"text-align:right\">% 4.1f</td>" % (perc)
            else:
                pg += "<td></td><td></td>\n"
            pg += "</tr>\n"

            # Add to the results JSON.
            if typename == "Beta":
                print("* %f [%s] has % 10d betas" % (dp.get_value(), dp.get_unit(), numtype))
                beta_results[dp.get_value()] = numtype


        pg += "      </table>\n"
        pg += "    </p>\n"
        pg += "  </body>\n"
        pg += "</html>"


        ## The text file for the HTML page.
        f = open(homepage_name, "w")
        f.write(pg)
        f.close()

    # Write out the results JSON.
    with open(outputpath + "/beta_results.json", "w") as rjf:
        json.dump(beta_results, rjf)

    # Create the index page.

    ## The index page text.
    ipg = ""
    ipg += "<!DOCTYPE html>\n"
    ipg += "<html>\n"
    ipg += "  <head>\n"
    ipg += "    <title>Beta Attenuation: the datasets.</title>\n"
    ipg += "  </head>\n"
    ipg += "  <body>\n"
    ipg += "    <h1>CERN@school: Beta Attenuation Datasets</h1>\n"
    ipg += "    <ul>\n"

    for dp in data_points:
        ipg += "<li><a href='%s/index.html'>%s</a></li>\n" % (dp.get_name(), dp.get_name())

    ipg += "    </ul>\n"
    ipg += "  </body>\n"
    ipg += "</html>"

    index_page_name = (outputpath + "/index.html").replace("//", "/")

    ## The text file for the HTML page.
    f = open(index_page_name, "w")
    f.write(ipg)
    f.close()

    # Now you can view "index.html" to see your results!
    print("*")
    print("* Sorting complete.")
    print("* View your results by opening '%s' in a browser, e.g." % (index_page_name))
    print("* firefox %s &" % (index_page_name))
