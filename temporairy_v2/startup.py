from DataProcessor import DataProcessor

# de file paden van de datafiles
file_1 = 'posities_1_Team_A2.txt'
file_2 = 'posities_2_Team_A2.txt'

# deze funcie laad de data van de data bestanden in met de hierboven gegeven paden
data_1 = DataProcessor.load_Data(file_1)
data_2 = DataProcessor.load_Data(file_2)

# deze regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
t_1 = data_1[:,0]
x_1 = data_1[:,1]

t_2 = data_2[:,0]
x_2 = data_2[:,1]

#deze functie leid de plaats informatie af en geeft snelheid
v_1, t_1 = DataProcessor.differentiate(x_1, t_1)
v_2, t_2 = DataProcessor.differentiate(x_2, t_2)


#deze functie leid de snelheids informatie af en geeft versnelling
a_1, t_1 = DataProcessor.differentiate(v_1, t_1)
a_2, t_2 = DataProcessor.differentiate(v_2, t_2)

#deze functie plot de data van beide bronnen
DataProcessor.plot_Data(t_1, a_1,a_2)