import numpy as np
from dataprocessor import DataProcessor as DP
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
DAMPING_COEFICIENT_DRIVE  = 7.3603e-07 #kg/s

# Berekende parameters 
ANGULAR_VELOCITY_DRIVE    = np.sqrt(SPRING_RATE_DRIVE/MASS_OF_DRIVE-(DAMPING_COEFICIENT_DRIVE/(2*MASS_OF_DRIVE)))

# berekende componenten
v                    = lambda t: V_0 + DRIVE_VOLTAGE * np.cos ( ANGULAR_VELOCITY_DRIVE * t )
c_derivative         = lambda t: CAPICITOR_PLATE_THICKNESS/DISTANCE_BETWEEN_PLATES_DRIVE * PERMMITIVITY_OF_FREE_SPACE
F_electric           = lambda t: 1/2 * (V_0 + DRIVE_VOLTAGE * np.cos ( ANGULAR_VELOCITY_DRIVE * t ))**2 * (CAPICITOR_PLATE_THICKNESS/DISTANCE_BETWEEN_PLATES_DRIVE * PERMMITIVITY_OF_FREE_SPACE) * CAPACITOR_PLATE_COUNT_DRIVE

step_count    = 100000+1
end_time      = 0.5 

# maakt lijsten van spanning en F_electric
t_values            = np.linspace(0, end_time, step_count)
F_electric_values   = list(map(F_electric, t_values))
v_values            = list(map(v, t_values))

plt.figure(1)
plt.plot(t_values, F_electric_values, color='pink')
plt.title('F_electric over tijd')
plt.xlabel('tijd [sec]')
plt.ylabel('Elektrische kracht [Newton]')

# berekenen van transmissiecoefficient n1.
transfer_coefficient_step_1 = max(F_electric_values)/max(v_values)
print(f'transfer coeficient of f_electric to velocity {transfer_coefficient_step_1}')

def process_data_drive (DAMPING_COEFICIENT_DRIVE, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric_values):
    Nstap    = 100000+1
    teind    = 0.5 
    dt       = teind/(Nstap -1)       
    t_values = np.linspace(0, teind, Nstap)

    # x en v berekeningen voor de differentiaal vergelijking.
    x0                = 0      # begin positie
    v0                = 0      # begin snelheid
    x_values_drive    = np.zeros_like(t_values)
    x_values_drive[0] = x0
    x_values_drive[1] = x0 + v0 * dt
    
    # differentiaal vergelijking constantes.
    component_a = - (SPRING_RATE_DRIVE - 2 * MASS_OF_DRIVE / (dt**2)) / (MASS_OF_DRIVE /(dt**2)+ DAMPING_COEFICIENT_DRIVE/(2*dt))
    component_b = - ( MASS_OF_DRIVE /( dt ** 2) - DAMPING_COEFICIENT_DRIVE / ( 2 * dt)) / ( MASS_OF_DRIVE /( dt**2) + DAMPING_COEFICIENT_DRIVE /(2*dt))
    component_c = 1 / (MASS_OF_DRIVE/ (dt**2) + DAMPING_COEFICIENT_DRIVE / (2*dt))
    
    # numerieke oplossing van de differentiaal vergelijking.
    for time_index in range(1, Nstap - 1):
         x_values_drive[time_index+1]  =  component_a * x_values_drive[time_index] +  component_b * x_values_drive[time_index-1] + component_c * F_electric_values[time_index] 
                        
    # amplitude berekenen
    amplitude_x_drive  = np.max(x_values_drive)
    
    return(amplitude_x_drive, x_values_drive, t_values)

# oproepen van waardes uit functie
amplitude_x_drive, x_values_drive, t_values = process_data_drive(DAMPING_COEFICIENT_DRIVE, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric_values)

# berekenen van transmissiecoefficient n2.
transfer_coefficient_step_2 = max(v_values)/amplitude_x_drive
print(f'transfer coeficient of v to drive amplitude {transfer_coefficient_step_2}')

plt.figure(2)
plt.plot(t_values, x_values_drive, color='pink')
plt.title('x_values_drive over tijd')
plt.xlabel('tijd [seconden]')
plt.ylabel('Drive uitwijking [meter]')

# berekenen van snelheid vanuit x waardes. 
def compute_velocity (x_values_drive,t_values):
    v_values_drive  = [] 
    for time_index in range(0,len(t_values)-1):
        dx          = x_values_drive[time_index +1]-x_values_drive[time_index]
        dt          = t_values[time_index +1]-t_values[time_index]
        afgeleide   = dx/dt
        v_values_drive.append(afgeleide) 
    v_values_drive.append(v_values_drive[-1])
    return(v_values_drive)

# oproepen van waardes uit functie
v_values_drive = compute_velocity(x_values_drive, t_values)

# gekregen parameters voor stap 3.
ANGULAR_VELOCITY = 10/60 #rad/sec

# F coriolis kracht berekenen. 
def compute_coriolis_force (MASS_OF_DRIVE, ANGULAR_VELOCITY, v_values_drive):
    F_coriolis  = []
    for time_index in range(0,len(t_values)-1):
        force = - 2 * MASS_OF_DRIVE * ANGULAR_VELOCITY * v_values_drive[time_index]
        F_coriolis.append(force)
    F_coriolis.append(F_coriolis[-1])
    return(F_coriolis)

