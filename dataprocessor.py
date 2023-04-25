
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:05:27 2023

@author: kayleepont
"""
# hier worden de gebruikte libraries geimporteerd. 
import csv
import matplotlib.pyplot as plt
import numpy as np

# [Tim] ik zou het stukje created on bla bla bla lekker weglaten. 
#       verder is het niet zozeer nodig om te benoemen waar wordt geimporteerd dat is wel duidelijk
#       in de bijna alle gevallen is het ook handig om geen code of comments boven je imports te plaatsen.
#       niet zozeer dat dat echt heel erg is maar dat is wel de algemene conventie om overzicht en structuur te behouden

#       de import van csv wordt niet gebruikt dus die kan je weghalen.

# deze lijn zorgt ervoor dat de data file wordt gelezen. 
file = 'posities_1_Team_A2.txt'
data = np.genfromtxt(file,delimiter='   ')

# [Tim] de naam file is niet helemaal correct hier
#       omdat je hier eigenlijk alleen het pad van de file opslaat 
#       de naam file_path zou hier beter passen


# deze twee regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
t = data[:,0]
x = data[:,1] 

# [Tim] t en x zou kunnen voor enkele waardes maar omdat je hier een lijsten aan waardes hebt
#       is een naam zoals t_values, x_values wat beter. 
#       als je deze waardes in een loop draait is het ook beter om deze x_value, t_value te noemen.
#       een loop zou er dan uit zien als:
#   	"for x_value in x_values" dit leest eigenlijk al als een zin en is dus veel leespaarder dan de namen x, t

# hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
v = [] 
for i in range(0,len(t)-1):
    dx= x[i+1]-x[i]
    dt= t[i+1]-t[i]
    afgeleide = dx/dt
    v.append(afgeleide) 

# [Tim] de naam i hier is opzich prima omdat het maar gaat over een klein stuk code.
#       echter is het verstandig om een naam aan te houden die wat beter omschrijft
#       wat i is een betere naam zou bijvoorbeeld 'data_point_index' kunnen zijn.
#       de code leest dan ook wat fijner. dan leest het namelijk als:
#       'for data_point_index in range(0,len(t)-1)'

#       verder kan je ook range(0,len(t)-1) een variabele maken voor je het in een loop doet
#       die kun je dan bijvoorbeeld 'data_point_indexes' noemen dan krijg je:
#       'for data_point_index in data_point_indexes'
#   	wat al helemaal fijn leest.

#       mijn eerdere punt over namen van lijsten en meervoud is ook van toepassing op v
#       de namen v_values, en v_value zou dan dus ook beter werken


# Deze lijnen zijn bijna iedentiek aan degene hierboven, behalve wordt v (snelheid) gedifferentieerd om a (versnelling) te krijgen. 
a = []

for i in range(0,len(t)-2):
    dv= v[i+1]-v[i]
    dt= t[i+1]-t[i]
    dubbeleafgeleide = dv/dt
    a.append(dubbeleafgeleide) 

# [Tim] mijn eerdere punten over i en lijstnaamgeving geld hier ook.

# deze lijn zorgt ervoor dat de tweede data file wordt gelezen. 
file_twee = 'posities_2_Team_A2.txt'
data_twee = np.genfromtxt(file_twee,delimiter='   ')

# deze twee regels geven een concrete definitie voor x en t wat het dus makkelijker maakt om versnellingsprofielen te maken. 
t_twee = data_twee[:,0]
x_twee = data_twee[:,1] 

# hier wordt er een lege lijst gemaakt voor v, vervolgens wordt x (positie) gedifferentieerd om v (snelheid) te krijgen. 
v_twee = [] 
for h in range(0,len(t)-1):
    dx_twee= x_twee[h+1]-x_twee[h]
    dt_twee= t_twee[h+1]-t_twee[h]
    afgeleide_twee = dx_twee/dt_twee
    v_twee.append(afgeleide_twee) 


# Deze lijnen zijn bijna iedentiek aan degene hierboven, behalve wordt v (snelheid) gedifferentieerd om a (versnelling) te krijgen. 
a_twee = [] 
for h in range(0,len(t)-2):
    dv_twee= v_twee[h+1]-v_twee[h]
    dt_twee= t_twee[h+1]-t_twee[h]
    dubbeleafgeleide_twee = dv_twee/dt_twee
    a_twee.append(dubbeleafgeleide_twee) 

# [Tim] voor de code die het tweede datafile ophaalt gelden alle comments over de eerste ook.
#       hierbij wil ik wel nog meegeven dat hier in plaats van i h gebruikt wordt.
#       dit kan toevoegen aan de onduidelijkheid van i gebruiken sinds je essentieel hetzelfde doet
#       maar het heeft opeens een andere naam.

#       verder is het mischien wat compacter om in plaats van a_twee de naam a_2 te gebruiken.
#       de informatie in beide namen is hetzelfde maar a_2 neemt wat minder ruimte in beslag
#       wat fijn kan zijn om te voorkomen dat je regels niet heel lang worden.

# het maken van een array voor beide versnellingsprofielen. de t staat zelf al wel in een array dus die hoefde niet veranderd te worden. 
a_array= np.array(a)
a_twee_array = np.array(a_twee)

# beide datasets hebben nu een versnellingsprofiel die in een array staan. Deze kunnen nu samen in een grafiek gezet worden. 
plt.plot(t[:-2],a_array, label= 'versnelling_dataset1' )
plt.plot(t[:-2],a_twee_array, label= 'versnelling_dataset2')
plt.xlabel('tijd[s]')
plt.ylabel('Versnelling[m/sˆ2]')
plt.title("Versnellingsprofielen van twee datasets")
plt.legend()
plt.show()

# [Tim] voor de rest is de code over het algemeen heel netjes complimenten!
#       ik weet dat ik nu veel aandachtspunten geef maar in het algemeen is het oprecht hele nette code
#       alle comments die ik nu geef zijn echt puntjes op de i dingen. die vooral handig zijn zodat iedereen
#       de code goed kan lezen onafhankelijk van voorkennis van deze code. 
#       Ook zodat jij de code in de toekomst direct en makkelijk kan begrijpen