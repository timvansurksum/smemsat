#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:20:48 2023

@author: kaylee pont
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# gekregen parameters.
massa = 5.7e-9 # kg 
gamma = 1.69e-6 # kg/s
drive_frequentie = 4000 # Hz
f_coriolis_geschaald = 8e-12 # N s/rad
omega = 10/60 # rad/s    # hoeksnelheid?

# functie van veerconstante. 
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
        omega_values[ti] = omega
        
    # differentiaal vergelijking constantes.
    a = - (veerconstante - 2 * massa / (dt**2)) / (massa /(dt**2)+gamma/(2*dt))
    b = - ( massa /( dt ** 2) - gamma / ( 2 * dt)) / ( massa /( dt**2) + gamma /(2*dt))
    c = f_coriolis_geschaald / (massa/ (dt**2) + gamma / (2*dt))
    
    # numerieke oplossing van de differentiaal vergelijking.
    for ti in range(1, Nstap - 1):
        x_values[ti+1] = a * x_values[ti] + b * x_values[ti-1]+ c * omega_values[ti] * np.cos(drive_omega * t_values[ti])   
         
    # amplitude definieren van de sense oscillatie.
    amplitude_x_sense = np.max(x_values)
    
    # respons tijd berekenen door middel van maximale amplitude en t waardes. 
    elementen = np.where(x_values>= amplitude_x_sense - amplitude_x_sense/math.e)
    element = elementen[0][0]
    t0 = t_values[20000]
    t1 = t_values[element]
    respons_tijd = t1 - t0
    
    # statische uitwijking definieren.
    statische_uitwijking = f_coriolis_geschaald / veerconstante
    
    # Q-factor berekenen. 
    Q_factor = (amplitude_x_sense / statische_uitwijking) * teind
    
    return(amplitude_x_sense, Q_factor, respons_tijd, x_values, t_values, omega_values)

# bepalen van de uiterste waardes voor de gamma variatie. 
gamma_half   = gamma/2
gamma_twee   = gamma * 2
gamma_delta  = gamma_twee - gamma_half

# stap groottes bepalen voor de gamma en Q factor. 
Nstap_Q         = 17
gamma_values    = np.zeros(Nstap_Q)  
gamma_values[0] = gamma_half
stap_grootte    = gamma_delta / Nstap_Q

# vullen van gamma array met stapgrootte en gamma. 
for i in range(1, Nstap_Q):
    gamma_values[i] = gamma_half + i * stap_grootte

# lege arrays maken. 
amplitude_values        = np.zeros_like(gamma_values)
Q_factor_values         = np.zeros_like(gamma_values)
respons_tijd_values     = np.zeros_like(gamma_values)

# 
for i in range(0, Nstap_Q):
    amplitude_values[i], Q_factor_values[i], respons_tijd_values[i] = differentiaal_sense(gamma_values[i], veerconstante_fun(gamma_values[i]))[0:3]

x_values, t_values, omega_values = differentiaal_sense(gamma, veerconstante_fun(gamma))[3:]

plt.plot(t_values, omega_values)


