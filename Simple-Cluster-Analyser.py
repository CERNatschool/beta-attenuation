import os
import glob
import numpy as np
import pylab as pl
from matplotlib.colors import LogNorm

"""

CERN@school Simple Cluster Analyser

Authors:
* Tom Whyntie (Langton Star Centre/Queen Mary, Uni. of London);
* Azaria Coupe (Langton Star Centre/Uni. of Southampton).

Based on code provided to CERN@school by Steve Lloyd et al.
of the Queen Mary, University of London Particle Physics
Research Centre (PPRC).

To run this code on Windows, download and install a Python
runtime environment with NumPy and PyLab support
(e.g. Python(x,y) - see https://code.google.com/p/pythonxy/
(it's free!). Then open this script with IDLE, change the datapath
to where your data is stored and press F5 to run the code.

"""

# Change the datapath variable to wherever your data is stored
datapath = "./3.2mm"

#=============================================================================
class Hit: # Set of definitions representing one hit pixel
    """
    A class to describe "hit" pixels (i.e. with a count > 0).
    """

    def __init__ (self, i, j, val):
        """Gives hit at specific co-ordinates"""
        self.i = i                      # The hit pixel's i coordinate.
        self.j = j                      # The hit pixel's j coordinate.
        self.val = int(val)             # The hit pixel's recorded count (C).
        self.cluster = None             # The cluster the hit belongs to.

    def string(self):
        """ Returns a printable string from the hit information."""
        return 'i '+str(self.i)+' j '+str(self.j)+' val '+str(self.val)

    def isClustered(self):
        """ Has the hit been assigned to a cluster?"""
        if self.cluster != None:
            return True          # Hit has been clustered into a cluster
        else:
            return False         # Hit has been clustered into a cluster


#=============================================================================
class Cluster:
    """
    A class representing a cluster of >= 1 adjacent hits.
    """


    def __init__ (self):
        """ Initialises a cluster. """
        self.hits = []
        self.sum    = 0               # Sum of the values of hits
        self.num    = 0               # Number of hits
        self.xbar   = 0.0             # Geometric mean of the hit pixels' i.
        self.ybar   = 0.0             # Geometric mean of the hit pixels' j.
        self.radius = 0.0             # Cluster radius, as defined by the
        self.density = 0.0            # distance from the geometric mean to
                                      # to the most-distant hit.

    def add(self, hit):
        """ Adds hits to the cluster. """
        self.hits.append(hit)         # Adds the hit to the cluster's hits.
        self.sum += hit.val           # Sums the hit counts in the cluster.
        self.num = len(self.hits)     # Gives number of hits in cluster.
        hit.cluster = self            # Assigns the given hit to the cluster.

    def isNear(self, newHit):
        """ Decides if a new hit is in the cluster. """
        for hit in self.hits:

            # Checks whether the hit is adjacent to those in the cluster
            # (i,j directions).
            if abs(hit.i-newHit.i) <= 1 and abs(hit.j-newHit.j) <= 1:
                return True           # New Hit is in cluster
        
        return False                  # New Hit is not in cluster

    def analyse(self):
        """ Performs post-cluster finding analysis on the cluster. """
        xs = []; ys = []

        # Loop over the hits in the cluster.
        for h in self.hits:
            xs.append(h.i); ys.append(h.j)
        self.xbar = np.mean(xs)        # x and y co-ordinates of geometric
        self.ybar = np.mean(ys)        # centre
        rmax = 0.0
        for h in self.hits:
            r_x = h.i - self.xbar      # Distance from the centre to  
            r_y = h.j - self.ybar      # each pixel hit
        # Finds the radius of the cluster
            if (r_x*r_x + r_y*r_y) > rmax: rmax = r_x*r_x + r_y*r_y
        self.radius = np.sqrt(rmax)    
        # Finds the spatial density of the cluster
        if self.radius > 0.0:
            self.density = self.num/((self.radius)*(self.radius)) 
        else:
            self.density = 0.0


#=============================================================================

#-----------------------------------------------------------------------------
def get_hits(pathname): # Lists the number of hits in the file
    """
    Helper function to extract the pixel hits from a supplied data file
    (via the file's path).
    """

    f = open(pathname, 'r')      # Opens the data file for reading.
    data = f.read()              # Read in the data.
    f.close()                    # Close the data file.

    hits = []                    # Initialise the hits list.

    datarows = data.splitlines() # Separates lines of the data file.

    # Loop over the rows of data from the data file.
    for datarow in datarows:
        v = datarow.split('\t')  # Separates the I J C values
        I = int(v[0])
        J = int(v[1])
        C = int(v[2])
        hit = Hit(I, J, C)       # Gives integer hit co-ordinates and value
        hits.append(hit)

    return hits # Return the list of hits to whatever called the function.

