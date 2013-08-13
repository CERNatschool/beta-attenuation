
import numpy as np

from scipy.optimize import curve_fit 
from pylab import *  

import matplotlib.pyplot as plt

"""

CERN@school Potassium Beta Fitting - Exponential 

Authors:
* Tom Whyntie (Langton Star Centre/Queen Mary, Uni. of London);
* Azaria Coupe (Langton Star Centre/Uni. of Southampton).

To run this code on Windows, download and install a Python
runtime environment with NumPy and PyLab support
(e.g. Python(x,y) - see https://code.google.com/p/pythonxy/
(it's free!). Then open this script with IDLE, change the datapath
to where your data is stored and press F5 to run the code.

"""

# Defines the function that fits the data measured according to the paramters
# it finds
def general_fit(f, xdata, ydata, p0=None, sigma=None, **kw):
    """
    Pass all arguments to curve_fit, which uses non-linear least squares
    to fit a function, f, to data.  Calculate the uncertaities in the
    fit parameters from the covariance matrix.
    """
    # Finds the fit parameters
    popt, pcov = curve_fit(f, xdata, ydata, p0, sigma, **kw)

    # Calculates the chi squared value from the expected values and the
    # experimental values
    if sigma is None:
        chi2 = sum(((f(xdata,*popt)-ydata))**2)
    else:
        chi2 = sum(((f(xdata,*popt)-ydata)/sigma)**2)
    # Calculates the reduced chi squared value, if rchi2 is close to 1 then
    # the data fits the expected values well
    dof = len(ydata) - len(popt)
    rchi2 = chi2/dof
    print 'results of general_fit:'
    print '   chi squared = ', chi2
    print '   degrees of freedom = ', dof
    print '   reduced chi squared = ', rchi2

    # Calculates the uncertainties in the paramteres as the square roots
    # of the diagonal elements of the array 
    punc = zeros(len(popt))
    for i in arange(0,len(popt)):
        punc[i] = sqrt(pcov[i,i])
    return popt, punc, rchi2, dof

# Defines the general form of the fit that is expected, the parameters
# found will be the unknowns in this function
def expfunc(x, a, mu):
    """
    A simple (negative) exponential function with two parameters:
    * a : a scaling parameter;
    * mu: the decay constant.
    """
    return a * np.exp(-mu*x)



# These are the thicknesses of Aluminium in mm as measured in the experiment
x = np.array([
    0.00,
    0.24,
    0.36,
    0.59,
    0.87
    ])

# These are the number of beta particles observed at each thickness
y = np.array([
        195,
        135,
         90,
         66,
         28
        ])

# These are the uncertainties in the thickness measurements as found in the
# experiment
xerr = np.array([
        0.01,
        0.01,
        0.01,
        0.01,
        0.01
        ])

# The errors in the number of counts is just
# the square root of the number (Poissonian statistics).
yerr = np.sqrt(y)


# These are the results of your fit:
popt, punc, rchi2, dof = general_fit(expfunc, x, y, sigma=yerr)

# And this helps you plot the function produced by the fit.
linx = np.linspace(0.0,4.0,100)
yan2 = expfunc(linx, popt[0], popt[1])

# Print out the list of parameters popt generated by
# the general_fit function, so it will print [a, mu]
print(popt)


# Plot the fitted function
plt.plot(linx,yan2,'g-')

# Plot the data with the horizontal and vertical error bars
plt.errorbar(x,y,xerr=xerr,yerr=yerr,ls='none',elinewidth=1)

# Show the plots
plt.show()
