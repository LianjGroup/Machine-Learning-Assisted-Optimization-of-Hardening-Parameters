import numpy as np
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART3_SIM_MOO import *
from ASSETS.PART4_SIM_SOO import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
from math import *
import os
import copy

def main_prepare_simCurves(info):
    
    logPath = info['logPath']
    resultPath = info['resultPath']
    geometries = info['geometries']    
    targetCurves = info['targetCurves']
    exampleGeometry = geometries[0]

    initial_original_geom_to_param_FD_Curves_unsmooth = {}
    initial_original_geom_to_param_FD_Curves_smooth = {}
    initial_original_geom_to_param_flowCurves = {}
    for geometry in geometries:
        initial_original_geom_to_param_FD_Curves_unsmooth[geometry] = np.load(f"{resultPath}/{geometry}/initial/common/FD_Curves_unsmooth.npy", allow_pickle=True).tolist()
        initial_original_geom_to_param_FD_Curves_smooth[geometry] = np.load(f"{resultPath}/{geometry}/initial/common/FD_Curves_smooth.npy", allow_pickle=True).tolist()
        initial_original_geom_to_param_flowCurves[geometry] = np.load(f"{resultPath}/{geometry}/initial/common/flowCurves.npy", allow_pickle=True).tolist()
    
    iteration_original_geom_to_param_FD_Curves_smooth = {}
    iteration_original_geom_to_param_FD_Curves_unsmooth = {}
    iteration_original_geom_to_param_flowCurves = {}
    
    if not os.path.exists(f"{resultPath}/{exampleGeometry}/iteration/common/FD_Curves_unsmooth.npy"):
        printLog("There are no iteration simulations. Program starts running the iteration simulations", logPath)
        for geometry in geometries:
            iteration_original_geom_to_param_FD_Curves_smooth[geometry] = {}
            iteration_original_geom_to_param_FD_Curves_unsmooth[geometry] = {}
            iteration_original_geom_to_param_flowCurves[geometry] = {}
    else:
        printLog("Iteration simulations exist", logPath)
        numberOfIterationSims = len(np.load(f"{resultPath}/{exampleGeometry}/iteration/common/FD_Curves_unsmooth.npy", allow_pickle=True).tolist())
        printLog(f"Number of iteration simulations: {numberOfIterationSims} FD curves", logPath)
        for geometry in geometries:
            iteration_original_geom_to_param_FD_Curves_smooth[geometry] = np.load(f"{resultPath}/{geometry}/iteration/common/FD_Curves_smooth.npy", allow_pickle=True).tolist()
            iteration_original_geom_to_param_FD_Curves_unsmooth[geometry] = np.load(f"{resultPath}/{geometry}/iteration/common/FD_Curves_unsmooth.npy", allow_pickle=True).tolist()
            iteration_original_geom_to_param_flowCurves[geometry] = np.load(f"{resultPath}/{geometry}/iteration/common/flowCurves.npy", allow_pickle=True).tolist()
    
    combined_original_geom_to_param_FD_Curves_smooth = copy.deepcopy(initial_original_geom_to_param_FD_Curves_smooth)
    combined_original_geom_to_param_flowCurves = copy.deepcopy(initial_original_geom_to_param_flowCurves)
    
    for geometry in geometries:
        combined_original_geom_to_param_FD_Curves_smooth[geometry].update(iteration_original_geom_to_param_FD_Curves_smooth[geometry])
        combined_original_geom_to_param_flowCurves[geometry].update(iteration_original_geom_to_param_flowCurves[geometry])
    
    
    initial_interpolated_geom_to_param_FD_Curves_smooth = {}
    iteration_interpolated_geom_to_param_FD_Curves_smooth = {}
    combined_interpolated_geom_to_param_FD_Curves_smooth = {}

    for geometry in geometries:
        initial_interpolated_geom_to_param_FD_Curves_smooth[geometry] = interpolating_FD_Curves(initial_original_geom_to_param_FD_Curves_smooth[geometry], targetCurves[geometry])
        iteration_interpolated_geom_to_param_FD_Curves_smooth[geometry] = interpolating_FD_Curves(iteration_original_geom_to_param_FD_Curves_smooth[geometry], targetCurves[geometry])
        combined_interpolated_geom_to_param_FD_Curves_smooth[geometry] = interpolating_FD_Curves(combined_original_geom_to_param_FD_Curves_smooth[geometry], targetCurves[geometry])

    FD_Curves_dict = {}
    flowCurves_dict = {}

    FD_Curves_dict['initial_original_geom_to_param_FD_Curves_smooth'] = initial_original_geom_to_param_FD_Curves_smooth
    FD_Curves_dict['iteration_original_geom_to_param_FD_Curves_smooth'] = iteration_original_geom_to_param_FD_Curves_smooth
    FD_Curves_dict['combined_original_geom_to_param_FD_Curves_smooth'] = combined_original_geom_to_param_FD_Curves_smooth
    FD_Curves_dict['initial_interpolated_geom_to_param_FD_Curves_smooth'] = initial_interpolated_geom_to_param_FD_Curves_smooth
    FD_Curves_dict['iteration_interpolated_geom_to_param_FD_Curves_smooth'] = iteration_interpolated_geom_to_param_FD_Curves_smooth
    FD_Curves_dict['combined_interpolated_geom_to_param_FD_Curves_smooth'] = combined_interpolated_geom_to_param_FD_Curves_smooth
    
    FD_Curves_dict['combined_interpolated_param_to_geom_FD_Curves_smooth'] = reverseAsParamsToGeometries(combined_interpolated_geom_to_param_FD_Curves_smooth, geometries)
    FD_Curves_dict['iteration_original_param_to_geom_FD_Curves_smooth'] = reverseAsParamsToGeometries(iteration_original_geom_to_param_FD_Curves_smooth, geometries)
    FD_Curves_dict['iteration_original_geom_to_param_FD_Curves_unsmooth'] = iteration_original_geom_to_param_FD_Curves_unsmooth
    
    flowCurves_dict['initial_original_geom_to_param_flowCurves'] = initial_original_geom_to_param_flowCurves
    flowCurves_dict['iteration_original_geom_to_param_flowCurves'] = iteration_original_geom_to_param_flowCurves
    flowCurves_dict['combined_original_geom_to_param_flowCurves'] = combined_original_geom_to_param_flowCurves
 
    return FD_Curves_dict, flowCurves_dict

    