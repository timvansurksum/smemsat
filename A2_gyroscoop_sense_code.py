#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:20:48 2023

@author: kaylee pont
"""

import numpy as np
import matplotlib.pyplot as plt

# gekregen parameters.
massa = 5.7e-9 # kg 
gamma = 1.69e-6 # kg/s
drive_frequentie = 4000 # Hz
f_coriolis_geschaald = 8e-12 # N s/rad
omega = 10/60 # rad/s    # hoeksnelheid?

# berekende parameters. 
def veerconstante_fun (gamma): 
    veerconstante = massa * (( 2 * np.pi * drive_frequentie)**2 + (gamma)**2/(4*massa)** 2 ) # N/m
    return veerconstante
drive_omega = drive_frequentie * (2 *np.pi) # rad/s       # de rotatiesnelheid
Periode = 2 * np.pi / drive_frequentie # ?        

def differentiaal_sense (gamma, veerconstante): 
    # stapsgroote over tijd.
    Nstap = 100000+1
    teind = 0.5 
    dt = teind/(Nstap -1)       # de stap grootte
    t_values = np.linspace(0, teind, Nstap)

    # x en v berekeningen voor de differentiaal vergelijking.
    x0 = 0      # begin positie
    v0 = 0      # begin snelheid
    x_values = np.zeros_like(t_values)
    x_values[0] = x0
    x_values[1] = x0 + v0 * dt
    
    # omega array
    omega_values = np.zeros_like(t_values)
    for ti in range(20000,80000):
        omega_values[ti] = 1
        
    # differentiaal vergelijking constantes
    a = -(veerconstante - 2 * massa / (dt**2)) / (massa /(dt**2)+gamma/(2*dt))
    b = -( massa /( dt ** 2) - gamma / ( 2 * dt)) / ( massa /( dt**2) + gamma /(2*dt))
    c = f_coriolis_geschaald / (massa/ (dt**2) + gamma / (2*dt))
    #F_coriolis = f_coriolis_geschaald * omega * np.cos(drive_omega * t_values)    # berekenen van de coriolis kracht
    
    # numerieke oplossing van de differentiaal vergelijking.
    for ti in range(1, Nstap - 1):
        x_values[ti+1] = a * x_values[ti] + b * x_values[ti-1]+ c * omega_values[ti] * np.cos(drive_omega * t_values[ti])   
         
    # amplitude bepalen van de sense oscillatie.
    amplitude_x_sense = np.max(x_values)
    
    # respons tijd berekenen door middel van maximale amplitude en t waardes. 
    elementen = np.where(x_values>= amplitude_x_sense - amplitude_x_sense/np.exp())
    element = elementen[0][0]
    t0 = t_values[20000]
    t1 = t_values[element]
    respons_tijd = t1 - t0
    
    # statische uitwijking definieren. 
    statische_uitwijking = f_coriolis_geschaald / veerconstante
    
    # Q-factor berekenen. 
    Q_factor = (amplitude_x_sense / statische_uitwijking) * teind
    
    return(amplitude_x_sense, x_values, t_values, )


# grafiek voor de responstijd berekenen. 
figuur_2 = plt.figure()
plt.plot(t_values, x_values_respons)
plt.xlabel('tijd [seconden]')
plt.ylabel('uitwijking [meter]')
plt.title('Respons tijd van de sense')
plt.show()


# gamma verandering 2 keer zo groot
gamma_twee = gamma * 2
veerconstante_gamma_twee = massa * (( 2 * np.pi * drive_frequentie)**2 + (gamma_twee)**2/(4*massa)** 2 ) # N/m

# x en v waardes voor gamma * 2
x_respons0 = 0      # begin positie
v_respons0 = 0      # begin snelheid
x_values_gamma_twee = np.zeros_like(t_values)
x_values_gamma_twee[0] = x0
x_values_gamma_twee[1] = x0 + v0 * dt

# differentiaal vergelijking constantes bij gamma * 2
a_twee = -(veerconstante_gamma_twee - 2 * massa / (dt**2)) / (massa /(dt**2)+gamma_twee/(2*dt))
b_twee = -( massa /( dt ** 2) - gamma_twee / ( 2 * dt)) / ( massa /( dt**2) + gamma_twee /(2*dt))
c_twee = 1 / (massa/ (dt**2) + gamma_twee / (2*dt))
F_coriolis = f_coriolis_geschaald * omega * np.cos(drive_omega * t_values)    # berekenen van de coriolis kracht

# numerieke oplossing van de differentiaal vergelijking met gamma * 2
for ti in range(1, Nstap - 1):
    x_values_gamma_twee[ti+1] = a_twee * x_values_gamma_twee[ti] + b_twee * x_values_gamma_twee[ti-1]+ c_twee * F_coriolis[ti] 

# maximale amplitude van de veranderde gamma en sense grafiek (2).
amplitude_gamma_twee  = np.max(x_values_gamma_twee)

# Q factor berekenen.
Q_factor_gamma_twee = amplitude_gamma_twee / statische_uitwijking * teind

# gamma variatie 2 keer zo klein
gamma_half = gamma * (1/2)
veerconstante_gamma_half = massa * (( 2 * np.pi * drive_frequentie)**2 + (gamma_half)**2/(4*massa)** 2 ) # N/m

# x en v waardes voor gamma * 0.5
x_respons0 = 0      # begin positie
v_respons0 = 0      # begin snelheid
x_values_gamma_half = np.zeros_like(t_values)
x_values_gamma_half[0] = x0
x_values_gamma_half[1] = x0 + v0 * dt

# differentiaal vergelijking constantes bij gamma * 0.5
a_half = -(veerconstante_gamma_half - 2 * massa / (dt**2)) / (massa /(dt**2)+gamma_half/(2*dt))
b_half = -( massa /( dt ** 2) - gamma_half / ( 2 * dt)) / ( massa /( dt**2) + gamma_half /(2*dt))
c_half = 1 / (massa/ (dt**2) + gamma_half / (2*dt))
F_coriolis = f_coriolis_geschaald * omega * np.cos(drive_omega * t_values)    # berekenen van de coriolis kracht

# numerieke oplossing van de differentiaal vergelijking bij gamma * 0.5
for ti in range(1, Nstap - 1):
    x_values_gamma_half[ti+1] = a_half * x_values_gamma_half[ti] + b_half * x_values_gamma_half[ti-1]+ c_half * F_coriolis[ti] 

# maximale amplitude van de veranderde gamma en sense grafiek (0.5).
amplitude_gamma_half  = np.max(x_values_gamma_half)

# Q factor berekenen.
Q_factor_gamma_half = amplitude_gamma_half / statische_uitwijking * teind

# plot van de sense grafieken gecombineerd met de gevarieerde gammas.
figuur_3 = plt.figure()
plt.plot(t_values, x_values)
plt.xlabel('tijd [seconden]')
plt.ylabel('uitwijking [meter]')
plt.title('simulatie uitwijking van massa bij F_coriolis')
plt.show()

# gamma tegenover Q factor



# vinden van waarde gamma waar in deze klant moet zitten voor hun eisen.(kritische demping)

