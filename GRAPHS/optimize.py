from ASSETS.PART4_SIM_SOO import *
from ASSETS.PART1_HARDENINGLAWS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART5_GUARD import *
from MODELS.PART1_BAYESIANOPT import *
import PART0_SETTINGS 
import PART3_PREPSOO 
import PART4_RUNSIMS_MOO
from math import *

def main_optimize():

    data = PART0_SETTINGS.load_settings()
    
    logPath = data['logPath']
    optimizeStrategy = data['optimizeStrategy']
    deviationPercent = data['deviationPercent']

    if optimizeStrategy == "SOO":
        targetCurve, maxTargetDisplacement = PART3_PREPSOO.buildTargetCurve(data)
        data['targetCurve'] = targetCurve
        data['maxTargetDisplacement'] = maxTargetDisplacement

        PART4_RUNSIMS_MOO.executeSimulations(data)

        FD_Curves_dict, flowCurves_dict = stage3_SOO_prepare_simCurves.main_prepare_simCurves(data) 
        data["initial_original_FD_Curves_smooth"] = FD_Curves_dict['initial_original_FD_Curves_smooth']
        data["iteration_original_FD_Curves_smooth"] = FD_Curves_dict['iteration_original_FD_Curves_smooth']
        data["combined_original_FD_Curves_smooth"] = FD_Curves_dict['combined_original_FD_Curves_smooth']
        data["initial_interpolated_FD_Curves_smooth"] = FD_Curves_dict['initial_interpolated_FD_Curves_smooth']
        data["iteration_interpolated_FD_Curves_smooth"] = FD_Curves_dict['iteration_interpolated_FD_Curves_smooth']
        data["combined_interpolated_FD_Curves_smooth"] = FD_Curves_dict['combined_interpolated_FD_Curves_smooth']
        data['iteration_original_FD_Curves_unsmooth'] = FD_Curves_dict['iteration_original_FD_Curves_unsmooth'] 
        data["initial_original_flowCurves"] = flowCurves_dict['initial_original_flowCurves']
        data["iteration_original_flowCurves"] = flowCurves_dict['iteration_original_flowCurves']
        data["combined_original_flowCurves"] = flowCurves_dict['combined_original_flowCurves']
    
        stage4_SOO_iterative_calibration.main_iterative_calibration(data)
        
    elif optimizeStrategy == "MOO":
        targetCurves, maxTargetDisplacements = stage1_MOO_prepare_targetCurve.main_prepare_targetCurve(data)
        data['targetCurves'] = targetCurves
        data['maxTargetDisplacements'] = maxTargetDisplacements

        stage2_MOO_run_initialSims.main_run_initialSims(data)
        
        FD_Curves_dict, flowCurves_dict = stage3_MOO_prepare_simCurves.main_prepare_simCurves(data) 
        data["initial_original_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['initial_original_geom_to_param_FD_Curves_smooth']
        data["iteration_original_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['iteration_original_geom_to_param_FD_Curves_smooth']
        data["combined_original_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['combined_original_geom_to_param_FD_Curves_smooth']
        data["initial_interpolated_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['initial_interpolated_geom_to_param_FD_Curves_smooth']
        data["iteration_interpolated_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['iteration_interpolated_geom_to_param_FD_Curves_smooth']
        data["combined_interpolated_geom_to_param_FD_Curves_smooth"] = FD_Curves_dict['combined_interpolated_geom_to_param_FD_Curves_smooth']
        data['iteration_original_geom_to_param_FD_Curves_unsmooth'] = FD_Curves_dict['iteration_original_geom_to_param_FD_Curves_unsmooth'] 
        data['combined_interpolated_param_to_geom_FD_Curves_smooth'] = FD_Curves_dict['combined_interpolated_param_to_geom_FD_Curves_smooth'] 
        data['iteration_original_param_to_geom_FD_Curves_smooth'] = FD_Curves_dict['iteration_original_param_to_geom_FD_Curves_smooth']
        data["initial_original_geom_to_param_flowCurves"] = flowCurves_dict['initial_original_geom_to_param_flowCurves']
        data["iteration_original_geom_to_param_flowCurves"] = flowCurves_dict['iteration_original_geom_to_param_flowCurves']
        data["combined_original_geom_to_param_flowCurves"] = flowCurves_dict['combined_original_geom_to_param_flowCurves']
        
        stage4_MOO_iterative_calibration.main_iterative_calibration(data)

    printLog(f"The simulations have satisfied the {deviationPercent}% deviation stop condition")
    printLog("Parameter calibration has successfully completed", logPath)
    

if __name__ == "__main__":
    main_optimize()