import json
import os
import numpy as np
import pandas as pd
from prettytable import PrettyTable
import copy
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from datetime import datetime
from ASSETS.PART5_GUARD import *
import torch
import numpy as np
from botorch.models import SingleTaskGP
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.fit import fit_gpytorch_model
from botorch.acquisition.multi_objective import qExpectedHypervolumeImprovement
from botorch.optim import optimize_acqf
from botorch.utils.multi_objective.box_decompositions import NondominatedPartitioning
from botorch.utils.multi_objective.pareto import is_non_dominated
from botorch.utils import standardize
from botorch.acquisition.multi_objective.objective import IdentityMCMultiOutputObjective
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def printLog(message, logPath):
    with open(logPath, 'a+') as logFile:
        logFile.writelines(message + "\n")
    print(message)

def parseBoundsBO(paramInfo):
    paramBounds = {}
    for param in paramInfo:
        paramBounds[param] = (paramInfo[param]['lowerBound'], paramInfo[param]['upperBound'])
    return paramBounds

def is_directory_empty(directory_path):
    return len(os.listdir(directory_path)) == 0

def smoothing_force(force, startIndex, endIndex, iter=20000):
    smooth_force = copy.deepcopy(force)
    for i in range(iter):
        smooth_force = savgol_filter(smooth_force[startIndex:endIndex], window_length=5, polyorder=3,mode='interp', delta=1)
        smooth_force = np.concatenate((force[0:startIndex], smooth_force, force[endIndex:]))
    return smooth_force

def interpolatingForce(simDisplacement, simForce, targetDisplacement):
    interpolatingFunction = interp1d(simDisplacement, simForce, fill_value='extrapolate')
    interpolatedSimForce = interpolatingFunction(targetDisplacement)
    return interpolatedSimForce

def interpolating_FD_Curves(FD_Curves, targetCurve):
    FD_Curves_copy = copy.deepcopy(FD_Curves)
    for paramsTuple, dispforce in FD_Curves_copy.items():
        simDisp = dispforce["displacement"]
        simForce = dispforce["force"]
        targetDisp = targetCurve["displacement"]
        FD_Curves_copy[paramsTuple]["force"] = interpolatingForce(simDisp, simForce, targetDisp)
        FD_Curves_copy[paramsTuple]["displacement"] = targetDisp
    return FD_Curves_copy

def interpolatingStress(simStrain, simStress, targetStrain):
    interpolatingFunction = interp1d(simStrain, simStress, fill_value='extrapolate')
    interpolatedSimStress = interpolatingFunction(targetStrain)
    return interpolatedSimStress

def interpolating_flowCurves(flowCurves, targetCurve):
    flowCurves_copy = copy.deepcopy(flowCurves)
    for paramsTuple, strainstress in flowCurves_copy.items():
        simStrain = strainstress["strain"]
        simStress = strainstress["stress"]
        targetStrain = targetCurve["strain"]
        flowCurves_copy[paramsTuple]["stress"] = interpolatingStress(simStrain, simStress, targetStrain)
        flowCurves_copy[paramsTuple]["strain"] = targetStrain
    return flowCurves_copy

