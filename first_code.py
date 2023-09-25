import numpy as np

# Specify the path to the folder containing the .npy files
folder_path = "data for training/(hardening para.) initial guesses/(hardening para.) inital guesses before smoothing"

# List of filenames to import
file_names = [
    "CHD6_FD_Curves_unsmooth (1).npy",
    "NDBR6_FD_Curves_unsmooth.npy",
    "NDBR20_FD_Curves_unsmooth.npy",
    "NDBR50_FD_Curves_unsmooth.npy"
]

# Create an empty list to store the loaded data
loaded_data_1 = []

# Specify the path to the folder containing the .npy files
folder_path = "data for training/(hardening para.) initial guesses/"

# List of filenames to import
file_names = [
    "CHD6_FD_Curves_smooth.npy"
    "CHD6_FD_Curves_unsmooth.npy"
    "CHD6_flowCurves.npy"
    "NDBR6_FD_Curves_smooth.npy"
    "NDBR6_flowCurves.npy"
    "NDBR20_FD_Curves_smooth.npy"
    "NDBR20_flowCurves.npy"
    "NDBR50_FD_Curves_smooth.npy"
    "NDBR50_flowCurves.npy"
]

loaded_data_2 = []

#Define the Material Model: Create a function or class that defines your material model, including the hardening 
#parameters that you want to calibrate. For example, if you're using a power-law hardening model:

def power_law_hardening(S0, n, E):
    return S0 * (1 + n * E)

#Define the Objective Function: Create an objective function that calculates the difference between the experimental 
#data and the model predictions for a given set of hardening parameters. You can use a least-squares error as your objective function:

def objective_function(params, E, S_exp):
    S_pred = power_law_hardening(*params, E)
    return np.sum((S_pred - S_exp) ** 2)

