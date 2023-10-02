import pandas as pd
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART4_SIM_SOO import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
from PART0_SETTINGS import * 
from math import *

def buildTargetCurve(data):

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
    
    # Retrieve the project path from the 'data' dictionary
    pathForProject = data['pathForProject']

    # Retrieve the log path from the 'data' dictionary
    pathForLog = data['pathForLog']

    # Retrieve the outputs path from the 'data' dictionary
    pathForOutputs = data['pathForOutputs']

    # Retrieve the simulations path from the 'data' dictionary
    pathForSimulations = data['pathForSimulations']

    # Retrieve the targets path from the 'data' dictionary
    pathForTargets = data['pathForTargets']

    # Retrieve the templates path from the 'data' dictionary
    pathForTemplates = data['pathForTemplates'] 

    ################################
    ####                        ####
    ####                        ####
    ####                        ####
    ####       DECLARING        ####
    ####    OTHER VARIABLES     ####
    ####                        ####
    ####                        ####
    ####                        ####
    ################################

    # Retrieve the 'medium' value from the 'data' dictionary
    medium = data['medium']

    # Retrieve the 'optimizationApproach' value from the 'data' dictionary
    optimizationApproach = data['optimizationApproach']

    # Retrieve the 'algorithmLabel' value from the 'data' dictionary
    algorithmLabel = data['algorithmLabel']

    # Retrieve the 'hardeningLaw' value from the 'data' dictionary
    hardeningLaw = data['hardeningLaw']

    # Retrieve the 'configData' value from the 'data' dictionary
    configData = data['configData']

    # Retrieve the 'geometries' value from the 'data' dictionary
    geometries = data['geometries']

    # Retrieve the 'percentageDifference' value from the 'data' dictionary
    percentageDifference = data['percentageDifference']

    # Retrieve the 'numInitialSimulations' value from the 'data' dictionary
    numInitialSimulations = data['numInitialSimulations']


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