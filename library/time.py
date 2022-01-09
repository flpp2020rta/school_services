import numpy as np
from random import choices

# Source: https://bmcpublichealth.biomedcentral.com/articles/10.1186/1471-2458-12-351
def GenerateTalkingTime( ):
    talkingTime = np.random.normal( 2.1, 0.8 )
    return talkingTime

# Source: project survey
def GeneratePathTimeForClassroom( ):
    pathTime = np.random.normal( 1.5, 0.25 )
    return pathTime

# Source: project survey
def GeneratePathTimeForSport( ):
    pathTime = np.random.normal( 3.0, 1.0 )
    return pathTime