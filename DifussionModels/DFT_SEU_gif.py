import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
plt.style.use("ggplot")

def DFTiteration(delta:float=0, z:float=0, s:float=0, c:float=0, s2:float=1,
             upper_limit:float=1, lower_limit:float=-1, h:float=0.001,
             t_max = 3, seed:int=None) -> list:

    P = [z] # Set the initial point to the bias.
    t = 0 # Init the time.
    if seed:
        np.random.seed(seed) # Set the seed if its given.

    while t<=t_max: # Init the simulation and break if reach to the limit of time of the session.

        deltaP = delta*h + np.random.normal(0, np.sqrt(h * s2)) # dP, rate of change of the Evidence.

        update = (1 - (s + c) * h) * P[-1] + deltaP # Update the Evidence

        P.append(update) # Store the process.

        t += h # Update the time.

        if (P[-1] >= upper_limit) or (P[-1] <= lower_limit): # Check if the process reach to any threshold of decision.
            P[-1] = upper_limit if P[-1] >= upper_limit else lower_limit # If does then set the last step to the threshold achieved and break the while loop.
            break

    return P

#seeds = [5072001, 1, 2, 4, 5]
trialddm = DFTiteration(seed = 10072001, delta=3, s=0.99)# for i in range(1)]
# xmax = max([len(i) for i in trialddm])
xmax = len(trialddm)

### Plot Empty and Set xlim, ylim, and Decision Bounderies.
fig = plt.figure(figsize=(15, 10))

l, = plt.plot([], [], 'k-')

plt.ylim(-1.1, 1.1)
plt.xlim(-20, xmax + int(xmax*0.01))

plt.ylabel(r"$P(n)$")
plt.xlabel("Tiempo (ms)")

plt.hlines(1, xmin=0, xmax=xmax, colors="green", label="Decidir A")
plt.hlines(-1, xmin=0, xmax=xmax, colors="red", label="Decidir B")

plt.title("")
plt.legend()

# Init Writer
writer = PillowWriter(fps=30, metadata={"artist":"Christian Badillo", "title":"dft simualtion"})

# Data
xlist = []
ylist = []

with writer.saving(fig, "/Users/christianbadillo/Desktop/Simulaciones_Aprendizaje_y_Conducta_Adaptativa/DifussionModels/img/linear_seu_s_low.gif", 72):
    for i in range(len(trialddm)):
            
        xlist.append(i)
        ylist.append(trialddm[i])
            
        l.set_data(xlist, ylist)

        writer.grab_frame()
