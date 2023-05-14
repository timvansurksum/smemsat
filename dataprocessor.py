import matplotlib.pyplot as plt
import numpy as np

class DataProcessor():
    def get_full_response_data(
        acceleratie_frame: list, 
        timestamps_frame: list, 
        response_bij_t_0: float, 
        response_bij_t_0_plus_dt: float, 
        dempingsfactor: float, 
        massa: float, 
        veerconstante: float
        ):
        """
        Get_full_response_data
        ----------
        Deze functie gebruikt de parameters van de accelerometer
        en het acceleratie profiel van het frame om numeriek
        de response van de massa te bepalen.

        Parameters
        ----------
        - acceleratie_frame : list, 
            de versnelling van het frame
        - timestamps_frame : list, 
            Tijdsmomenten van data.
        - dempingsfactor : float, 
            de dempingsfactor gamma is de denpingsfactor van het massaveersysteem.
        - response_bij_t_0 : float,
            de response op het startmoment van het versnellingsprofiel.
        - response_bij_t_0_plus_dt: float, 
            De response een tijdsmoment dt na de start van het versnellingsprofiel.
        - massa : float, 
            De de massa van de massa
        - veerconstante : float, 
            het collectieve veerconstante van alle veren in het massa veersysteem
        
        Returns
        ----------
        response_acceleration_data : list
            -   een reponse profiel op het gegeven acceleratie profiel in de vorm van een lijst.
        """
        
        input_data_indexes = range(1, len(acceleratie_frame))
        response_acceleration_data = [response_bij_t_0, response_bij_t_0_plus_dt]
        
        for input_data_index in input_data_indexes:
            response_at_t = DataProcessor.response_T_Plus_dt(
                dempingsfactor = dempingsfactor,
                massa = massa,
                veerconstante = veerconstante,
                acceleratie_frame_t = acceleratie_frame[input_data_index],
                response_t = response_acceleration_data[input_data_index],
                response_t_min_dt = response_acceleration_data[input_data_index - 1],
                dt = timestamps_frame[input_data_index] - timestamps_frame[input_data_index - 1]
                )
            response_acceleration_data.append(response_at_t)
        return response_acceleration_data
        
    def response_T_Plus_dt(
        dempingsfactor: float, 
        massa: float, 
        veerconstante: float, 
        acceleratie_frame_t: float, 
        response_t: float, 
        response_t_min_dt: float, 
        dt: float
        ):
        """
        Response_T_Plus_dt
        ----------
        Berekend de response in een gegeven punt
        
        Parameters
        ----------
        - dempingsfactor: float, 
            de dempingsfactor gamma is de denpingsfactor van het massaveersysteem.
        - massa: float, 
            De de massa van de massa
        - veerconstante: float, 
            het collectieve veerconstante van alle veren in het massa veersysteem
        - acceleratie_frame_t: float, 
            de versnelling van het frame op een gegeven tijd t
        - response_t: 
            float, de response of relatieve positie van de massa ten opzichten van het frame op een gegeven tijd t
        - response_t_min_dt: float, 
            de response of relatieve positie van de massa ten opzichten van het frame op een gegeven tijd t - h
        - dt: float, 
            Het verschil in tijdsmomenten.
            
        Returns
        ----------
        - response_t_plus_dt : float
            de response van een gegeven punt
        
        """
        response_t_plus_dt = (
                              response_t            * ( 2 - (dempingsfactor*dt/massa) - (dt**2)*veerconstante/massa )
                            - response_t_min_dt     * ( 1 - (dempingsfactor*dt/massa) ) 
                            + acceleratie_frame_t   * ( (dt**2) )
                            )
        return response_t_plus_dt

    def load_Data(filepath: str):
        """
        Load_Data
        ----------
        laad de databestanden in op basis van een gegeven pad
        
        Parameters
        ----------
        - filepath: str
            het pad van het bestand dat je wil inlezen
        
        Returns
        ----------
        - data: np.array
            de data van het bestand in de vorm van een numpy array
        """
        
        data = np.genfromtxt(filepath,delimiter='   ')
        return data

    def differentiatie(x: list, t: list):
        """
        Differentiatie
        --------------
        hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
        
        Parameters
        ----------
        - x: list
            functie waardes waar over wordt gediferentieerd
        - t: list
            
        """
        v = [] 
        for i in range(0,len(t)-1):
            dx= x[i+1]-x[i]
            dt= t[i+1]-t[i]
            afgeleide = dx/dt
            v.append(afgeleide)
        return v, t[:-1]
    
    def plot_2_graphs_with_2_different_scales(
        time_data: list, 
        plot_title: str, 
        x_axis_title: str, 
        dataset_1: list, 
        graph_1_title: str, 
        graph_1_y_label: str,
        dataset_2: list, 
        graph_2_title:str,
        graph_2_y_label: str,
        max_data_index: int 
        ):
        """
        plot_2_graphs_with_2_different_scales
        ---------
        plot 2 grafieken op basis van gegeven x data
        
        Parameters
        ----------
            - time_data: list, 
                x data van grafiek
            - plot_title: str, 
                titel van de plot
            - x_axis_title: str, 
                x as titel
            - dataset_1: list, 
                y data van eerste dataset
            - graph_1_title: str, 
                titel van eerste dataset
            - graph_1_y_label: str,
                y label of first graph
            - dataset_2: list, 
                y data van tweede dataset
            - graph_2_title:str
                titel van tweede dataset
            - graph_1_y_label: str,
                y label of first graph
            - max_data_index: int 
                maximale index van data
        """
        dataset_1_array= np.array(dataset_1)
        dataset_2_array = np.array(dataset_2)
        fig, axis_1 = plt.subplots()
        axis_1.plot(
            time_data[:max_data_index], 
            dataset_1_array[:max_data_index],
            label =  graph_1_title, 
            color = "green"
            )
        axis_2 = axis_1.twinx()
        axis_2.plot(
            time_data[:max_data_index], 
            dataset_2_array[:max_data_index], 
            label = graph_2_title, 
            color = "red"
            )
        axis_1.set_xlabel(x_axis_title)
        axis_1.set_ylabel(graph_1_y_label)
        axis_2.set_ylabel(graph_2_y_label)
        axis_1.set_title(plot_title)
        axis_1.legend(loc=2)
        axis_2.legend(loc=0)
        plt.show()
        
    def plot_Data_scalable(
        t: list, 
        plot_title: str, 
        x_axis_title: str, 
        y_axis_title: str, 
        datasets: list,
        max_data_index: int 
        ):
        """
        plot_Data_scalable
        ---------
        plot n grafieken op basis van gegeven data
        
        Parameters
        -----------
            - t: list,
                x data van grafiek
            - plot_title: str, 
                naam van plot
            - x_axis_title: str, 
                x as titel
            - y_axis_title: str, 
                y as titel
            - datasets: list,
                alle datasets met grafiek titels
            - max_data_index: int 
                maximale index van data
        """
        for dataset in datasets:
            plt.plot(t[:max_data_index],dataset["x_data"][:max_data_index], label=  dataset["title"])
        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)
        plt.title(plot_title)
        plt.legend()
        plt.show()