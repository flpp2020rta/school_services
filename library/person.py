import numpy as np
import math
from library.metadata import *
from library.portion import Portion
from library.time import GenerateTalkingTime
from random import choices

class Person:

    def __init__( self, sex, studyYear, soupEattingSpeed, solidMealEattingSpeed, sweetMult, likeSchoolKitchen, userOfExternalFood, solidDesertIsTakenToClass ):
        self.sex = sex
        self.studyYear = studyYear
        self.soupEattingSpeed = soupEattingSpeed
        self.solidMealEattingSpeed = solidMealEattingSpeed
        self.sweetMult = sweetMult
        self.likeSchoolKitchen = likeSchoolKitchen
        self.userOfExternalFood = userOfExternalFood
        self.solidDesertIsTakenToClass = solidDesertIsTakenToClass
    
    def CalculateRequiredTime( self, portion ):

        # Calculate time per each portion component (in minutes)
        mainTime = portion.main / self.solidMealEattingSpeed
        if mainTime < 0:
            mainTime = 0

        soupTime = portion.soup / self.soupEattingSpeed
        if soupTime < 0:
            soupTime = 0

        solidDesertTime = 0
        if not (self.solidDesertIsTakenToClass):
            solidDesertTime = portion.solidDesert / (self.solidMealEattingSpeed * self.sweetMult)
            if solidDesertTime < 0:
                solidDesertTime = 0
        
        liquidDesertTime = portion.liquidDesert / (self.soupEattingSpeed * self.sweetMult)
        if liquidDesertTime < 0:
            liquidDesertTime = 0

        breadTime = portion.bread / self.solidMealEattingSpeed
        if breadTime < 0:
            breadTime = 0

        freshPlantsTime = portion.freshPlants / self.solidMealEattingSpeed
        if freshPlantsTime < 0:
            freshPlantsTime = 0

        milkTime = np.random.normal( 1.5, 0.25 ) * portion.milk / 200.0
        if milkTime < 0:
            milkTime = 0

        # Calculate the total amount
        sumTime = mainTime + soupTime + solidDesertTime + liquidDesertTime + breadTime + freshPlantsTime + milkTime

        return sumTime

    def CalculatePortionEatting( self, portion, time ):

        if self.MakeDecisionToContinueEat():

            portion.main = 0
            portion.soup = 0
            portion.solidDesert = 0
            portion.liquidDesert = 0
            portion.freshPlants = 0
            portion.bread = 0
            portion.milk = 0

        else:

            # Milk
            milkTime = np.random.normal( 1.5, 0.25 ) * portion.milk / 200.0
            if milkTime < time:
                portion.milk = 0
                time = time - milkTime
            elif milkTime > 0:
                portion.milk = portion.milk - portion.milk * time / milkTime
                return portion

            # Solid desert
            if not (self.solidDesertIsTakenToClass):
                solidDesertTime = portion.solidDesert / (self.solidMealEattingSpeed * self.sweetMult)
                if solidDesertTime < time:
                    portion.solidDesert = 0
                    time = time - solidDesertTime
                else:
                    portion.solidDesert = portion.solidDesert - (self.solidMealEattingSpeed * self.sweetMult) * time
                    return portion
            else:
                portion.solidDesert = 0

            # Liquid desert
            liquidDesertTime = portion.liquidDesert / (self.soupEattingSpeed * self.sweetMult)
            if liquidDesertTime < time:
                portion.liquidDesert = 0
                time = time - liquidDesertTime
            else:
                portion.liquidDesert = portion.liquidDesert - (self.solidMealEattingSpeed * self.sweetMult) * time
                return portion

            # Soup
            soupTime = portion.soup / self.soupEattingSpeed
            if soupTime < time:
                portion.soup = 0
                time = time - soupTime
            else:
                portion.soup = portion.soup - self.soupEattingSpeed * time
                return portion

            # Main
            mainTime = portion.main / self.solidMealEattingSpeed
            if mainTime < time:
                portion.main = 0
                time = time - mainTime
            else:
                portion.main = portion.main - self.solidMealEattingSpeed * time
                return portion

            # Bread
            breadTime = portion.bread / self.solidMealEattingSpeed
            if breadTime < time:
                portion.bread = 0
                time = time - breadTime
            else:
                portion.bread = portion.bread - self.solidMealEattingSpeed * time
                return portion

            # Fresh products
            freshPlantsTime = portion.freshPlants / self.solidMealEattingSpeed
            if freshPlantsTime < time:
                portion.freshPlants = 0
                time = time - freshPlantsTime
            else:
                portion.freshPlants = portion.freshPlants - self.solidMealEattingSpeed * time
            
        return portion

    def MakeDecisionToContinueEat(self):
        return np.random.choice( [True, False], p=[1.0-STOP_EAT_IF_TIME_OUT, STOP_EAT_IF_TIME_OUT] )

    def __str__(self):
        return  "sex: " + str(self.sex) + \
            "; year: " + str(self.studyYear) + \
            "; main (g/min): " + str(self.solidMealEattingSpeed) + \
            "; soup (g/min): " + str(self.soupEattingSpeed) + \
            "; mult sweet: " + str(self.sweetMult) + \
            "; dislike kitchen: " + str(self.likeSchoolKitchen) + \
            "; like external food: " + str(self.userOfExternalFood)

