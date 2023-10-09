import numpy as np
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART3_SIM_MOO import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
from GRAPHS.PART0_SETTINGS import * 
import GRAPHS.PART0_SETTINGS as PART0_SETTINGS 
import GRAPHS.PART2_PREPMOO as PART2_PREPMOO
from GRAPHS.PART2_PREPMOO import *
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

    # Retrieve the log path from the 'data' dictionary
    pathForLog = data['pathForLog']

    # Retrieve the outputs path from the 'data' dictionary
    pathForOutputs = data['pathForOutputs']

    # Retrieve the simulations path from the 'data' dictionary
    pathForSimulations = data['pathForSimulations']

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

    # Retrieve the 'geometries' value from the 'data' dictionary
    geometries = data['geometries']

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
    info = PART0_SETTINGS.load_settings()
    targetCurves, maxTargetDisplacements = PART2_PREPMOO.buildTargetCurve(info)
    info['targetCurves'] = targetCurves
    info['maxTargetDisplacements'] = maxTargetDisplacements
    executeSimulations(info)