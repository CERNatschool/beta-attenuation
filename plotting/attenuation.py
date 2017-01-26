#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

CERN@school: Analysis functions for the attenuation experiment.

See the README.md file for more information.

"""

#...for the logging.
import logging as lg

#...for the MATH.
import math

#...for even more MATH.
import numpy as np

#...for the least squares fitting.
from scipy import optimize

from scipy.optimize import curve_fit

# Import the plotting libraries.
import pylab as plt

#...for the colours. Oh, the colours!
from matplotlib.colors import LogNorm

# Load the LaTeX text plot libraries.
from matplotlib import rc

# Uncomment to use LaTeX for the plot text.
#rc('font',**{'family':'serif','serif':['Computer Modern']})
#rc('text', usetex=True)

#...for the chi^2 method.
from plotting.stats import chi2

def straight_line(x, m, c):
    return (x * m) + c #np.log(27003)


class DataPoint:

    def __init__(self, d_i, B_i, B_0):
        """ Constructor. """

        ## The thickness of the material.
        self.__d_i = float(d_i)

        ## The number of particles detected.
        self.__B_i = float(B_i)

        self.__ln_B_i = None

        if self.__B_i > 0.0:
            self.__ln_B_i = np.log(self.__B_i)

        ## The initial number of particles.
        self.__B_0 = float(B_0)

        ## The estimated attenuation coefficient from this data point.
        self.__mu_est = None

        ## The error on B_i (y) - binomial.
        self.__y_error = np.sqrt(self.__B_i * (1.0 - (self.__B_i/self.__B_0)))

        ## The upper y error.
        self.__y_error_upper = None

        ## The lower y error.
        self.__y_error_lower = None

        if self.__d_i > 0.0:
            mu = (1.0 / self.__d_i)
            mu *= np.log(self.__B_0 / self.__B_i)
            self.__mu_est = mu

        lg.info(" * d_i: %5.3f B_i: % 8d B_0: % 8d" % (self.__d_i, self.__B_i, self.__B_0))

    def __lt__(self, other):
        return self.get_thickness() < other.get_thickness()

    def get_thickness(self):
        return self.__d_i

    def get_count(self):
        return self.__B_i

    def get_predicted_count(self, mu, B_0):
        return B_0 * (np.exp(-mu * self.__d_i))

    def get_log_count(self):
        return self.__ln_B_i

    def get_predicted_log_count(self, mu, B_0):
        return np.log(B_0) - (mu*self.__d_i)

    def get_initial(self):
        return self.__B_0

    def get_success_rate(self):
        return self.__B_i / self.__B_0

    def get_estimated_attenuation_coefficient(self):
        return self.__mu_est

    def get_y_error(self):
        return self.__y_error

    def get_y_error_upper(self):
        return self.__y_error_upper

    def get_y_error_lower(self):
        return self.__y_error_lower

    def get_log_y_error_upper(self, mu, B_0):

        err = np.sqrt(self.__B_i * (1.0 - (self.__B_i/self.__B_0)))

        err_pc = 100.0 * err / float(self.__B_i)

        upper_bound = self.__B_i + err

        ln_upper_bound = np.log(upper_bound)

        lower_bound = self.__B_i - err

        ln_lower_bound = np.log(lower_bound)

        lg.info(" *")
        lg.info(" * Calculating error on (%f, %d):" % (self.__d_i, self.__B_i))
        lg.info(" *")
        lg.info(" *--> \sigma_{B_i}       = sqrt(B_i * (1 - B_i/B_0)) = %f (%f %%)" % (err, err_pc))
        lg.info(" *-->     { %f ---> %f" % (upper_bound, ln_upper_bound))
        lg.info(" *--> B_i = %f ---> %f" % (self.__B_i, np.log(self.__B_i)))
        lg.info(" *-->     { %f ---> %f" % (lower_bound, ln_lower_bound))
        lg.info(" *")

        return ln_upper_bound - np.log(self.__B_i)

    def get_log_y_error_lower(self, mu, B_0):

        err = np.sqrt(self.__B_i * (1.0 - (self.__B_i/self.__B_0)))

        err_pc = 100.0 * err / float(self.__B_i)

        upper_bound = self.__B_i + err

        ln_upper_bound = np.log(upper_bound)

        lower_bound = self.__B_i - err

        ln_lower_bound = np.log(lower_bound)

        lg.info(" *")
        lg.info(" * Calculating error on (%f, %d):" % (self.__d_i, self.__B_i))
        lg.info(" *")
        lg.info(" *--> \sigma_{B_i}       = sqrt(B_i * (1 - B_i/B_0)) = %f (%f %%)" % (err, err_pc))
        lg.info(" *-->     { %f ---> %f" % (upper_bound, ln_upper_bound))
        lg.info(" *--> B_i = %f ---> %f" % (self.__B_i, np.log(self.__B_i)))
        lg.info(" *-->     { %f ---> %f" % (lower_bound, ln_lower_bound))
        lg.info(" *")

        return np.log(self.__B_i) - ln_lower_bound

    def get_thickness_error(self):
        return 0.01 # [mm]


class DataPoints:
    """ A wrapper class for the data points in the attenuation experiment. """

    def __init__(self, data_points):

        ## A list of DataPoints.
        self.__dps = data_points

        # Calculate all of the properties of the data points.

        # Get the estimated attenuation coefficient and B_0 by fitting
        # ln(B_i) vs. d_i to a straight line.

        ## The estimate of the attenuation coefficient.
        self.__mu_est = None

        ## The estimated error on the attenuation coefficient (MLL).
        self.__mu_est_err_mll = None

        ## The estimate of the mean free path.
        self.__mfp_est = None

        ## The estimated error on the mean free path (MLL).
        self.__mfp_est_err_mll = None

        ## The estimated initial attempts (fit).
        self.__B_0_est = None

        # First, let's use the curve_fit function to fit the points
        # to a straight line.

        ## An array of the x values (thicknesses).
        self.__xs = np.array(self.get_thicknesses())

        ## An array of the y values (thicknesses).
        self.__ys = np.array(self.get_log_of_successes())

        ## A list of the estimated parameters, m and c.
        self.__parameter_estimates = None

        ## The covariance matrix of the parameter estimates.
        self.__covariance_matrix = None

        # Perform the fitting.
        self.__parameter_estimates, self.__covariance_matrix = curve_fit(straight_line, self.__xs, self.__ys)

        # Assign the estimate values and errors.
        self.__mu_est = -1.0 * self.__parameter_estimates[0]
        #
        self.__mfp_est = 1.0 / self.__mu_est
        #
        self.__B_0_est = np.exp(self.__parameter_estimates[1])

        # Now use the Maximum Log Likelihood method to estimate the error.

        # Loop over the data points

        sum_of_terms = 0.0

        lg.info(" *")
        lg.info(" * Looping over the data points:")
        lg.info(" *")
        for dp in sorted(self.__dps):
            lg.info(" * | d_i = % 5.2f [mm] | B_i = % 8d |" % (dp.get_thickness(), dp.get_count()))

            B_i_times_B_0 = dp.get_count() * self.__B_0_est

            B_0_minus_B_i = self.__B_0_est - dp.get_count()

            count_frac = float(B_i_times_B_0) / float(B_0_minus_B_i)

            d_i_squared = dp.get_thickness() * dp.get_thickness()

            d_i_squared_times_count_frac = d_i_squared * count_frac

            sum_of_terms += d_i_squared_times_count_frac

            lg.info(" * |-----------------------------------|")
            lg.info(" * | d_i^{2}   = %f" % (d_i_squared))
            lg.info(" * | |")
            lg.info(" * | | B_i * B_0 = %d" % (B_i_times_B_0))
            lg.info(" * | | B_0 - B_i = %d" % (B_0_minus_B_i))
            lg.info(" * | |-->Y/Z     = %f" % (count_frac))
            lg.info(" * | |")
            lg.info(" * | *-->X*Y/Z   = %f" % (d_i_squared_times_count_frac))
            lg.info(" * |")
        lg.info(" *")
        lg.info(" * Sum of terms = %f [mm^{2}] " % (sum_of_terms))
        lg.info(" *")
        #
        self.__mu_est_err_mll = 1.0/(np.sqrt(sum_of_terms))
        #
        self.__mu_est_err_mll_pc = 100.0 * (self.__mu_est_err_mll/self.__mu_est)
        #
        self.__mfp_est_err_mll = (1.0/(self.__mu_est * self.__mu_est)) * self.__mu_est_err_mll
        #
        self.__mfp_est_err_mll_pc = 100.0 * (self.__mfp_est_err_mll / self.__mfp_est)
        #
        lg.info(" * 1/sqrt(sum)  = %f [mm^{-1}]" % (self.__mu_est_err_mll))
        lg.info(" *")

        lg.info(" *")
        lg.info(" * from curve_fit:")
        lg.info(" *")
        lg.info(" *--> \mu (MLL)      = (% 10.5f \pm % 10.5f) [mm^{-1}] % 6.2f %%" % \
            (self.__mu_est, self.__mu_est_err_mll, self.__mu_est_err_mll_pc))
        lg.info(" *")
        lg.info(" *--> <x> = 1 / \mu  = (% 10.5f \pm % 10.5f) [mm]      % 6.2f %%" % \
            (self.__mfp_est, self.__mfp_est_err_mll, self.__mfp_est_err_mll_pc))
        lg.info(" *")
        lg.info(" *--> B_0            = % 10.2f particles" % (self.__B_0_est))
        lg.info(" *")

        # Calculate the Chi^2 values for the estimated distribution.
        #chi2_est, n_deg_est, chi2_div_est = chi2(self.get_successes(), self.get_predicted_successes(), 2)
        self.__chi_squared_value, self.__chi_squared_dof, chi2_div_est = \
            chi2(self.get_log_of_successes(), self.get_predicted_log_of_successes(), 2)

        lg.info(" * Estimated distribution (\hat{\mu}, \hat{B_{0}}):")
        lg.info(" *--> \Chi^2      = % 7.5f" % (self.__chi_squared_value))
        lg.info(" *--> N_freedom   = % d" % (self.__chi_squared_dof))
        lg.info(" *")

    def get_thicknesses(self):
        return [dp.get_thickness() for dp in self.__dps]

    def get_successes(self):
        return [dp.get_count() for dp in self.__dps]

    def get_predicted_successes(self):
        return [dp.get_predicted_count(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_log_of_successes(self):
        return [dp.get_log_count() for dp in self.__dps]

    def get_predicted_log_of_successes(self):
        return [dp.get_predicted_log_count(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_successes_upper_errors(self):
        return [dp.get_y_error_upper(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_log_of_successes_upper_errors(self):
        return [dp.get_log_y_error_upper(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_successes_lower_errors(self):
        return [dp.get_y_error_lower(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_log_of_successes_lower_errors(self):
        return [dp.get_log_y_error_lower(self.__mu_est, self.__B_0_est) for dp in self.__dps]

    def get_estimated_attenuation_coefficient(self):
        return self.__mu_est

    def get_error_on_the_estimated_attenuation_coefficient(self):
        """ Get the standard error on the est. attenuation coefficient. """
        # Maximum Log Likelihood method.
        return self.__mu_est_err_mll

    def get_estimated_mean_free_path(self):
        return self.__mfp_est

    def get_error_on_the_estimated_mean_free_path(self):
        return self.__mfp_est_err_mll

    def get_estimated_initial_count(self):
        return self.__B_0_est

    def get_log_of_the_estimated_initial_count(self):
        return np.log(self.__B_0_est)

    def get_chi_squared_fit_value(self):
        return self.__chi_squared_value

    def get_chi_squared_fit_dof(self):
        return self.__chi_squared_dof

    def write_html_table(self):

        ipg = ""
        ipg += "    <table>\n"
        #
        # The headings.
        ipg += "      <tr>"
        ipg += "<th colspan='3'>d<sub>i</sub> / mm</th>"
        ipg += "<th colspan='3'>B<sub>i</sub></th>"
        ipg += "</tr>\n"

        # Loop over the data points to get the table rows.
        for dp in self.__dps:
            ipg += "      <tr>"
            #
            # The thickness values.
            ipg += "<td style='font-family:Monospace'>% 4.2f</td>" % (dp.get_thickness())
            ipg += "<td>&pm;</td>"
            ipg += "<td style='font-family:Monospace'>% 4.2f</td>" % (dp.get_thickness_error())
            #
            # The counts.
            ipg += "<td style='text-align:right; font-family:Monospace;'>%d</a></td>" % (dp.get_count())
            ipg += "<td>&pm;</td>"
            ipg += "<td style='font-family:Monospace'>% 2d</td>" % (dp.get_y_error())
            ipg += "</tr>\n"

        ipg += "    </table>\n"

        return ipg

    def write_latex_table(self):
        ts = ""
        for dp in self.__dps:
            ts += "% 4.2f & % 6d & $\\pm$ & % 2d    \\\\\n" % \
                (dp.get_thickness(), \
                 dp.get_count()    , dp.get_y_error())
        return ts

class AttenuationPlot:
    """ Wrapper class for the attenuation plot. """

    #def __init__(self, dat, sim, **kwargs):
    def __init__(self, data_points, **kwargs):
        lg.info(" *")
        lg.info(" * Initialising AttenuationPlot object...")
        lg.info(" *")

        self.__dps = data_points

        # GETTING READY TO MAKE THE PLOTS
        #=================================

        # Reset the matplot lib plotting stuff.
        plt.close()

        # Here we create the figure on which we'll be plotting our results.
        # We assign the figure a number, a size (5" x 3"), set the resolution
        # of the image (150 DPI), and set the background and outline to white.

        ## The figure width [inches].
        self.__fig_w = 5.0
        #
        if "fig_width" in kwargs.keys():
            self.__fig_width = kwargs["fig_width"]

        ## The figure height [inches].
        self.__fig_h = 5.0
        #
        if "fig_height" in kwargs.keys():
            self.__fig_h = kwargs["fig_height"]

        ## The histogram.
        self.__plot = plt.figure(101, figsize=(self.__fig_w, self.__fig_h), dpi=150, facecolor='w', edgecolor='w')

        # Then we give a bit of clearance for the axes.
        self.__plot.subplots_adjust(bottom=0.17, left=0.15)

        # This is the subplot on which we'll actually be plotting.
        self.__plot_ax = self.__plot.add_subplot(111) # hpcplotax->self.__plot_ax

        # Label your axes:

        ## The x axis label.
        self.__x_label = "$x$"
        #
        if "x_label" in kwargs.keys():
            self.__x_label = kwargs["x_label"]
        #
        plt.xlabel(self.__x_label)

        ## The y axis label.
        self.__y_label = "$y$"
        #
        if "y_label" in kwargs.keys():
            self.__y_label = kwargs["y_label"]
        #
        plt.ylabel(self.__y_label)

        # Add gridlines.
        plt.grid(1)

        # Should be we use a logarithmic scale for the y axis?
        # Not yet, but we might do later.
        uselogy = False

        ## The x axis maximum.
        self.__x_max = 4.0
        #
        if "x_max" in kwargs.keys():
            self.__x_max = kwargs["x_max"]

        ## The x values for the fitted straight line plot.
        fitxs = np.arange(0.0, self.__x_max + 0.1, 0.1)

        ## The y values for the fitted straight line plot.
        fitys = (-1.0 * self.__dps.get_estimated_attenuation_coefficient() * fitxs) + self.__dps.get_log_of_the_estimated_initial_count()

        # Plot the line of best fit.
        plt.plot(fitxs, fitys, color='grey')

        # Plot the data.
        plt.errorbar(self.__dps.get_thicknesses(), \
                     self.__dps.get_log_of_successes(), \
                     linestyle="None", \
                     fmt='d', \
                     color='black', \
                     yerr=[self.__dps.get_log_of_successes_lower_errors(), self.__dps.get_log_of_successes_upper_errors()], \
                     ecolor='black', \
                     capthick=2, \
                     elinewidth=1 \
                     )

        lg.info(" *")

        # Set the x axis limits.
        plt.xlim([0, self.__x_max])

        # If supplied by the user, set the y axis limits.
        if "y_max" in kwargs.keys():
            plt.ylim([0.0, kwargs["y_max"]])

    def save_plot(self, outputpath, name):
        """ Saves the figure. """
        self.__plot.savefig(outputpath + "/%s.png" % (name))
        self.__plot.savefig(outputpath + "/%s.ps"  % (name))
