import numpy as np

# Probabilities are based on project survey
def GenerateSportDays( ):

    sportDays = 2

    numbers = [0, 1, 2, 3, 4]
    days = [0, 0, 0, 0, 0]

    while sportDays > 0:
        rand = np.random.choice( numbers )
        days[rand] = 1
        numbers.remove(rand)
        sportDays = sportDays - 1

    return days