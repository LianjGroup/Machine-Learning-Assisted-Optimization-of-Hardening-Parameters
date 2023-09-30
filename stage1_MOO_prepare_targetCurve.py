import pandas as pd
from modules.SOO_SIM import *
from modules.hardeningLaws import *
from modules.helper import *
from modules.stoploss import *
from optimizers.BO import *
from stage0_configs import * 
from math import *

    ################################
    ####                        ####
    ####                        ####
    ####                        ####
    #### BUILDING TARGET CURVE  ####
    ####        FOR MOO         ####
    ####                        ####
    ####                        ####
    ####                        ####
    ################################

def buildTargetCurve(data):
    
    ################################
    ####                        ####
    ####                        ####
    ####                        ####
    ####       DECLARING        ####
    ####     PATH VARIABLES     ####
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
    
    # Initialize empty dictionaries for storing data
    intendedCurves = {}
    targetMovementLimits = {}

    # Iterate over each 'geometry' in the 'geometries' list
    for geometry in geometries:
        # Read data from a CSV file based on 'geometry'
        dataFrame = pd.read_csv(f'{pathForTargets}/{geometry}/FD_Curve.csv')
        
        # Extract displacement and force data from the DataFrame
        anticipatedShift = dataFrame['displacement/mm'].to_numpy()
        anticipatedForce = dataFrame['force/N'].to_numpy()
        
        # Create a dictionary for the intended curve
        intendedCurve = {}
        intendedCurve['displacement'] = anticipatedShift
        intendedCurve['force'] = anticipatedForce
        
        # Calculate the target movement limit
        targetMovementLimit = ceil(max(anticipatedShift) * 10) / 10
        
        # Store the intended curve and target movement limit in dictionaries
        intendedCurves[geometry] = intendedCurve
        targetMovementLimits[geometry] = targetMovementLimit

    # Return the dictionaries containing intended curves and target movement limits
    return intendedCurves, targetMovementLimits
