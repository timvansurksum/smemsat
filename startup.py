import numpy as np


# stap 1
V_0 =  15 #V
DRIVE_VOLTAGE = 1.5 #V
CAPICATOR_OVERLAPPING_DISTANCE_DRIVE =  200e-6 #meter
DISTANCE_BETWEEN_PLATES_DRIVE =  2e-6 #meter
CAPICITOR_PLATE_THICKNESS =  3e-6 #meter
CAPACITOR_PLATE_COUNT_DRIVE =  100
PERMMITIVITY_OF_FREE_SPACE = 8.85 * 10**-12

# Stap 2
MASS_OF_DRIVE = 4.1e-9  #kilogram
SPRING_RATE = 0.1619 #N/m
DAMPING_COEFICIENT = 7.3603e-07 #kg/s
ANGULAR_VELOCITY = np.sqrt(SPRING_RATE/MASS_OF_DRIVE-(DAMPING_COEFICIENT/(2*MASS_OF_DRIVE)))


v = lambda t: V_0 * DRIVE_VOLTAGE * np.cos(ANGULAR_VELOCITY * t)
c_derivative = lambda t: CAPICITOR_PLATE_THICKNESS/DISTANCE_BETWEEN_PLATES_DRIVE*PERMMITIVITY_OF_FREE_SPACE

F_electric = lambda t: 1/2 * v(t)**2*c_derivative(t)

print(F_electric(5))
# Stap 3
Omega = 10 #rad/min

# Stap 4
m_sense = 4.92e-9 #kilogram
k_sense = 0.7769 #N/m
gamma_sense = 1.237e-06 # kg/s

# Stap 5
l_sense = 200e-6 #meter
d_sense = 2e-6 #meter
w = 3e-6 #meter
N_sense = 40
Vdc = 15 #V
