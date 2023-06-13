from dataprocessor import DataProcessor

# de file paden van de datafiles
datafile_frame_1_pad = "posities_1_Team_A2.txt"
datafile_frame_2_pad = "posities_2_Team_A2.txt"

# deze funcie laad de data van de data bestanden in met de hierboven gegeven paden
data_frame_1 = DataProcessor.load_Data(datafile_frame_1_pad)
data_frame_2 = DataProcessor.load_Data(datafile_frame_2_pad)

# deze regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken.
timestamps_data_1 = data_frame_1[:, 0]
positie_data_frame_1 = data_frame_1[:, 1]

timestamps_data_2 = data_frame_2[:, 0]
positie_data_frame_2 = data_frame_2[:, 1]

# deze functie leid de plaats informatie af en geeft snelheid
snelheid_data_frame_1, timestamps_data_1 = DataProcessor.differentiatie(
    positie_data_frame_1, timestamps_data_1)


snelheid_data_frame_2, timestamps_data_2 = DataProcessor.differentiatie(
    positie_data_frame_2, timestamps_data_2)

# deze functie leid de snelheids informatie af en geeft versnelling
acceleratie_data_frame_1, timestamps_data_1 = DataProcessor.differentiatie(
    snelheid_data_frame_1, timestamps_data_1)

acceleratie_data_frame_2, timestamps_data_2 = DataProcessor.differentiatie(
    snelheid_data_frame_2, timestamps_data_2)


response_bij_t_0 = 0
response_bij_t_0_plus_dt = 0    # in theorie is kan dit ook niet nul zijn
# maar gezien de stapgrootte heel klein is en beide datasets
# vrijwel beginnen bij 0 zal dit vrijwel geen invloed op het resultaat hebben

# gegeven parameters
massa = 1.476*10**-6
dempingsfactor = 0.034363
# dempingsfactor =  0.0137 # kritisch
veerconstante = 32
dt = 6*10**-7

# berekend voor de dataset de response in de accelerometer met de gegeven parameters

response_acceleration_data_1 = DataProcessor.get_full_response_data(
    acceleratie_frame=acceleratie_data_frame_1,
    timestamps_frame=timestamps_data_1,
    response_bij_t_0=response_bij_t_0,
    response_bij_t_0_plus_dt=response_bij_t_0_plus_dt,
    dempingsfactor=dempingsfactor,
    massa=massa,
    veerconstante=veerconstante
)

# voor een ideale accelerometer dt is hier niet exact
# sinds het wel veranderd bij verschillende tijdsmomenten al is die verandering zo goed als insignificant
veerconstante = dempingsfactor/dt

max_data_index = len(timestamps_data_1)

veerconstante = dempingsfactor/dt
# berekend voor de dataset de response in een ideale accelerometer
response_acceleration_data_1_met_ideale_accelerometer = DataProcessor.get_full_response_data(
    acceleratie_frame=acceleratie_data_frame_1,
    timestamps_frame=timestamps_data_1,
    response_bij_t_0=response_bij_t_0,
    response_bij_t_0_plus_dt=response_bij_t_0_plus_dt,
    dempingsfactor=dempingsfactor,
    massa=massa,
    veerconstante=veerconstante
)
datasets = [
    {
        "title": f"response_acceleration_data_1_met_ideale_accelerometer",
        "x_data": response_acceleration_data_1_met_ideale_accelerometer
    },
]
DataProcessor.plot_2_graphs_with_2_different_scales(
    time_data=timestamps_data_1,
    plot_title="frame acceleratie vs response dataset 1 met ideale accelerometer",
    x_axis_title="T[s]",
    dataset_1=response_acceleration_data_1,
    graph_1_title="response_acceleration_data_1",
    graph_1_y_label="x[m]",
    dataset_2=acceleratie_data_frame_1,
    graph_2_title="acceleratie_data_frame_1",
    graph_2_y_label="a[m*s^-2]",
    max_data_index=max_data_index
)

DataProcessor.plot_Data_scalable(
    timestamps_data_2,
    "response profiel van dataset 1",
    "tijd[s]",
    "afstand[m]",
    datasets,
    max_data_index
)

veerconstante = 32
dempingsfactoren = [0.001, 0.003, 0.007, 0.013, 0.034363, 0.05, 0.075, 0.01]
datasets = []
for dempingsfactor in dempingsfactoren:
	# berekend voor de dataset de response in de accelerometer met de gegeven parameters
	response_acceleration_data = DataProcessor.get_full_response_data(
		acceleratie_frame=acceleratie_data_frame_2,
		timestamps_frame=timestamps_data_2,
		response_bij_t_0=response_bij_t_0,
		response_bij_t_0_plus_dt=response_bij_t_0_plus_dt,
		dempingsfactor=dempingsfactor,
		massa=massa,
		veerconstante=veerconstante
	)
	datasets.append({
		"title": f"response_massa_dataset_2_dempingsfactor: {dempingsfactor}",
		"x_data": response_acceleration_data
	})

DataProcessor.plot_Data_scalable(
    timestamps_data_2,
    f"response profielen van dataset 2 met veerconstante van {veerconstante}",
    "tijd[s]",
    "afstand[m]",
    datasets,
    max_data_index
)

dempingsfactor = 0.0136
veerconstanten = [32, 100, 200, 500, 750, 1000]
datasets = []
for veerconstante in veerconstanten:
	# berekend voor de dataset de response in de accelerometer met de gegeven parameters
	response_acceleration_data = DataProcessor.get_full_response_data(
		acceleratie_frame=acceleratie_data_frame_2,
		timestamps_frame=timestamps_data_2,
		response_bij_t_0=response_bij_t_0,
		response_bij_t_0_plus_dt=response_bij_t_0_plus_dt,
		dempingsfactor=dempingsfactor,
		massa=massa,
		veerconstante=veerconstante
	)
	datasets.append({
		"title": f"response_massa_dataset_2_veerconstante: {veerconstante}",
		"x_data": response_acceleration_data
	})

DataProcessor.plot_Data_scalable(
    timestamps_data_2,
    f"response profielen van dataset 2 met dempingsfactor van {dempingsfactor}",
    "tijd[s]",
    "afstand[m]",
    datasets,
    max_data_index
)