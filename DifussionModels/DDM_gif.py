import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

plt.style.use("ggplot")

def DDM_iter(drift_rate:float=1, bias:float=0, upper_limit:float=1, lower_limit:float=-1, 
        s2_normal:float=1, ds:float=0.001, t_max = 3, seed:int=None) -> list:
    
    s = [bias]
    t = 0
    if seed:
        np.random.seed(seed)

    while t<=t_max:
        
        deltaS = (drift_rate*ds) + (np.random.normal(0, s2_normal)*np.sqrt(ds))

        update = s[-1] + deltaS

        s.append(update)

        t+= ds

        if (s[-1] >= upper_limit) or (s[-1] <= lower_limit):
            break
    
    return s

#seeds = [5072001, 1, 2, 4, 5]
trialddm = DDM_iter(seed = 5072001)# for i in range(1)]
# xmax = max([len(i) for i in trialddm])
xmax = len(trialddm)

### Plot Empty and Set xlim, ylim, and Decision Bounderies.
fig = plt.figure(figsize=(15, 10))

l, = plt.plot([], [], 'k-', label = r"$S(t+1) = S(t) + \delta \cdot h + \frac{\epsilon(0, \sigma^2)}{\sqrt{h}}$")

plt.ylim(-1.1, 1.1)
plt.xlim(-20, xmax + int(xmax*0.01))

plt.ylabel(r"Evidencia Acumulada")
plt.xlabel("Tiempo (ms)")

plt.hlines(1, xmin=0, xmax=xmax, colors="green", label="Decidir A")
plt.hlines(-1, xmin=0, xmax=xmax, colors="red", label="Decidir B")

plt.title("Simulación del Modelo de Difusión de Ratcliff (1976)")
plt.legend()

# Init Writer
writer = PillowWriter(fps=30, metadata={"artist":"Christian Badillo", "title":"DDM simualtion"})

# Data
xlist = []
ylist = []

with writer.saving(fig, "DDM.gif", 72):
    for i in range(len(trialddm)):
            
        xlist.append(i)
        ylist.append(trialddm[i])
            
        l.set_data(xlist, ylist)

        writer.grab_frame()

    