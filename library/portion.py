import numpy as np
from random import choices
from library.metadata import *

# This class is used for meal and meal waste
class Portion:

    def __init__(self, main, soup, solidDesert, liquidDesert, bread, freshPlants, milk ):
        self.main = main
        self.soup = soup
        self.solidDesert = solidDesert
        self.liquidDesert = liquidDesert
        self.bread = bread
        self.freshPlants = freshPlants
        self.milk = milk

    def __str__(self):
        return  "main: " + str(self.main) + \
            "; soup: " + str(self.soup) + \
            "; solidDesert: " + str(self.solidDesert) + \
            "; liquidDesert: " + str(self.liquidDesert) + \
            "; bread: " + str(self.bread) + \
            "; freshPlants: " + str(self.freshPlants) + \
            "; milk: " + str(self.milk)

    def __copy__(self):
        return Person( self.main, self.soup, self.solidDesert, self.liquidDesert, self.bread, self.freshPlants, self.milk )

    def getTotalWeight(self):
        return self.main + self.soup + self.solidDesert + self.liquidDesert + self.bread + self.freshPlants + self.milk

    def getWeightWithoutAdds(self):
        return self.main + self.soup + self.solidDesert + self.liquidDesert

    # adding two objects
    def __add__(self, second):
        sumPortion = Portion( 0, 0, 0, 0, 0, 0, 0 ) 
        sumPortion.main = self.main + second.main
        sumPortion.soup = self.soup + second.soup
        sumPortion.solidDesert = self.solidDesert + second.solidDesert
        sumPortion.liquidDesert = self.liquidDesert + second.liquidDesert
        sumPortion.bread = self.bread + second.bread
        sumPortion.freshPlants = self.freshPlants + second.freshPlants
        sumPortion.milk = self.milk + second.milk
        return sumPortion
    
    # substracting two objects
    def __sub__(self, second):
        subPortion = Portion( 0, 0, 0, 0, 0, 0, 0 ) 
        subPortion.main = self.main - second.main
        subPortion.soup = self.soup - second.soup
        subPortion.solidDesert = self.solidDesert - second.solidDesert
        subPortion.liquidDesert = self.liquidDesert - second.liquidDesert
        subPortion.bread = self.bread - second.bread
        subPortion.freshPlants = self.freshPlants - second.freshPlants
        subPortion.milk = self.milk - second.milk
        return subPortion

    # substracting two objects
    def __mul__(self, mult):
        mulPortion = Portion( 0, 0, 0, 0, 0, 0, 0 ) 
        mulPortion.main = self.main * mult
        mulPortion.soup = self.soup * mult
        mulPortion.solidDesert = self.solidDesert * mult
        mulPortion.liquidDesert = self.liquidDesert * mult
        mulPortion.bread = self.bread * mult
        mulPortion.freshPlants = self.freshPlants * mult
        mulPortion.milk = self.milk * mult
        return mulPortion

# Generates with equal probability
def GeneratePortion( ):

    # Generate menu type 
    portionType = np.random.choice( MENU_TYPES, p=MENU_TYPE_PROB )

    return GeneratePortionByMenuType( portionType )

# Generates with predefined probability
# Sequence is important: [ "MainDesert", "SoupMain", "SoupDesert" ]
def GeneratePortionWithProb( portionTypeProb ):

    # Generate menu type 
    portionType = np.random.choice( MENU_TYPES, p=portionTypeProb )

    return GeneratePortionByMenuType( portionType )

def GeneratePortionByMenuType( menu ):

    # Default
    main = 0
    soup = 0
    solidDesert = 0
    liquidDesert = 0
    bread = 0
    freshPlants = 0
    milk = 0

    # Generate main
    if( menu == "MainDesert" ):
        main = np.random.gumbel(225, 37.5)
    elif( menu == "SoupDesert" ):
        soup = np.random.normal(225, 37.5)
    else:
        main = np.random.normal( 200, 25 )
        soup = np.random.normal( 175, 12.5 )
        return Portion( main, soup, solidDesert, liquidDesert, bread, freshPlants, milk )
    
    # Generate desert
    desertType = np.random.choice( ["SolidDesert", "LiquidDesert", "BothDeserts"] )
    if( desertType == "SolidDesert" ):
        solidDesert = np.random.normal( 75, 12.5 )
    elif( desertType == "LiquidDesert" ):
        liquidDesert = np.random.normal( 200, 25 )
    else:
        solidDesert = np.random.normal( 32.5, 8.75 )
        liquidDesert = np.random.normal( 150, 25 )

    # Additional meal parts
    isBread = np.random.choice( [True, False] )
    if( isBread ):
        bread = np.random.exponential( 1.2 ) + 20
    isAdd = np.random.choice( ["Milk", "FreshPlants", "None"] )
    if( isAdd == "Milk" ):
        milk = 200
    elif( isAdd == "FreshPlants" ):
        freshPlants = np.random.normal( 75, 12.5 )

    return Portion( main, soup, solidDesert, liquidDesert, bread, freshPlants, milk )



