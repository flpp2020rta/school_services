# Version 1.1: improved language

# Simulator internal packages
from library.metadata import *
from library.person import *
from library.portion import *
from library.time import *
from library.menu import *
from library.school import *

# Python required packages
import numpy as np
import matplotlib.pyplot as plt
import math
import copy

# Streamlit packages
import streamlit as st


# Global parameters of simulator
NUMBER_OF_EXAMPLES = 10000

# Header
left_column, center_column, right_column = st.columns((1, 1, 2))
left_column.image('./img/projectLogo.jpg', use_column_width=True)
right_column.image('./img/rtaLogo.jpg', use_column_width=True)
st.title('Pasniegtā ēdiena atkritumu traukos prognozēšanas rīks skolām')

# Description
st.write('**Apraksts:** pielietojot šo simulācijas rīku, skolas vadība var noteikt vidējo pārtikas atkritumu daudzumu, ievadot skolas īpašības.')
st.write('**Ierobežojumi:**')
st.write('* rīks izmanto Rēzeknes skolu parametrus, kas tika iegūti aptaujas un atkrītumu mērīšanas laikā;')
st.write('* rīks balstās uz porciju izmēriem atbilstoši MK noteikumiem Nr. 172, versija 28/08/2020.')

# User input
st.write('**Skolas profils:**')
breakfastDuration = st.slider('Pārtraukuma ilgums (min.):', min_value=5, max_value=60, value=30, step=1)
pathTime = st.slider('Ceļā pavadītais laiks (min.):', min_value=0, max_value=20, value=6, step=1)
dislikeProbab = st.slider('Bērnu īpatsvars, kuriem nepatīk skolas ēdiens (%):', min_value=0, max_value=100, value=27, step=1)
externalFoodProbab = st.slider('Bērnu īpatsvars, kuri ēd konkurējošo ēdienu (%):', min_value=0, max_value=100, value=30, step=1)

# Data
resultsSnacksWaste = 0      # competitive food impact
resultsDislikeWaste = 0     # hated food
resultsTotalWaste = 0       # dislike + ignored (competitive food impact)
resultsTimeWaste = 0        # uneatten due to insufficient time
resultsWaste = 0            # insufficient time + hated food + competitive food impact

# Forecasting through simulation
breakfastDuration = breakfastDuration - pathTime
if breakfastDuration < 0:
    breakfastDuration = 0
dislikeProbab = dislikeProbab / 100.0
externalFoodProbab = externalFoodProbab / 100.0

# Launch button
button = st.button( 'Palaist' )

# Exception
if breakfastDuration < 1:
    st.error('Laikam ceļā jābūt mazākam par pārtraukuma ilgumu!')