#-----------------------------------------------------------------------------
def get_clusters(hits):
    """
    Constructs a list of clusters from adjacent hits in the supplied
    list of hits.
    """

    clusters = []  # Initialise the list of clusters.

    # Loop over hits making new clusters from any hits not yet clustered
    for hit in hits:
        if hit.isClustered():
            continue # Ignore hits that have been clustered already.

        cluster = Cluster()               # Create a new (empty) cluster.
        cluster.add(hit)                  # Add the (unclustered) hit.
        clusters.append(cluster)          # Add the new cluster to the list.

        # Now we loop over all of the other hits, looking for adjacent hits.
        # The loop only ends when we have run out of adjacent hits.
        #
        found = True                      # Initialise our loop test as true.
        while (found):                    # Loops until nothing more is found
            found = False
            for nhit in hits:             # Loops around all other hits to see
                                          # if they are clustered
                if nhit.isClustered():    # Hit already clustered, ignore it.
                    continue
                if cluster.isNear(nhit):  # Hit is in cluster! Woohoo!
                    cluster.add(nhit)     # Add to the cluster.
                    found = True          # Make sure we loop again.

    return clusters # Return the list of clusters to whatever called the function.
    print len(clusters)

#-------------------------------------------------------------------------------
#
#
#
#
if __name__ == "__main__": # Starts Program
    print "--------------------------------------"
    print " CERN@school: Simple Cluster Analysis "
    print "--------------------------------------"

    # Set up lists for the cluster properties we wish to plot.
    cluster_size   = []
    cluster_counts = []
    cluster_radius = []
    alpha_clusters=[]
    beta_clusters=[]
    gamma_clusters=[]
    cluster_density=[]
    tot_clusters=[]

    # Loop over the data files in the directory named in "datapath".
    # Data files must end in ".txt".
    for f in glob.glob(datapath + "/*.txt"):

        #
        # These are print statements added so that you can see what
        # each of the helper functions (get_hits, get_clusters) is doing.
        # You can comment them out if they start to get annoying.
        #

        print "For data file %s:" % (f)

        # Find the hits in the current data file.
        hits = get_hits(f)
        print "* Number of hits found:     %6d" % (len(hits))

        # Find the clusters in the data file from the hits
        clusters = get_clusters(hits)
        print "* Number of clusters found: %6d" % (len(clusters))

        # Finds the total number of clusters in the data set
        for i in range(0,len(clusters)):
            tot_clusters.append(i)
        

        # Loop over the clusters we've found
        for c in clusters:
            # Perform the cluster analysis
            c.analyse()
            # Plot the variables we're interested in
            cluster_size.append(len(c.hits))
            cluster_counts.append(c.sum)
            cluster_radius.append(c.radius)
            cluster_density.append(c.density)
            
            # Assigns a cluster to a particle type based on the
            # values of these variables
            
            if len(c.hits)>=1 and len(c.hits)<=4:
                if c.radius <= 0.71:
                    gamma_clusters.append(c)
                else:
                    beta_clusters.append(c)

            elif len(c.hits)<=6:
                if c.radius<=1.42:
                    alpha_clusters.append(c)
                elif c.radius>1.42:
                    beta_clusters.append(c)
                    
            elif len(c.hits)>6:
                if c.density>3.14:
                    alpha_clusters.append(c)
                elif c.density<3.14:
                    beta_clusters.append(c)

    # Gives the number of alpha, beta, gamma and total clusters in the data set
    # Alpha, beta and gamma should add up to the total!
    
    print len(alpha_clusters), len(beta_clusters), len(gamma_clusters), len(tot_clusters)

    # Finds the mean of each variable
    print("Mean counts = % 10.2f counts" % (np.mean(cluster_counts)))
    print("Mean hits = % 10.2f hits" % (np.mean(cluster_size)))
    print("Mean radius = % 10.2f pixels" % (np.mean(cluster_radius)))

    # Make the plots
    #----------------
    #
    # 1D plots
    # Hits per cluster
    fig = pl.figure(1)
    fig.set_facecolor('white')
    pl.xlabel('$N_h$')
    pl.ylabel('Number of clusters')
    pl.title('Hits Per Cluster Frequency Histogram')
    pl.grid(b=True)
    n, bins, patches = pl.hist(cluster_size, range(0,max(cluster_size),1))

    
    # Counts per cluster
    fig = pl.figure(2)
    fig.set_facecolor('white')
    pl.xlabel('Number of counts per cluster')
    pl.ylabel('Number of clusters')
    pl.title('Counts Per Cluster Frequency Histogram')
    pl.grid(b=True)
    n, bins, patches = pl.hist(cluster_counts,
                               range(0,max(cluster_counts)+100,50))

    
    # Cluster radius
    fig = pl.figure(3)
    fig.set_facecolor('white')
    pl.xlabel('Cluster radius [pixels]')
    pl.ylabel('Number of clusters')
    pl.title('Cluster Radius Frequency Histogram')
    pl.grid(b=True)
    n, bins, patches = pl.hist(cluster_radius, bins=100)


    # Show the plots!
    pl.show()


