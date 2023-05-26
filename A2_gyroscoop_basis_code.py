#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:08:27 2023

@author: kayleepont
"""

import numpy as np
import matplotlib.pyplot as plt

# gekregen parameters.
k = 0.3820 # N/m
m = 4.3* 10**-9 # kg 
gamma = (8.1053* 10**-7) # kg/s
F_max = 60* 10**-9 # N
#voor grafieken 3 en 4 van opdracht 8 is de gamma keer 1.2 en keer 0.8 gedaan. 

# andere parameters die van toepassing zijn.
Nstap = 0.0001 
omega = np.sqrt(k / m)  # Eigenfrequentie
T = 2 * np.pi / omega  # Periode

# stapsgroote over tijd.
dt = 0.0001
# grotere simulatietijd gebruikt voor een beter zicht van de grafiek. 
t_values = np.arange(0, 100 * T, dt)  

# x en v berekeningen voor de differentiaal vergelijking.
x0 = 0.0 
v0 = 0.0 
x_values = np.zeros_like(t_values)
v_values = np.zeros_like(t_values)
x_values[0] = x0
v_values[0] = v0

# functie van de kracht en oscillatie.
def oscillatie_kracht(t_values):
    return F_max * np.cos( omega * t_values)

# functie voor de richtingscoefficient.
def richtingscoefficient(x_values, v_values, t_values):
    return (oscillatie_kracht(t_values) - gamma * v_values - k * x_values) / m

# numerieke oplossing van de differentiaal vergelijking.
for i in range(len(t_values) - 1):
    a_values = richtingscoefficient(x_values[i], v_values[i], t_values[i])
    v_values[i + 1] = v_values[i] + a_values * dt
    x_values[i + 1] = x_values[i] + v_values[i + 1] * dt + 0.5 * a_values * dt ** 2

# plot van de drive grafiek.
plt.plot(t_values, x_values, color='blue')
plt.xlabel('tijd [seconden]')
plt.ylabel('uitwijking [meter]')
plt.title('simulatie uitwijking van massa bij F_max')
plt.show()

# Berekenen van de tuning-kromme.
frequency_values = np.linspace(0.9 * omega / (2 * np.pi), 1.1 * omega / (2 * np.pi), 1000)
amplitude_values = np.zeros_like(frequency_values)

for i, frequency in enumerate(frequency_values):
    omega_new = (2 * np.pi) * frequency
    x_value_new =  F_max / np.sqrt((k - m * omega_new ** 2) ** 2 + (gamma * omega_new) ** 2)
    amplitude_values[i] = x_value_new

# de frequentiewaarden van amplitudes die gelijk zijn aan of groter dan de helft van de maximale amplitude. 
half_max_amplitude = np.max(amplitude_values) / 2.0
indices = np.where(amplitude_values >= half_max_amplitude)[0]
frequency_half_max = frequency_values[indices]
left_frequency = frequency_half_max[0]
right_frequency = frequency_half_max[-1]

# Berekenen van de FWHM.
full_width_half_max = right_frequency- left_frequency

# Plot van de tuning-kromme en wat labels, kleur veranderingen. 
plt.plot(frequency_values, amplitude_values, label='Tuning-kromme', color='blue')
plt.axhline( y=half_max_amplitude, color='r', linestyle='--', label='Half maximum')
plt.fill_between(frequency_values, 0, amplitude_values, where=(frequency_values >= left_frequency) & (frequency_values <= right_frequency), facecolor='green', alpha=0.3)
plt.xlabel('Frequentie [Hertz]')
plt.ylabel('Trillingsamplitude [meter]')
plt.title('Tuning-kromme van de oscillator')
plt.xlim(1350, 1650)  
annotation_color = (0.5, 0.8, 0.5)  
plt.annotate(f'FWHM = {full_width_half_max:.4f} Hz', xy=(0.95, 0.95), xycoords='axes fraction', fontsize=10, ha='right', va='top',
             bbox=dict(facecolor=annotation_color, edgecolor='green', boxstyle='round,pad=0.4'))
plt.show()



