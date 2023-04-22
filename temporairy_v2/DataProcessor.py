# hier worden de gebruikte libraries geimporteerd. 
import csv
import matplotlib.pyplot as plt
import numpy as np

class DataProcessor():
    def load_Data(file):
        # deze lijn zorgt ervoor dat de data file wordt gelezen. 
        
        data = np.genfromtxt(file,delimiter='   ')
        return data

    def differentiate(x, t):
        # hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
        v = [] 
        for i in range(0,len(t)-1):
            dx= x[i+1]-x[i]
            dt= t[i+1]-t[i]
            afgeleide = dx/dt
            v.append(afgeleide)
        return v, t[:-1]
    
    @classmethod
    def plot_Data(self, t, a_1, a_2):
        # het maken van een array voor beide versnellingsprofielen. de t staat zelf al wel in een array dus die hoefde niet veranderd te worden. 
        a_array= np.array(a_1)
        a_twee_array = np.array(a_2)

        # beide datasets hebben nu een versnellingsprofiel die in een array staan. Deze kunnen nu samen in een grafiek gezet worden. 
        plt.plot(t,a_array, label= 'versnelling_dataset1' )
        plt.plot(t,a_twee_array, label= 'versnelling_dataset2')
        plt.xlabel('tijd[s]')
        plt.ylabel('Versnelling[m/sˆ2]')
        plt.title("Versnellingsprofielen van twee datasets")
        plt.legend()
        plt.show()