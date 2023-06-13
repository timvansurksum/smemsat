import numpy as np
import matplotlib.pyplot as plt

# Gekregen parameters voor stap 1.
V_0                                     =  15 #V
DRIVE_VOLTAGE                           =  1.5 #V
CAPICATOR_OVERLAPPING_DISTANCE_DRIVE    =  200e-6 #meter
DISTANCE_BETWEEN_PLATES_DRIVE           =  2e-6 #meter
CAPICITOR_PLATE_THICKNESS               =  3e-6 #meter
CAPACITOR_PLATE_COUNT_DRIVE             =  100

# gevonden parameters
PERMMITIVITY_OF_FREE_SPACE              = 8.85e-12

# gekregen parameters voor stap 2.
MASS_OF_DRIVE       = 4.1e-9  #kilogram
SPRING_RATE_DRIVE         = 0.1619 #N/m
DAMPING_COEFICIENT  = 7.3603e-07 #kg/s

# Berekende parameters 
ANGULAR_VELOCITY_DRIVE    = np.sqrt(SPRING_RATE_DRIVE/MASS_OF_DRIVE-(DAMPING_COEFICIENT/(2*MASS_OF_DRIVE)))

# berekende componenten
v                    = lambda t: V_0 + DRIVE_VOLTAGE * np.cos ( ANGULAR_VELOCITY_DRIVE * t )
c_derivative         = lambda t: CAPICITOR_PLATE_THICKNESS/DISTANCE_BETWEEN_PLATES_DRIVE * PERMMITIVITY_OF_FREE_SPACE
F_electric           = lambda t: 1/2 * v(t)**2 * c_derivative(t) * CAPACITOR_PLATE_COUNT_DRIVE

# berekenen van transmissiecoefficient n2.
transfer_coefficient = F_electric(0.1)/v(0.1) # 

def process_data_drive (DAMPING_COEFICIENT, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric):
    Nstap    = 100000+1
    teind    = 0.5 
    dt       = teind/(Nstap -1)       
    t_values = np.linspace(0, teind, Nstap)

    # x en v berekeningen voor de differentiaal vergelijking.
    x0          = 0      # begin positie
    v0          = 0      # begin snelheid
    x_values    = np.zeros_like(t_values)
    x_values[0] = x0
    x_values[1] = x0 + v0 * dt
    
    # differentiaal vergelijking constantes.
    component_a = - (SPRING_RATE_DRIVE - 2 * MASS_OF_DRIVE / (dt**2)) / (MASS_OF_DRIVE /(dt**2)+ DAMPING_COEFICIENT/(2*dt))
    component_b = - ( MASS_OF_DRIVE /( dt ** 2) - DAMPING_COEFICIENT / ( 2 * dt)) / ( MASS_OF_DRIVE /( dt**2) + DAMPING_COEFICIENT /(2*dt))
    component_c = 1 / (MASS_OF_DRIVE/ (dt**2) + DAMPING_COEFICIENT / (2*dt))
    
    # numerieke oplossing van de differentiaal vergelijking.
    for time_index in range(1, Nstap - 1):
         x_values[time_index+1]  =  component_a * x_values[time_index] +  component_b * x_values[time_index-1] + component_c * F_electric(t_values[time_index]) 
                        
    # amplitude berekenen
    amplitude_x_drive   = np.max(x_values)
    
    return(amplitude_x_drive, x_values, t_values)

# oproepen van waardes uit functie
amplitude_x_drive, x_values, t_values = process_data_drive(DAMPING_COEFICIENT, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric)


# berekenen van snelheid vanuit x waardes. 
def compute_velocity (x_values,t_values):
    v_values = [] 
    for time_index in range(0,len(t_values)-1):
        dx= x_values[time_index +1]-x_values[time_index]
        dt= t_values[time_index +1]-t_values[time_index]
        afgeleide = dx/dt
        v_values.append(afgeleide) 
    v_values.append(v_values[-1])
    return(v_values)

# oproepen van waardes uit functie
v_values = compute_velocity(x_values, t_values)

# gekregen parameters voor stap 3.
ANGULAR_VELOCITY_SENSE = 10/60 #rad/sec


# F coriolis kracht berekenen. 
def compute_coriolis_force (MASS_OF_DRIVE, ANGULAR_VELOCITY_SENSE, v_values):
    F_coriolis  = []
    for time_index in range(0,len(t_values)-1):
        force = - 2 * MASS_OF_DRIVE * ANGULAR_VELOCITY_SENSE * v_values[time_index]
        F_coriolis.append(force)
    F_coriolis.append(F_coriolis[-1])
    print(force)
    return(F_coriolis)

F_coriolis  = compute_coriolis_force(MASS_OF_DRIVE, ANGULAR_VELOCITY_SENSE, v_values)

plt.plot(t_values,F_coriolis)
plt.show()

# Stap 4
MASS_OF_SENSE           = 4.92e-9 #kilogram
SPRING_RATE_SENSE       = 0.7769 #N/m
ANGULAR_VELOCITY_SENSE  = 1.237e-06 # kg/s


# Stap 5
l_sense     = 200e-6 #meter
d_sense     = 2e-6 #meter
w           = 3e-6 #meter
N_sense     = 40
Vdc         = 15 #V
