from DataProcessor import DataProcessor

# de file paden van de datafiles
datafile_frame_1_pad = "posities_1_Team_A2.txt"
datafile_frame_2_pad = "posities_2_Team_A2.txt"

# deze funcie laad de data van de data bestanden in met de hierboven gegeven paden
data_frame_1 = DataProcessor.load_Data(datafile_frame_1_pad)
data_frame_2 = DataProcessor.load_Data(datafile_frame_2_pad)

# deze regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
timestamps_data_1 = data_frame_1[:,0]
positie_data_frame_1 = data_frame_1[:,1]

timestamps_data_2 = data_frame_2[:,0]
positie_data_frame_2 = data_frame_2[:,1]

#deze functie leid de plaats informatie af en geeft snelheid
snelheid_data_frame_1, timestamps_data_1 = DataProcessor.differentiatie(positie_data_frame_1, timestamps_data_1)
snelheid_data_frame_2, timestamps_data_2 = DataProcessor.differentiatie(positie_data_frame_2, timestamps_data_2)

#deze functie leid de snelheids informatie af en geeft versnelling
acceleratie_data_frame_1, timestamps_data_1 = DataProcessor.differentiatie(snelheid_data_frame_1, timestamps_data_1)
acceleratie_data_frame_2, timestamps_data_2 = DataProcessor.differentiatie(snelheid_data_frame_2, timestamps_data_2)


response_bij_t_0 = 0
response_bij_t_0_plus_dt = 0    # in theorie is kan dit ook niet nul zijn 
        	                # maar gezien de stapgrootte heel klein is en beide datasets 
                                # vrijwel beginnen bij 0 zal dit vrijwel geen invloed op het resultaat hebben

# gegeven parameters
massa = 1.476*10**-6
dempingsfactor =  0.034363 
dt = 6*10**-7

# voor een ideale accelerometer dt is hier niet exact 
# sinds het wel veranderd bij verschillende tijdsmomenten al is die verandering zo goed als insignificant
veerconstante = dempingsfactor/dt 

# berekend voor beide datasets de response in een ideale accelerometer
response_acceleration_data_1_met_ideale_accelerometer = DataProcessor.get_full_response_data(
        acceleratie_frame = acceleratie_data_frame_1, 
        timestamps_frame = timestamps_data_1, 
        response_bij_t_0 = response_bij_t_0, 
        response_bij_t_0_plus_dt = response_bij_t_0_plus_dt, 
        dempingsfactor = dempingsfactor, 
        massa = massa, 
        veerconstante = veerconstante
        ) 
response_acceleration_data_2_met_ideale_accelerometer = DataProcessor.get_full_response_data(
        acceleratie_frame = acceleratie_data_frame_2, 
        timestamps_frame = timestamps_data_2, 
        response_bij_t_0 = response_bij_t_0, 
        response_bij_t_0_plus_dt = response_bij_t_0_plus_dt, 
        dempingsfactor = dempingsfactor, 
        massa = massa, 
        veerconstante = veerconstante
        ) 

max_data_index = len(timestamps_data_1)

#deze functie plot de acceleratie data van het frame voor beide databestanden
DataProcessor.plot_Data(
    timestamps_data_1, 
    "Versnellingsprofielen van 2 datasets",
    "tijd[s]",
    "versnelling[m*s^-2]",
    acceleratie_data_frame_1[:max_data_index], "acceleration_frame_dataset_1", 
    acceleratie_data_frame_2[:max_data_index], "acceleration_frame_dataset_2", 
    )

#deze functie plot de response voor beide acceleratie profielen binnen een ideale accelerometer
DataProcessor.plot_Data(
    timestamps_data_1, 
    "ideale response van 2 datasets",
    "tijd[s]",
    "versnelling[m*s^-2]",
    response_acceleration_data_1_met_ideale_accelerometer[:max_data_index], "response_massa_dataset_1", 
    response_acceleration_data_2_met_ideale_accelerometer[:max_data_index], "response_massa_dataset_2", 
    )

# gegeven veerconstantes
veerconstante = 32

# berekend voor beide datasets de response in de accelerometer met de gegeven parameters
response_acceleration_data_1 = DataProcessor.get_full_response_data(
        acceleratie_frame = acceleratie_data_frame_1, 
        timestamps_frame = timestamps_data_1, 
        response_bij_t_0 = response_bij_t_0, 
        response_bij_t_0_plus_dt = response_bij_t_0_plus_dt, 
        dempingsfactor = dempingsfactor, 
        massa = massa, 
        veerconstante = veerconstante
        ) 
response_acceleration_data_2 = DataProcessor.get_full_response_data(
        acceleratie_frame = acceleratie_data_frame_2, 
        timestamps_frame = timestamps_data_2, 
        response_bij_t_0 = response_bij_t_0, 
        response_bij_t_0_plus_dt = response_bij_t_0_plus_dt, 
        dempingsfactor = dempingsfactor, 
        massa = massa, 
        veerconstante = veerconstante
        ) 

DataProcessor.plot_Data(
    timestamps_data_1, 
    "response profielen van 2 datasets",
    "tijd[s]",
    "afstand[m]",
    response_acceleration_data_1[:max_data_index], "response_massa_dataset_1", 
    response_acceleration_data_2[:max_data_index], "response_massa_dataset_2"
    )


dempingsfactoren =  [ 0.01, 0.05, 0.15, 0.1, 0.5, 1]
datasets = []
for dempingsfactor in dempingsfactoren:

        # berekend voor beide datasets de response in de accelerometer met de gegeven parameters
        response_acceleration_data_1 = DataProcessor.get_full_response_data(
                acceleratie_frame = acceleratie_data_frame_1, 
                timestamps_frame = timestamps_data_1, 
                response_bij_t_0 = response_bij_t_0, 
                response_bij_t_0_plus_dt = response_bij_t_0_plus_dt, 
                dempingsfactor = dempingsfactor, 
                massa = massa, 
                veerconstante = veerconstante
                ) 
        datasets.append({
                "title": f"response_massa_dataset_1_dempingsfactor: {dempingsfactor}",
                "x_data": [response_acceleration_data_1]
        })
DataProcessor.plot_Data_scalable(
    timestamps_data_1, 
    f"response profielen van 2 datasets",
    "tijd[s]",
    "afstand[m]",
    datasets,
    max_data_index
    )

