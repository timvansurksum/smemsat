#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:05:27 2023

@author: kayleepont
"""
# hier worden de gebruikte libraries geimporteerd. 
import csv
import matplotlib.pyplot as plt
import numpy as np

# deze lijn zorgt ervoor dat de data file wordt gelezen. 
file = 'posities_1_Team_A2.txt'
data = np.genfromtxt(file,delimiter='   ')

# deze twee regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
t = data[:,0]
x = data[:,1] 

# hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
v = [] 
for i in range(0,len(t)-1):
    dx= x[i+1]-x[i]
    dt= t[i+1]-t[i]
    afgeleide = dx/dt
    v.append(afgeleide) 

# Deze lijnen zijn bijna iedentiek aan degene hierboven, behalve wordt v (snelheid) gedifferentieerd om a (versnelling) te krijgen. 
a = [] 
for i in range(0,len(t)-2):
    dv= v[i+1]-v[i]
    dt= t[i+1]-t[i]
    dubbeleafgeleide = dv/dt
    a.append(dubbeleafgeleide) 

# deze lijn zorgt ervoor dat de tweede data file wordt gelezen. 
file_twee = 'posities_2_Team_A2.txt'
data_twee = np.genfromtxt(file_twee,delimiter='   ')

# deze twee regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
t_twee = data_twee[:,0]
x_twee = data_twee[:,1] 

# hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
v_twee = [] 
for h in range(0,len(t)-1):
    dx_twee= x_twee[h+1]-x_twee[h]
    dt_twee= t_twee[h+1]-t_twee[h]
    afgeleide_twee = dx_twee/dt_twee
    v_twee.append(afgeleide_twee) 


# Deze lijnen zijn bijna iedentiek aan degene hierboven, behalve wordt v (snelheid) gedifferentieerd om a (versnelling) te krijgen. 
a_twee = [] 
for h in range(0,len(t)-2):
    dv_twee= v_twee[h+1]-v_twee[h]
    dt_twee= t_twee[h+1]-t_twee[h]
    dubbeleafgeleide_twee = dv_twee/dt_twee
    a_twee.append(dubbeleafgeleide_twee) 

# het maken van een array voor beide versnellingsprofielen. de t staat zelf al wel in een array dus die hoefde niet veranderd te worden. 
a_array= np.array(a)
a_twee_array = np.array(a_twee)

# beide datasets hebben nu een versnellingsprofiel die in een array staan. Deze kunnen nu samen in een grafiek gezet worden. 
plt.plot(t[:-2],a_array, label= 'versnelling_dataset1' )
plt.plot(t[:-2],a_twee_array, label= 'versnelling_dataset2')
plt.xlabel('tijd[s]')
plt.ylabel('Versnelling[m/sˆ2]')
plt.title("Versnellingsprofielen van twee datasets")
plt.legend()
plt.show()