def SOO_write_BO_json_log(FD_Curves, targetCurve, yieldingIndex, paramConfig,iteration):
    if os.path.exists(f"optimizers/logs.json"):
        os.remove(f"optimizers/logs.json")

    for paramsTuple, dispforce in FD_Curves.items():
        line = {}
        line["target"] = -lossFD(targetCurve["displacement"][yieldingIndex:], targetCurve["force"][yieldingIndex:], dispforce["force"][yieldingIndex:],iteration)
        line["params"] = dict(paramsTuple)
        for param in paramConfig:
            line["params"][param] = line["params"][param]/paramConfig[param]["exponent"] 
        line["datetime"] = {}
        line["datetime"]["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line["datetime"]["elapsed"] = 0.0
        line["datetime"]["delta"] = 0.0
        with open(f"optimizers/logs.json", "a") as file:
            json.dump(line, file)
            file.write("\n")

def MOO_write_BO_json_log(combined_interpolated_params_to_geoms_FD_Curves_smooth, targetCurves, geometries, geometryWeights, yieldingIndices, paramConfig,iteration):
    
    if os.path.exists(f"optimizers/logs.json"):
        os.remove(f"optimizers/logs.json")

    for paramsTuple, geometriesToForceDisplacement in combined_interpolated_params_to_geoms_FD_Curves_smooth.items():
        line = {}
        loss = 0
        for geometry in geometries:
            yieldingIndex = yieldingIndices[geometry]
            loss += - geometryWeights[geometry] * lossFD(targetCurves[geometry]["displacement"][yieldingIndex:], targetCurves[geometry]["force"][yieldingIndex:], geometriesToForceDisplacement[geometry]["force"][yieldingIndex:],iteration)
        line["target"] = loss
        line["params"] = dict(paramsTuple)
        for param in paramConfig:
            line["params"][param] = line["params"][param]/paramConfig[param]["exponent"] 
        line["datetime"] = {}
        line["datetime"]["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line["datetime"]["elapsed"] = 0.0
        line["datetime"]["delta"] = 0.0
        with open(f"optimizers/logs.json", "a") as file:
            json.dump(line, file)
            file.write("\n")

def MOO_suggest_BOTORCH(combined_interpolated_params_to_geoms_FD_Curves_smooth, targetCurves, geometries, yieldingIndices, paramConfig,iteration):
    params = []
    losses = []
    for param_tuple, geom_to_simCurves in combined_interpolated_params_to_geoms_FD_Curves_smooth.items():
        params.append([value for param, value in param_tuple])
        loss_iter = []
        for geometry in geometries:
            yieldingIndex = yieldingIndices[geometry]
            loss_iter.append(- lossFD(
                targetCurves[geometry]["displacement"][yieldingIndex:], 
                targetCurves[geometry]["force"][yieldingIndex:], 
                geom_to_simCurves[geometry]["force"][yieldingIndex:],
                iteration
            ))
        losses.append(loss_iter)

    X = torch.tensor(params, dtype=torch.float64)
    Y = torch.stack([torch.tensor(loss, dtype=torch.float64) for loss in losses])

    lower_bounds = torch.tensor([paramConfig[param]['lowerBound'] * paramConfig[param]['exponent'] for param in paramConfig.keys()]).float()
    upper_bounds = torch.tensor([paramConfig[param]['upperBound'] * paramConfig[param]['exponent'] for param in paramConfig.keys()]).float()

    bounds = np.vstack([lower_bounds, upper_bounds])

    scaler = MinMaxScaler().fit(bounds)

    X_normalized = torch.tensor(scaler.transform(X.numpy()), dtype=torch.float64)

    Y_standardized = standardize(Y)

    bounds_normalized = torch.tensor([[0.0]*X_normalized.shape[1], [1.0]*X_normalized.shape[1]])

    model = SingleTaskGP(X_normalized, Y_standardized)
    mll = ExactMarginalLogLikelihood(model.likelihood, model)
    fit_gpytorch_model(mll)

    ref_point = Y_standardized.max(dim=0).values - 0.01

    partitioning = NondominatedPartitioning(ref_point=ref_point, Y=Y_standardized)
    acq_func = qExpectedHypervolumeImprovement(
        model=model,
        partitioning=partitioning,
        ref_point=ref_point,
        objective=IdentityMCMultiOutputObjective(),
    )

    candidates, _ = optimize_acqf(
        acq_function=acq_func,
        bounds=bounds_normalized,
        q=1,
        num_restarts=10,
        raw_samples=1000,
    )

    candidates = torch.tensor(scaler.inverse_transform(candidates.detach().numpy()), dtype=torch.float64)

    pareto_front = [{param: value.item() for param, value in zip(paramConfig.keys(), next_param)} for next_param in candidates]
    return pareto_front

def MOO_calculate_geometries_weight(targetCurves, geometries):
    geometryWeights = {}
    
    for geometry in geometries:
        targetDisplacement = targetCurves[geometry]["displacement"]
        targetForce = targetCurves[geometry]["force"]
        
        x_start = min(targetDisplacement)
        x_end = max(targetDisplacement)

        target_FD_func = interp1d(targetDisplacement, targetForce, fill_value="extrapolate")

        x_values = np.linspace(x_start, x_end, num=10000)

        y_values = target_FD_func(x_values)

        area = simpson(y_values, x_values)
        geometryWeights[geometry] = 1/np.array(area)
    
    sumWeights = np.sum(list(geometryWeights.values()))
    for geometry in geometryWeights:
        geometryWeights[geometry] = geometryWeights[geometry]/sumWeights

    return geometryWeights

def prettyPrint(parameters, paramConfig, logPath):
    logTable = PrettyTable()
    logTable.field_names = ["Parameter", "Value"]
    for param in parameters:
        paramName = paramConfig[param]['name']
        paramValue = parameters[param]
        paramUnit = paramConfig[param]['unit']
        paramValueUnit = f"{paramValue} {paramUnit}" if paramUnit != "dimensionless" else paramValue
        logTable.add_row([paramName, paramValueUnit])

    stringMessage = "\n"
    stringMessage += logTable.get_string()
    stringMessage += "\n"

    printLog(stringMessage, logPath)


def read_FD_Curve(filePath):
    output_data=np.loadtxt(filePath, skiprows=2)
    columns=['X', 'Displacement', 'Force']
    df = pd.DataFrame(data=output_data, columns=columns)
    displacement = df.iloc[:, 1].to_numpy()
    force = df.iloc[:, 2].to_numpy()
    return displacement, force

def create_parameter_file(filePath, paramsDict):
    columns = ["Parameter", "Value"]
    df = pd.DataFrame(columns=columns)
    for key, value in paramsDict.items():
        df.loc[len(df.index)] = [key, value]
    df.to_excel(f"{filePath}/parameters.xlsx", index=False)
    df.to_csv(f"{filePath}/parameters.csv", index=False)

def create_flowCurve_file(filePath, truePlasticStrain, trueStress):
    columns = ["strain,-", "stress,MPa", "stress,Pa"]
    df = pd.DataFrame(columns=columns)
    for i in range(len(truePlasticStrain)):
        df.loc[len(df.index)] = [truePlasticStrain[i], trueStress[i], trueStress[i]*1e6]
    df.to_excel(f"{filePath}/flowCurve.xlsx", index=False)
    df.to_csv(f"{filePath}/flowCurve.csv", index=False)

def create_FD_Curve_file(filePath, displacement, force):
    columns = ["displacement,mm", "force,kN", "force,N"]
    df = pd.DataFrame(columns=columns)
    for i in range(len(displacement)):
        df.loc[len(df.index)] = [displacement[i], force[i] * 1e-3, force[i]]
    df.to_excel(f"{filePath}/FD_Curve.xlsx", index=False)
    df.to_csv(f"{filePath}/FD_Curve.csv", index=False)

def replace_flowCurve_material_inp(filePath, truePlasticStrain, trueStress):
    with open(filePath, 'r') as material_inp:
        material_inp_content = material_inp.readlines()
    start_line = None
    end_line = None
    for i, line in enumerate(material_inp_content):
        if '*Plastic' in line:
            start_line = i + 1
        elif '*Density' in line:
            end_line = i
            break

    if start_line is None or end_line is None:
        raise ValueError('Could not find the stress-strain data section')

    new_stress_strain_data = zip(trueStress, truePlasticStrain)
    new_lines = []
    new_lines.extend(material_inp_content[:start_line])
    new_lines.extend([f'{stress},{strain}\n' for stress, strain in new_stress_strain_data])
    new_lines.extend(material_inp_content[end_line:])

    with open(filePath, 'w') as file:
        file.writelines(new_lines)

def replace_maxDisp_geometry_inp(filePath, maxTargetDisplacement):
    with open(filePath, 'r') as geometry_inp:
        geometry_inp_content = geometry_inp.readlines()
    start_line = None
    end_line = None
    for i, line in enumerate(geometry_inp_content[-60:]):
        if line.startswith('*Boundary, amplitude'):
            original_index = len(geometry_inp_content) - 60 + i
            start_line = original_index + 1
            end_line = original_index + 2
            break

    if start_line is None or end_line is None:
        raise ValueError('Could not find the *Boundary, amplitude displacement section')

    new_disp_data = f"Disp, 2, 2, {maxTargetDisplacement}\n"

    new_lines = []
    new_lines.extend(geometry_inp_content[:start_line])
    new_lines.extend([new_disp_data])
    new_lines.extend(geometry_inp_content[end_line:])

    with open(filePath, 'w') as file:
        file.writelines(new_lines)

def replace_materialName_geometry_inp(filePath, materialName):
    with open(filePath, 'r') as geometry_inp:
        geometry_inp_content = geometry_inp.readlines()
    start_line = None
    end_line = None
    for i, line in enumerate(geometry_inp_content[-100:]):
        if line.startswith('*INCLUDE, INPUT='):
            original_index = len(geometry_inp_content) - 100 + i
            start_line = original_index
            end_line = original_index + 1
            break

    if start_line is None or end_line is None:
        raise ValueError('Could not find the *INCLUDE, INPUT= section')

    new_material_data = f"*INCLUDE, INPUT={materialName}\n"

    new_lines = []
    new_lines.extend(geometry_inp_content[:start_line])
    new_lines.extend([new_material_data])
    new_lines.extend(geometry_inp_content[end_line:])

    with open(filePath, 'w') as file:
        file.writelines(new_lines)

def rescale_paramsDict(paramsDict, paramConfig):
    rescaled_paramsDict = {}
    for param, value in paramsDict.items():
        rescaled_paramsDict[param] = value * paramConfig[param]['exponent']
    return rescaled_paramsDict

def reverseAsParamsToGeometries(curves, geometries):
    exampleGeometry = geometries[0]
    reverseCurves = {}
    for paramsTuple in curves[exampleGeometry]:
        reverseCurves[paramsTuple] = {}
        for geometry in geometries:
            reverseCurves[paramsTuple][geometry] = curves[geometry][paramsTuple]
    return reverseCurves

def calculate_yielding_index(targetDisplacement, targetForce, r2_threshold=0.998):
    """
    This function calculates the end of the elastic (linear) region of the force-displacement curve.
    """
    yielding_index = 0

    linReg = LinearRegression()
    targetDisplacement = np.array(targetDisplacement)
    targetForce = np.array(targetForce)
    for i in range(2, len(targetDisplacement)):
        linReg.fit(targetDisplacement[:i].reshape(-1, 1), targetForce[:i]) 
        simForce = linReg.predict(targetDisplacement[:i].reshape(-1, 1)) 
        r2 = r2_score(targetForce[:i], simForce) 
        if r2 < r2_threshold:  
            yielding_index = i - 1
            break
    return yielding_index