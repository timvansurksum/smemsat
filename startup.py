import numpy as np

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
F_electric           = lambda t: 1/2 * v(t)**2 * c_derivative(t) * CAPACITOR_PLATE_COUNT_DRIVE

# berekenen van transmissiecoefficient n1.
transfer_coefficient_step1 = F_electric(0.1)/v(0.1) 

def process_data_drive (DAMPING_COEFICIENT_DRIVE, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric):
    Nstap    = 100000000+1
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
         x_values_drive[time_index+1]  =  component_a * x_values_drive[time_index] +  component_b * x_values_drive[time_index-1] + component_c * F_electric(t_values[time_index]) 
                        
    # amplitude berekenen
    amplitude_x_drive  = np.max(x_values_drive)
    
    return(amplitude_x_drive, x_values_drive, t_values)

# oproepen van waardes uit functie
amplitude_x_drive, x_values_drive, t_values = process_data_drive(DAMPING_COEFICIENT_DRIVE, SPRING_RATE_DRIVE, MASS_OF_DRIVE, F_electric)


# berekenen van snelheid vanuit x waardes. 
def compute_velocity (x_values_drive,t_values):
    v_values_drive = [] 
    for time_index in range(0,len(t_values)-1):
        dx= x_values_drive[time_index +1]-x_values_drive[time_index]
        dt= t_values[time_index +1]-t_values[time_index]
        afgeleide = dx/dt
        v_values_drive.append(afgeleide) 
    v_values_drive.append(v_values_drive[-1])
    return(v_values_drive)

# oproepen van waardes uit functie
v_values_drive = compute_velocity(x_values_drive, t_values)

# berekenen van de transmissiecoefficient n2
transfer_coefficient_step2 = amplitude_x_drive/v_values_drive

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



# gekregen parameters stap 4
MASS_OF_SENSE           = 4.92e-9 #kilogram
SPRING_RATE_SENSE       = 0.7769 #N/m
DAMPING_COEFICIENT_SENSE  = 1.237e-06 # kg/s


def process_data_sense (DAMPING_COEFICIENT_SENSE, SPRING_RATE_SENSE, MASS_OF_SENSE, F_coriolis):
    Nstap    = 100000000+1
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

amplitude_x_sense, x_values_sense, t_values = process_data_sense(DAMPING_COEFICIENT_SENSE, SPRING_RATE_SENSE, MASS_OF_SENSE, F_coriolis)


# Stap 5
l_sense     = 200e-6 #meter
d_sense     = 2e-6 #meter
w           = 3e-6 #meter
N_sense     = 40
Vdc         = 15 #V
