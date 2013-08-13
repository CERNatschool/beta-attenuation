import pylab as p

"""

CERN@school Strontium Mean Cluster Property Plot

Authors:
* Tom Whyntie (Langton Star Centre/Queen Mary, Uni. of London);
* Azaria Coupe (Langton Star Centre/Uni. of Southampton).

To run this code on Windows, download and install a Python
runtime environment with NumPy and PyLab support
(e.g. Python(x,y) - see https://code.google.com/p/pythonxy/
(it's free!). Then open this script with IDLE, and press F5
to run the code.


"""

# Manual input arrays of the thickness of Aluminium (x) and
# the Mean Counts per Cluster (y), the Mean Hits per Cluster (z)
# and the Mean Cluster Radius (w)
x=[0.00,0.23,0.36,0.48,0.60,0.72,0.85,1.01,1.46,3.20]
y=[229.41,225.04,226.67,231.41,229.51,229.71,233.98,237.06,243.03,198.05]
z=[6.22,6.29,6.31,6.46,6.46,6.45,6.47,6.55,6.62,4.77]
w=[1.9,1.97,1.98,2.02,2.03,2.02,2.02,2.05,2.05,1.36]

# Makes the Mean Counts plot
fig = p.figure(1)
p.plot(x,y)
p.xlabel("Thickness(mm)")
p.ylabel("Mean Counts per Cluster")
p.title("Variation of Mean Counts with Thickness")

# Makes the Mean Hits Plot
fig = p.figure(2)
p.plot(x,z)
p.xlabel("Thickness (mm)")
p.ylabel("Mean Hits per Cluster")
p.title("Variation of Mean Hits with Thickness")

# Makes the Mean Radius Plot
fig = p.figure(3)
p.plot(x,w)
p.xlabel("Thickness (mm)")
p.ylabel("Mean Cluster Radius")
p.title("Variation of Mean Radius with Thickness")

# Shows the plot!
p.show()

