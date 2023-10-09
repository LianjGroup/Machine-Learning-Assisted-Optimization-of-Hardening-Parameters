import pandas as pd
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART4_SIM_SOO import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
from GRAPHS.PART0_SETTINGS import * 
from math import *

    ################################
    ####                        ####
    ####                        ####
    ####                        ####
    #### BUILDING TARGET CURVE  ####
    ####        FOR SOO         ####
    ####                        ####
    ####                        ####
    ####                        ####
    ################################


def buildTargetCurve(data):

    # Retrieve the targets path from the 'data' dictionary
    pathForTargets = data['pathForTargets']

    ################################
    ####                        ####
    ####                        ####
    ####                        ####
    ####  CURVE SPECIFICATIONS  ####
    ####                        ####
    ####                        ####
    ####                        ####
    ################################

    # Read data from a CSV file
    dataFrame = pd.read_csv(f'{pathForTargets}/FD_Curve.csv')

    # Extract displacement and force data from the DataFrame
    anticipatedShift = dataFrame['displacement/mm'].to_numpy()
    anticipatedForce = dataFrame['force/N'].to_numpy()

    # Create a dictionary for the intended curve    
    intendedCurve = {}
    intendedCurve['displacement'] = anticipatedShift
    intendedCurve['force'] = anticipatedForce

    # Store the intended curve and target movement limit in dictionaries
    targetMovementLimits = ceil(max(anticipatedShift) * 10) / 10

    # Return the dictionaries containing intended curves and target movement limits
    return intendedCurve, targetMovementLimits