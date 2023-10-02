import numpy as np
import pandas as pd
from modules.SOO_SIM import *
from modules.MOO_SIM import *
from modules.hardeningLaws import *
from modules.helper import *
from modules.stoploss import *
from MODELS.PART1_BAYESIANOPT import *
from PART0_SETTINGS import * 
from PART3_PREPSOO import *
from math import *
import os

def executeSimulations(info):

    # ---------------------------------------#
    #   Step 2: Running initial simulations  #
    # ---------------------------------------#
    
    pathForProject = info['pathForProject']
    pathForLog = info['pathForLog']
    pathForOutputs = info['pathForOutputs']
    pathForSimulations = info['pathForSimulations']
    pathForTargets = info['pathForTargets']

    
    templatePath = info['templatePath'] 
    material = info['material']
    optimizeStrategy = info['optimizeStrategy']
    optimizerName = info['optimizerName']
    hardeningLaw = info['hardeningLaw']
    paramConfig = info['paramConfig']
    geometry = info['geometry']
    deviationPercent = info['deviationPercent']
    numberOfInitialSims = info['numberOfInitialSims']
    generateParams = info['generateParams'] 

    if generateParams == "manual":
        parameters = np.load(f"{resultPath}/initial/common/parameters.npy", allow_pickle=True).tolist()
        info['numberOfInitialSims'] = len(parameters)
    elif generateParams == "auto":
        parameters = sim.latin_hypercube_sampling()

    sim = SOO_SIM(info)    
    
    if not os.path.exists(f"{resultPath}/initial/common/FD_Curves_unsmooth.npy"):
        printLog("There are no initial simulations. Program starts running the initial simulations", logPath)
        sim.run_initial_simulations(parameters)
    else: 
        printLog("Initial simulations already exist", logPath)
        numberOfInitialSims = len(np.load(f"{resultPath}/initial/common/FD_Curves_unsmooth.npy", allow_pickle=True).tolist())
        printLog(f"Number of initial simulations: {numberOfInitialSims} FD curves", logPath)