def GeneratePerson( girlProb = 0.5, dislikeKitchenProb = 0.2, externalFoodProb = 0.3 ):

    # Generates "Sex"
    population = [ "girl", "boy" ]
    weights = [ girlProb, ( 1.0 - girlProb ) ]
    sex = np.random.choice( population, p=weights ) 

    # Generates if student hates school meal
    likeSchoolKitchen = np.random.choice( [True, False], p=[ 1.0 - dislikeKitchenProb, dislikeKitchenProb ] )

    # Generates if student is user of competitive food
    userOfExternalFood = np.random.choice( [True, False], p=[ externalFoodProb, 1.0 - externalFoodProb ] )

    # Generates "Study Year"
    studyYear = np.random.choice( np.arange(1, 13) )

    # Generate "Eatting Speed"
    # https://doi.org/10.1186/1471-2458-12-351
    solidMealEattingSpeed = np.random.normal( 27, 2 )    # g/min
    soupEattingSpeed = solidMealEattingSpeed * 2.0

    sweetMult = 1
    solidDesertIsTakenToClass = False

    return Person( sex, studyYear, soupEattingSpeed, solidMealEattingSpeed, sweetMult, likeSchoolKitchen, userOfExternalFood, solidDesertIsTakenToClass )

# Probabilities are based on project survey
def GenerateDislikeDays( person ):

    # Five days in week
    dislikeList = np.empty(5)
    if person.likeSchoolKitchen:
        dislikeDays = np.random.normal( 0.0, 0.5 ) 
        dislikeDays = round( dislikeDays ) - 1.0          
    else:
        dislikeDays = np.random.gumbel( 3.0, 0.5 )
        dislikeDays = round( dislikeDays )
        
    if dislikeDays > 5.0:
        dislikeDays = 5.0
    elif dislikeDays < 0.0:
        dislikeDays = 0.0

    return dislikeDays

def GenerateDislikeWeek( dislikeDays ):

    if dislikeDays == 0:
        return [0, 0, 0, 0, 0]
    else:
        numbers = [0, 1, 2, 3, 4]
        days = [0, 0, 0, 0, 0]
        while dislikeDays > 0:
            rand = np.random.choice( numbers )
            days[rand] = 1
            numbers.remove(rand)
            dislikeDays = dislikeDays - 1
        return days

# Generates dislike meal waste
def GenerateDislikeMenu( person, menu ):

    dislikeDays = GenerateDislikeDays( person )
    dislikeDays = GenerateDislikeWeek( dislikeDays )

    portionList = []

    for x in range(5):

        wportion = Portion( 0, 0, 0, 0, 0, 0, 0 )

        if dislikeDays[x] < 1:
            portionList.append( wportion )
        else:

            portion = menu.portionList[x]
      
            wportion.main = portion.main * np.random.normal(0.3, 0.05)
            wportion.soup = portion.soup * np.random.normal(0.15, 0.03)
            wportion.solidDesert = portion.solidDesert * 0.02
            wportion.liquidDesert = portion.liquidDesert * np.random.normal(0.35, 0.07)
            wportion.bread = portion.bread * 0.05
            wportion.freshPlants = portion.freshPlants * np.random.normal(0.3, 0.1)

            wmain = np.random.choice( [True, False], p=[0.92, 0.08] )
            wsoup = np.random.choice( [True, False] )

            if wmain:
                wportion.main = portion.main
            if wsoup:
                wportion.soup = portion.soup
            
            portionList.append( wportion )

    return portionList

# Probabilities are based on project survey
def GenerateEattenAfterSnacks():

    decision = np.random.choice( EXTERNAL_FOOD_TYPES, p=EXTERNAL_FOOD_TYPE_PROB )

    if decision == "BuyInShop":
        eatten = np.random.choice( [0.12, 0.37, 0.62, 0.87] )
        eatten = np.random.normal( eatten, 0.0625 )
        if eatten < 0:
            eatten = 0
        if eatten > 1:
            eatten = 1
        return eatten
    else:
        eatten = np.random.choice( [0.12, 0.37, 0.62, 0.87] )
        eatten = np.random.normal( eatten, 0.0625 )
        if eatten < 0:
            eatten = 0
        if eatten > 1:
            eatten = 1
        return eatten
