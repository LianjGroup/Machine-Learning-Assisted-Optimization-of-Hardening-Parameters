import numpy as np
import pandas as pd

from modules.MOO_SIM import *
from modules.hardeningLaws import *
from modules.helper import *
from modules.stoploss import *
from optimizers.BO import *
from stage0_configs import * 
import stage0_configs 
import stage1_MOO_prepare_targetCurve
from stage1_MOO_prepare_targetCurve import *
from math import *
import os

    ##################################
    ###                            ###
    ###                            ###
    ###     Executing Initial      ###
    ###        Simulations         ###
    ###          for MOO           ###
    ###                            ###
    ###                            ###
    ##################################


def executeSimulations(data):

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

    # Retrieve the 'specsSetForGeneration' value from the 'data' dictionary
    specsSetForGeneration = data['specsSetForGeneration'] 

    # Retrieve the 'targetMovementLimits' value from the 'data' dictionary
    targetMovementLimits = data['targetMovementLimits']


    # Check the value of 'specsSetForGeneration' to determine how to proceed
    if specsSetForGeneration == "manual":
        # Load specifications from a file and convert to a Python dictionary
        specs = np.load(f"{pathForOutputs}/parameters.npy", allow_pickle=True).tolist()
        # Update the number of initial simulations in the 'data' dictionary
        data['numberOfInitialSims'] = len(specs)
    elif specsSetForGeneration == "auto":
        # Generate specifications using Latin hypercube sampling
        specs = simulation.latin_hypercube_sampling(shapeOfTheObject)

    # Iterate over different geometries
    for shapeOfTheObject in geometries:
        # Create a deep copy of the 'data' dictionary
        copyTheData = copy.deepcopy(data)

        # Construct paths for result, simulation, and template directories
        resultPathGeometry = f"{pathForOutputs}/{shapeOfTheObject}"
        simPathGeometry = f"{pathForSimulations}/{shapeOfTheObject}"
        templatePathGeometry = f"{pathForTemplates}/{shapeOfTheObject}"

        # Update paths and 'maxTargetDisplacement' in the copied data
        copyTheData['resultPath'] = resultPathGeometry
        copyTheData['simPath'] = simPathGeometry
        copyTheData['templatePath'] = templatePathGeometry
        copyTheData['maxTargetDisplacement'] = targetMovementLimits[shapeOfTheObject]

        # Create a simulation object 'simulation' with the updated data
        simulation = MOO_SIM(copyTheData) 

        if not os.path.exists(f"{resultPathGeometry}/initial/common/FD_Curves_unsmooth.npy"):
            printLog("***********************************************************", pathForLog)
            printLog(f"Shape with the name: {shapeOfTheObject} , doesn't have any simulations.", pathForLog)
            printLog(f"Simulations for the shape with name: {shapeOfTheObject} , are running.", pathForLog)
            simulation.run_initial_simulations(specs)
            printLog(f"Simulations for the shape with name: {shapeOfTheObject} have been completed", pathForLog)
        else: 
            printLog("***********************************************************", pathForLog)
            printLog(f"Simulations for the shape with name: {shapeOfTheObject}, already exist.", pathForLog)
            numberOfInitialSims = len(np.load(f"{resultPathGeometry}/initial/common/FD_Curves_unsmooth.npy", allow_pickle=True).tolist())
            printLog(f"Simulation count for the geometry named {shapeOfTheObject}: {numberOfInitialSims} FD curves", pathForLog)

if __name__ == "__main__":
    info = stage0_configs.load_settings()
    targetCurves, maxTargetDisplacements = stage1_MOO_prepare_targetCurve.buildTargetCurve(info)
    info['targetCurves'] = targetCurves
    info['maxTargetDisplacements'] = maxTargetDisplacements
    executeSimulations(info)