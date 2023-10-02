import pandas as pd
import numpy as np
from prettytable import PrettyTable
from PART1_FOLDERS import *
from ASSETS.PART2_ASSTFUNCT import *
from ASSETS.PART1_HARDENINGLAWS import *

#Users need Abaqus and CSC to use this code. 

#Loading the configurations that encompass the whole programme
def load_settings(): 

     # First, we define a dictionary 'dataDictionary' containing various configuration settings and data. 
     # we will return this dictionary 
    dataDictionary = {
        'projectDirectoryLocation': projectDirectoryLocation,  # Location of the project directory
        'logFileLocation': logFileLocation,  # Location of log files
        'specsDataFolder': specsDataFolder,  # Folder for specifications data
        'outputFileDirectory': outputFileDirectory,  # Directory for output files
        'simulationFileDirectory': simulationFileDirectory,  # Directory for simulation files
        'targetFileDirectory': targetFileDirectory,  # Directory for target files
        'templateFileDirectory': templateFileDirectory,  # Directory for template files
        'optimizationApproach': optimizationApproach,  # Approach used for optimization
        'numInitialSimulations': numInitialSimulations,  # Number of initial simulations
        'specsSetForGeneration': specsSetForGeneration,  # Specifications set for generation
        'initialSimulationSpacing': initialSimulationSpacing,  # Spacing between initial simulations
        'medium': medium,  # Medium or material properties
        'hardeningLaw': hardeningLaw,  # Hardening law used in simulations
        'curveIdentifier': curveIdentifier,  # Identifier for curves
        'algorithmLabel': algorithmLabel,  # Label for the optimization algorithm
        'specsSettings': specsSettings,  # Dictionary containing specifications settings
        'percentageDifference': percentageDifference,  # Percentage difference parameter
        'truePlasticStrain': truePlasticStrain,  # Array containing true plastic strain values
        'SLURMLoopCounter': SLURMLoopCounter  # Counter for SLURM job loops
    }

    # Load general settings from an Excel file
    generalSettings = pd.read_excel("configs/global_config.xlsx", nrows=1, engine="openpyxl")
    generalSettings = generalSettings.T.to_dict()[0]

    # Extract specific settings from the general settings
    optimizationApproach = generalSettings["methodOfOptimization (strategy)"]
    medium = generalSettings["medium (material)"]
    algorithmLabel = generalSettings["algorithmLabel"]
    hardeningLaw = generalSettings["hardeningLaw"]
    percentageDifference = generalSettings["percentageDifference"]
    shapeOfTheObject = generalSettings["shapeOfTheObject"]
    outputIdentifier = generalSettings["outputIdentifier (Yielding Index)"]
    curveIdentifier = generalSettings["curveIdentifier"]
    specsSetForGeneration = generalSettings["numInitialSimulations"]
    numInitialSimulations = generalSettings["initialSimulationCount"]
    initialSimulationSpacing = generalSettings["initialSimulationSpacing"]
    SLURMLoopCounter = generalSettings["SLURMLoopCounter"]

    # Start directory for Single Objective Optimization
    if optimizationApproach == "SOO":
        (
            projectDirectoryLocation, 
            logFileLocation, 
            specsDataFolder, 
            outputFileDirectory, 
            simulationFileDirectory, 
            templateFileDirectory, 
            targetFileDirectory
        ) = startFolder(optimizationApproach, medium, hardeningLaw, shapeOfTheObject, curveIdentifier)

    # Start directory for Multi-Objective Optimization
    elif optimizationApproach == "MOO":
        shapes = shapeOfTheObject.split(",")
        (
            projectDirectoryLocation, 
            logFileLocation, 
            specsDataFolder, 
            outputFileDirectory, 
            simulationFileDirectory, 
            templateFileDirectory, 
            targetFileDirectory
        ) = startFolder(optimizationApproach, medium, hardeningLaw, shapes, curveIdentifier)

    # Extract corresponding indices for MOO
        correspondingIndices = str(outputIdentifier).split(";")
        correspondingIndices = [int(k) for k in correspondingIndices]
        correspondingIndices = dict(zip(shapes, correspondingIndices))
    
    # Read the configuration settings for true plastic strain from an Excel file
    # The 'hardeningLaw' variable is assumed to contain a specific value
    settingsForTruePlasticStrain = pd.read_excel(f"configs/truePlasticStrain_{hardeningLaw}_config.xlsx",engine="openpyxl")

    # Initialize an empty list to store tuples representing strain intervals
    intervalStride = []

    # Iterate through each row in the 'settingsForTruePlasticStrain' DataFrame
    # and extract the start, end, and step values into a list of tuples called 'intervalStride'.
    for itemPosition, row in settingsForTruePlasticStrain.iterrows():
        intervalStride.append((row['strainStart'], row['strainEnd'], row['strainStep']))
    
    # Initialize an empty NumPy array called 'truePlasticStrain'.
    truePlasticStrain = np.array([])

    # Iterate through each tuple (start, end, step) in the 'intervalStride' list.
    for k, (start, end, step) in enumerate(intervalStride):
        if k > 0:
            # Adjust the 'start' value for subsequent intervals
            start += step

        # Create an array of plastic strain values within the current interval
        deformationRange = np.arange(start, end + step, step)

        # Round the values to 6 decimal places
        deformationRange = np.around(deformationRange, decimals=6)

        # Concatenate the generated values to the 'truePlasticStrain' array
        truePlasticStrain = np.concatenate((truePlasticStrain, deformationRange))

    # Save the 'truePlasticStrain' array to a NumPy binary file
    # The filename includes a variable 'hardeningLaw' in the format "truePlasticStrain_{hardeningLaw}.npy"
    np.save(f"configs/truePlasticStrain_{hardeningLaw}.npy", truePlasticStrain)

    # Read an Excel file 'paramInfo.xlsx' from a specific folder using pandas
    specsSettings = pd.read_excel(f"{specsDataFolder}/paramInfo.xlsx", engine="openpyxl")

    # Set the 'parameter' column as the index for the DataFrame
    specsSettings.set_index("parameter", inplace=True)

    # Transpose the DataFrame and convert it into a dictionary of dictionaries
    # Each row becomes a dictionary with column names as keys
    specsSettings = specsSettings.T.to_dict()

    # Iterate through each parameter in the 'specsSettings' dictionary
    for param in specsSettings:
        # Convert the 'exponent' value for each parameter to a floating-point number
        specsSettings[param]['exponent'] = float(specsSettings[param]['exponent'])

    # Depending on the chosen optimization approach ('SOO' or 'MOO'), 
    # update the 'dataDictionary' with specific data related to the approach.
    #     if (optimizationApproach == 'SOO'):
    if optimizationApproach == "SOO":
        # For Single Objective Optimization (SOO), store 'shapeOfTheObject' and 'outputIdentifier'
        dataDictionary['shapeOfTheObject'] = shapeOfTheObject
        dataDictionary['outputIdentifier'] = outputIdentifier

    if optimizationApproach == "MOO":
        # For Multi-Objective Optimization (MOO), store 'shapes' and 'correspondingIndices'
        dataDictionary['shapes'] = shapes
        dataDictionary['correspondingIndices'] = correspondingIndices


    # Print a message indicating the start of Group 3's Abaqus Project to the log file.
    printLog(f"\Here's Group 3's Abaqus Project \n\n", logFileLocation)

    # Print a message displaying the settings to the log file.
    printLog(f"Here's your settings: \n", logFileLocation)

    # Create an instance of PrettyTable for tabular data presentation.
    logTable = PrettyTable()


    # Set the field names (column headers) for the PrettyTable.
    logTable.field_names = ["General Settings", "User choice"]

    # Add rows of data to the PrettyTable.
    logTable.add_row(["SLURM Loop Count", SLURMLoopCounter])
    logTable.add_row(["Quantity of Initial Simulations", numInitialSimulations])
    logTable.add_row(["Optimization Approach", optimizationApproach])
    logTable.add_row(["Medium", medium])
    logTable.add_row(["Hardening law", hardeningLaw])
    logTable.add_row(["Curve Identifier", curveIdentifier])

    # Check the optimization approach and add relevant data accordingly.
    if optimizationApproach == "SOO":
        logTable.add_row(["Shape Of The Object", shapeOfTheObject])

    if optimizationApproach == "MOO":
        # Combine multiple shape descriptions into a single string with commas.
        shapeDescription = ",".join(shapes)
        logTable.add_row(["Shapes", shapeDescription])

    logTable.add_row(["Algorithm Name", algorithmLabel])
    logTable.add_row(["Percentage Difference", percentageDifference])

    # Print a message indicating the creation of directories to the log file.
    printLog("Creating directories\n", logFileLocation)

    # Print a message displaying the location of the project folder to the log file.
    printLog(f"Your project folder is here: \n", logFileLocation)

    # Print the path of the project directory to the log file.
    printLog(f"{projectDirectoryLocation}\n", logFileLocation)

    return dataDictionary