F_coriolis  = compute_coriolis_force(MASS_OF_DRIVE, ANGULAR_VELOCITY, v_values_drive)

# berekenen van transmissiecoefficient n3.
transfer_coefficient_step_3 = amplitude_x_drive/max(F_coriolis)
print(f'transfer coeficient of amplitude_x_drive to F_coriolis {transfer_coefficient_step_3}')

plt.figure(3)
plt.plot(t_values, F_coriolis, color='pink')
plt.title('F_coriolis over tijd')
plt.xlabel('tijd [seconden]')
plt.ylabel('Coriolis kracht [Newton]')

# gekregen parameters stap 4.
MASS_OF_SENSE             = 4.92e-9 #kilogram
SPRING_RATE_SENSE         = 0.7769 #N/m
DAMPING_COEFICIENT_SENSE  = 1.237e-06 # kg/s

# functie voor het berekenen van de sense uitwijking.
def process_data_sense (DAMPING_COEFICIENT_SENSE, SPRING_RATE_SENSE, MASS_OF_SENSE, F_coriolis):
    Nstap    = 100000+1
    teind    = 0.5 
    dt       = teind/(Nstap -1)       
    t_values = np.linspace(0, teind, Nstap)

    # x en v berekeningen voor de differentiaal vergelijking.
    x0                = 0      # begin positie
    v0                = 0      # begin snelheid
    x_values_sense    = np.zeros_like(t_values)
    x_values_sense[0] = x0
    x_values_sense[1] = x0 + v0 * dt
    
    # differentiaal vergelijking constantes.
    component_a = - (SPRING_RATE_SENSE - 2 * MASS_OF_SENSE / (dt**2)) / (MASS_OF_SENSE /(dt**2)+ DAMPING_COEFICIENT_SENSE/(2*dt))
    component_b = - ( MASS_OF_SENSE /( dt ** 2) - DAMPING_COEFICIENT_SENSE / ( 2 * dt)) / ( MASS_OF_SENSE /( dt**2) + DAMPING_COEFICIENT_SENSE /(2*dt))
    component_c = 1 / (MASS_OF_SENSE/ (dt**2) + DAMPING_COEFICIENT_SENSE / (2*dt))
    
    # numerieke oplossing van de differentiaal vergelijking.
    for time_index in range(1, Nstap - 1):
         x_values_sense[time_index+1]  =  component_a * x_values_sense[time_index] +  component_b * x_values_sense[time_index-1] + component_c * F_coriolis[time_index]
                        
    # amplitude berekenen
    amplitude_x_sense   = np.max(x_values_sense)
    
    return(amplitude_x_sense, x_values_sense, t_values)

# oproepen van waardes uit functie.
amplitude_x_sense, x_values_sense, t_values = process_data_sense(DAMPING_COEFICIENT_SENSE, SPRING_RATE_SENSE, MASS_OF_SENSE, F_coriolis)

# berekenen van transmissiecoefficient n4.
transfer_coefficient_step_4 = max(F_coriolis)/max(x_values_sense)
print(f'transfer coeficient of F_coriolis to x_values_sense {transfer_coefficient_step_4}')

plt.figure(4)
plt.plot(t_values, x_values_sense, color='pink')
plt.title('x_values_sense')
plt.title('x_values_sense over tijd')
plt.xlabel('tijd [seconden]')
plt.ylabel('Uitwijking Sense [meter]')

# Gekregen parameters stap 5.
L_SENSE                  = 200e-6 #meter
D_SENSE                  = 2e-6 #meter
W_SENSE                  = 3e-6 #meter
SENSE_CAPACITOR_COUNT    = 40
VDC                      = 15 #V

# vertaalt positie naar snelheid door te differentieren, 
# en maakt een lijst van berekende stroom sterktes: i_sense_values.
v_values_sense, t_values = DP.differentiatie(x_values_sense, t_values)
I_extra_factor           = SENSE_CAPACITOR_COUNT*PERMMITIVITY_OF_FREE_SPACE*W_SENSE/D_SENSE
i_sense                  = lambda t_index: I_extra_factor * v_values_sense[int(t_index)]
t_indexes                = range(0, len(t_values))
i_sense_values           = list(map(i_sense, t_indexes))

# berekenen van transmissiecoefficient n5.
transfer_coefficient_step_5 = max(x_values_sense)/max(i_sense_values)
print(f'transfer coeficient of x_sense_values to i_sense_values {transfer_coefficient_step_5}')
print(f'transfer coeficient of f_electric to i_sense_values or the whole system {transfer_coefficient_step_1*transfer_coefficient_step_2*transfer_coefficient_step_3*transfer_coefficient_step_4*transfer_coefficient_step_5}')

plt.figure(5)
plt.plot(t_values, i_sense_values, color='pink')
plt.title('i_sense_values over tijd')
plt.xlabel('tijd [seconden]')
plt.ylabel('Stroomsterkte [Ampere]')

plt.show()  