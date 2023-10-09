import numpy as np
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART3_SIM_MOO import *
from ASSETS.PART4_SIM_SOO import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
from math import *


def main_iterative_calibration(info):

    logPath = info['logPath']
    resultPath = info['resultPath']
    material = info['material']
    optimizerName = info['optimizerName']
    hardeningLaw = info['hardeningLaw']
    paramConfig = info['paramConfig']
    geometries = info['geometries']
    curveIndex = info['curveIndex']
    deviationPercent = info['deviationPercent']
    targetCurves = info['targetCurves']
    yieldingIndices = info['yieldingIndices']
    
    if optimizerName == "BO":
        param_bounds = parseBoundsBO(info['paramConfig'])

    initial_original_geom_to_param_FD_Curves_smooth = info['initial_original_geom_to_param_FD_Curves_smooth']
    iteration_original_geom_to_param_FD_Curves_smooth = info['iteration_original_geom_to_param_FD_Curves_smooth']
    combined_original_geom_to_param_FD_Curves_smooth = info['combined_original_geom_to_param_FD_Curves_smooth']
    initial_interpolated_geom_to_param_FD_Curves_smooth = info['initial_interpolated_geom_to_param_FD_Curves_smooth']
    iteration_interpolated_geom_to_param_FD_Curves_smooth = info['iteration_interpolated_geom_to_param_FD_Curves_smooth']
    combined_interpolated_geom_to_param_FD_Curves_smooth = info['combined_interpolated_geom_to_param_FD_Curves_smooth']
    combined_interpolated_param_to_geom_FD_Curves_smooth = info['combined_interpolated_param_to_geom_FD_Curves_smooth']
    iteration_original_geom_to_param_FD_Curves_unsmooth = info['iteration_original_geom_to_param_FD_Curves_unsmooth']
    iteration_original_param_to_geom_FD_Curves_smooth = info['iteration_original_param_to_geom_FD_Curves_smooth']
    
    initial_original_geom_to_param_flowCurves = info['initial_original_geom_to_param_flowCurves']
    iteration_original_geom_to_param_flowCurves = info['iteration_original_geom_to_param_flowCurves']
    combined_original_geom_to_param_flowCurves = info['combined_original_geom_to_param_flowCurves']

    sim = MOO_SIM(info)
    

    #SAVING THESE TO USE IN OUR DUMMY MODEL
    np.save("combined_interpolated_param_to_geom_FD_Curves_smooth.npy", combined_interpolated_param_to_geom_FD_Curves_smooth)
    np.save("targetCurves.npy", targetCurves)

    while not stopFD_MOO(targetCurves, list(combined_interpolated_param_to_geom_FD_Curves_smooth.values())[-1], geometries, yieldingIndices, deviationPercent):

        iterationIndex = len(iteration_original_param_to_geom_FD_Curves_smooth) + 1
        exampleGeometry = geometries[0]
        if optimizerName == "BO":
            geometryWeights = MOO_calculate_geometries_weight(targetCurves, geometries)
            printLog("The weights for the geometries are: ", logPath)
            printLog(str(geometryWeights), logPath)
            

            MOO_write_BO_json_log(combined_interpolated_param_to_geom_FD_Curves_smooth, targetCurves, geometries, geometryWeights, yieldingIndices, paramConfig,iterationIndex)
            BO_instance = BO(info)
            BO_instance.initializeOptimizer(lossFunction=None, param_bounds=param_bounds, loadingProgress=True)
            next_paramDict = BO_instance.suggest()
            next_paramDict = rescale_paramsDict(next_paramDict, paramConfig)
            
        if optimizerName == "BOTORCH":
            pareto_front = MOO_suggest_BOTORCH(combined_interpolated_param_to_geom_FD_Curves_smooth, targetCurves, geometries, yieldingIndices, paramConfig,iterationIndex)
            next_paramDict = pareto_front[0]
        

        printLog("\n" + 60 * "#" + "\n", logPath)
        printLog(f"Running iteration {iterationIndex} for {material}_{hardeningLaw}_curve{curveIndex}" , logPath)
        printLog(f"The next candidate {hardeningLaw} parameters predicted by {optimizerName}", logPath)
        prettyPrint(next_paramDict, paramConfig, logPath)

        time.sleep(30)
        printLog("Start running iteration simulation", logPath)
        
        geom_to_param_new_FD_Curves, geom_to_param_new_flowCurves = sim.run_iteration_simulations(next_paramDict, iterationIndex)
        
        geom_to_param_new_FD_Curves_unsmooth = copy.deepcopy(geom_to_param_new_FD_Curves)
        geom_to_param_new_FD_Curves_smooth = copy.deepcopy(geom_to_param_new_FD_Curves)
        new_param = list(geom_to_param_new_FD_Curves[exampleGeometry].keys())[0]
        
        for geometry in geometries:
            geom_to_param_new_FD_Curves_smooth[geometry][new_param]['force'] = smoothing_force(geom_to_param_new_FD_Curves_unsmooth[geometry][new_param]['force'], startIndex=20, endIndex=90, iter=20000)
        
        # Updating the combined FD curves smooth
        for geometry in geometries:
            combined_original_geom_to_param_FD_Curves_smooth[geometry].update(geom_to_param_new_FD_Curves_smooth[geometry])
            combined_interpolated_geom_to_param_FD_Curves_smooth[geometry] = interpolating_FD_Curves(combined_original_geom_to_param_FD_Curves_smooth[geometry], targetCurves[geometry])
        
        # Updating the iteration FD curves smooth
        for geometry in geometries:
            iteration_original_geom_to_param_FD_Curves_smooth[geometry].update(geom_to_param_new_FD_Curves_smooth[geometry])
            iteration_interpolated_geom_to_param_FD_Curves_smooth[geometry] = interpolating_FD_Curves(iteration_original_geom_to_param_FD_Curves_smooth[geometry], targetCurves[geometry])
        
        # Updating the iteration FD curves unsmooth
        for geometry in geometries:
            iteration_original_geom_to_param_FD_Curves_unsmooth[geometry].update(geom_to_param_new_FD_Curves_unsmooth[geometry])
        
        # Updating the original flow curves
        for geometry in geometries:
            combined_original_geom_to_param_flowCurves[geometry].update(geom_to_param_new_flowCurves[geometry])
            iteration_original_geom_to_param_flowCurves[geometry].update(geom_to_param_new_flowCurves[geometry])
        
        # Updating the param_to_geom data
        combined_interpolated_param_to_geom_FD_Curves_smooth = reverseAsParamsToGeometries(combined_interpolated_geom_to_param_FD_Curves_smooth, geometries)
        iteration_original_param_to_geom_FD_Curves_smooth = reverseAsParamsToGeometries(iteration_original_geom_to_param_FD_Curves_smooth, geometries)

        loss_newIteration = {}
        for geometry in geometries:
            yieldingIndex = yieldingIndices[geometry]
            
            simForce = list(iteration_interpolated_geom_to_param_FD_Curves_smooth[geometry].values())[0]['force'][yieldingIndex:]
            simDisplacement = list(iteration_interpolated_geom_to_param_FD_Curves_smooth[geometry].values())[0]['displacement'][yieldingIndex:]
            targetForce = targetCurves[geometry]['force'][yieldingIndex:]
            targetDisplacement = targetCurves[geometry]['displacement'][yieldingIndex:]
            interpolated_simForce = interpolatingForce(simDisplacement, simForce, targetDisplacement)
            loss_newIteration[geometry] = round(lossFD(targetDisplacement, targetForce, interpolated_simForce,iterationIndex), 3)
        
        printLog(f"The loss of the new iteration is: ", logPath)
        printLog(str(loss_newIteration), logPath)

        # Saving the iteration data
        for geometry in geometries:
            np.save(f"{resultPath}/{geometry}/iteration/common/FD_Curves_unsmooth.npy", iteration_original_geom_to_param_FD_Curves_unsmooth[geometry])
            np.save(f"{resultPath}/{geometry}/iteration/common/FD_Curves_smooth.npy", iteration_original_geom_to_param_FD_Curves_smooth[geometry])
            np.save(f"{resultPath}/{geometry}/iteration/common/flowCurves.npy", iteration_original_geom_to_param_flowCurves[geometry])