if button and breakfastDuration > 0:

    # Reset progress bar
    progress_bar = st.progress(0)

    # Reset values
    resultsSnacksWaste = 0
    resultsDislikeWaste = 0
    resultsTotalWaste = 0
    resultsTimeWaste = 0
    resultsWaste = 0

    for k in range( NUMBER_OF_EXAMPLES ):
                        
        person = GeneratePerson( 0.5, dislikeProbab, externalFoodProbab )
        menu = GenerateWeekMenu()
        dislikeMenu = GenerateDislikeMenu( person, menu )
                        
        # Week analysis
        for x in range(5):

            time = breakfastDuration

            producedFood = menu.portionList[x].getTotalWeight()                 
            wastePortion = copy.deepcopy( dislikeMenu[x] )
                    
            if person.userOfExternalFood:
                                        
                eattenPart = GenerateEattenAfterSnacks()
                ignoredPortion = menu.portionList[x] * (1.0-eattenPart)
                        
                resultsSnacksWaste = resultsSnacksWaste + (ignoredPortion.getTotalWeight() / producedFood)
                    
                if ignoredPortion.main > dislikeMenu[x].main:
                    dislikeMenu[x].main = 0
                else:
                    dislikeMenu[x].main = dislikeMenu[x].main - ignoredPortion.main
                wastePortion.main = ignoredPortion.main + dislikeMenu[x].main
                            
                if ignoredPortion.soup > dislikeMenu[x].soup:
                    dislikeMenu[x].soup = 0
                else:
                    dislikeMenu[x].soup = dislikeMenu[x].soup - ignoredPortion.soup
                wastePortion.soup = ignoredPortion.soup + dislikeMenu[x].soup
                                                    
                if ignoredPortion.solidDesert > dislikeMenu[x].solidDesert:
                    dislikeMenu[x].solidDesert = 0
                else:
                    dislikeMenu[x].solidDesert = dislikeMenu[x].solidDesert - ignoredPortion.solidDesert
                wastePortion.solidDesert = ignoredPortion.solidDesert + dislikeMenu[x].solidDesert
                            
                if ignoredPortion.liquidDesert > dislikeMenu[x].liquidDesert:
                    dislikeMenu[x].liquidDesert = 0
                else:
                    dislikeMenu[x].liquidDesert = dislikeMenu[x].liquidDesert - ignoredPortion.liquidDesert
                wastePortion.liquidDesert = ignoredPortion.liquidDesert + dislikeMenu[x].liquidDesert
                        
                wastePortion.bread = ignoredPortion.bread
                wastePortion.freshPlants = ignoredPortion.freshPlants
                wastePortion.milk = ignoredPortion.milk
                                    
            resultsDislikeWaste = resultsDislikeWaste + (dislikeMenu[x].getTotalWeight() / producedFood)
            resultsTotalWaste = resultsTotalWaste + (wastePortion.getTotalWeight() / producedFood)
                    
            # Eatten part
            ePortion = menu.portionList[x] - wastePortion

            # Uneatten part        
            uwastePortion = person.CalculatePortionEatting( ePortion, time )
            resultsTimeWaste = resultsTimeWaste + uwastePortion.getTotalWeight() / producedFood

        progress_bar.progress( k / NUMBER_OF_EXAMPLES )
    progress_bar.progress( 1.0 )

    # Average value calculation        
    if resultsDislikeWaste != 0:
        resultsDislikeWaste = resultsDislikeWaste / ( 5.0 * NUMBER_OF_EXAMPLES )
    else:
        resultsDislikeWaste = 0
                
    if resultsSnacksWaste != 0:
        resultsSnacksWaste = resultsSnacksWaste / ( 5.0 * NUMBER_OF_EXAMPLES )
    else:
        resultsSnacksWaste = 0

    if resultsTimeWaste != 0:
        resultsTimeWaste = resultsTimeWaste / ( 5.0 * NUMBER_OF_EXAMPLES )
    else:
        resultsTimeWaste = 0

    if resultsTotalWaste != 0:
        resultsTotalWaste = resultsTotalWaste / ( 5.0 * NUMBER_OF_EXAMPLES )
    else:
        resultsTotalWaste = 0
                
    resultsWaste = resultsTotalWaste + resultsTimeWaste

# Percent calculation
resultsWaste = round(resultsWaste * 100.0, 2) 
resultsTimeWaste = round(resultsTimeWaste * 100.0, 2) 
resultsDislikeWaste = round(resultsDislikeWaste * 100.0, 2) 
resultsSnacksWaste = round(resultsSnacksWaste * 100.0, 2) 

# Output
st.write('**Prognoze:**')
st.write('**Kopējais atkritumu daudzums**: ' + str(resultsWaste) + '%')
st.write('**Atkritumi laika trūkuma dēļ**: ' + str(resultsTimeWaste) + '%')
st.write('**Atkritumi skolas ēdiena nepatikšanas dēļ**: ' + str(resultsDislikeWaste) + '%')
st.write('**Atkritumi konkurējoša ēdiena dēļ**: ' + str(resultsSnacksWaste) + '%')

# Footer
left_column, center_column, right_column = st.columns((1, 5, 1))
center_column.image('./img/grantLogo.png')