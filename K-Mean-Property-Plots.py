import pylab as p
import numpy as n

"""

CERN@school Potassium Mean Counts Plot

Authors:
* Tom Whyntie (Langton Star Centre/Queen Mary, Uni. of London);
* Azaria Coupe (Langton Star Centre/Uni. of Southampton).

To run this code on Windows, download and install a Python
runtime environment with NumPy and PyLab support
(e.g. Python(x,y) - see https://code.google.com/p/pythonxy/
(it's free!). Then open this script with IDLE, and press F5
to run the code.


"""

# Manual input arrays of Al thickness (x), Mean Counts per Cluster (y),
# Mean Hits per Cluster, and Mean Cluster Radius
x=[0.0,0.24,0.36,0.59,0.87]
y=[252.60,265.13,253.20,213.88,207.08]
z=[8.03,8.36,8.47,7.27,6.90]
w=[2.22,2.20,2.42,2.13,1.86]


# Makes the Mean Counts Plot
fig = p.figure(1)
p.plot(x,y)
p.xlabel("Thickness (mm)")
p.ylabel("Mean Counts per Cluster")
p.title("Variation of Mean Cluster Counts with Thickness")

# Makes the Mean Hits Plot
fig = p.figure(2)
p.plot(x,z)
p.xlabel("Thickness (mm)")
p.ylabel("Mean Hits per Cluster")
p.title("Mean Hits per Cluster vs Thickness")

# Makes the Mean Radius Plot
fig = p.figure(3)
p.plot(x,w)
p.xlabel("Thickness (mm)")
p.ylabel("Mean Cluster Radius")
p.title("Mean Cluster Radius vs Thickness")


# Shows the plots
p.show()
