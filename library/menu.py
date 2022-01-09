import numpy as np
import math
from library.metadata import *
from random import choices
from library.portion import MENU_TYPES
from library.portion import GeneratePortionByMenuType

class SchoolWeekMenu:

    # Sequence is important: [ "MainDesert", "SoupMain", "SoupDesert" ]
    def __init__( self ):

        # Generates 5 portions for week: Monday, Tuesday, Wednesday, Thurstday, Friday
        self.portionTypeList = ["" for x in range(5)]
        self.portionList = []

        for day in range(5):
            self.portionTypeList[day] = np.random.choice( MENU_TYPES, p=MENU_TYPE_PROB )
            self.portionList.append( GeneratePortionByMenuType( self.portionTypeList[day] ) )
    
    def __str__(self):
        return  str( "Monday: " + self.portionTypeList[0] + \
                     "; Tuesday: " + self.portionTypeList[1] + \
                     "; Wednesday: " + self.portionTypeList[2] + \
                     "; Thurstday: " + self.portionTypeList[3] + \
                     "; Friday: " + self.portionTypeList[4] )

# Probabilities are based on project survey
def GenerateWeekMenu( ):
    return SchoolWeekMenu( )
