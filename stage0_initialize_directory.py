import os
import pandas as pd


    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    ##### VERIFY AND BUILD FUNCTION #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

def verifyAndBuild(path):
    """
    Creates a directory at the specified 'path' if it does not already exist.

    Args:
        path (str): The path where the directory should be created.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)

    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####   START FOLDER FUNCTION   #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################


def startFolder(optimizationApproach, medium, hardeningLaw, shapeOfTheObject, curveIdentifier):
    """
    Activate a folder structure based on optimization parameters.

    Args:
        optimization_approach (str): The optimization approach ('SOO' or other).
        medium (str): The medium type.
        hardening_law (str): The hardening law used.
        shape_of_the_object (str): The shape of the object.
        curve_identifier (int): The curve identifier.
    """

    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####          FOR SOO          #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

    if optimizationApproach == "SOO":
        # Define a directory for logs
        startFolder("log")
        
        # Define a path for parameter information
        path = f"SOO_paramInfo/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"
        startFolder(path)

        # Define a path for results
        path = f"SOO_results/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"
        startFolder(path)

        # Define subdirectories within the results folder
        startFolder(f"{path}/initial")
        startFolder(f"{path}/initial/data")
        startFolder(f"{path}/initial/common")
        startFolder(f"{path}/iteration")
        startFolder(f"{path}/iteration/data")
        startFolder(f"{path}/iteration/common")

        # Define a path for simulations
        path = f"SOO_simulations/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"
        startFolder(path)

        # Define subdirectories within the simulations folder
        startFolder(f"{path}/initial")
        startFolder(f"{path}/iteration")

        # Define a path for targets
        path = f"SOO_targets/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"
        startFolder(path)

        # Define a path for templates
        path = f"templates/{medium}"
        startFolder(path)
        startFolder(f"{path}/{shapeOfTheObject}")

    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####          FOR MOO          #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

    elif optimizationApproach == "MOO":
        # Define the list of geometries for Multi-Objective Optimization (MOO)
        geometries = shapeOfTheObject

        # Define a directory for logs
        startFolder("log")

        # Define a path for parameter information
        path = f"MOO_paramInfo/{medium}_{hardeningLaw}_curve{curveIdentifier}"
        startFolder(path)
        
        # Define a path for results
        path = f"MOO_results/{medium}_{hardeningLaw}_curve{curveIdentifier}"
        startFolder(path)

        # Define subdirectories within the results folder for each geometry
        for shapeOfTheObject in geometries:
            startFolder(f"{path}/{shapeOfTheObject}")
            startFolder(f"{path}/{shapeOfTheObject}/initial")
            startFolder(f"{path}/{shapeOfTheObject}/initial/data")
            startFolder(f"{path}/{shapeOfTheObject}/initial/common")
            startFolder(f"{path}/{shapeOfTheObject}/iteration")
            startFolder(f"{path}/{shapeOfTheObject}/iteration/data")
            startFolder(f"{path}/{shapeOfTheObject}/iteration/common")

        # Define a path for simulations
        path = f"MOO_simulations/{medium}_{hardeningLaw}_curve{curveIdentifier}"
        startFolder(path)

        # Create subdirectories within the simulations folder for each geometry
        for shapeOfTheObject in geometries:
            startFolder(f"{path}/{shapeOfTheObject}")
            startFolder(f"{path}/{shapeOfTheObject}/initial")
            startFolder(f"{path}/{shapeOfTheObject}/iteration")

        # Define a path for targets
        path = f"MOO_targets/{medium}_{hardeningLaw}_curve{curveIdentifier}"
        startFolder(path)

        # Create subdirectories within the targets folder for each geometry
        for shapeOfTheObject in geometries:
            startFolder(f"{path}/{shapeOfTheObject}")

        # Define a path for templates
        path = f"templates/{medium}"
        startFolder(path)

        # Create subdirectories within the templates folder for each geometry
        for shapeOfTheObject in geometries:
            startFolder(f"{path}/{shapeOfTheObject}")

    locateProject = os.getcwd()
    
    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####          FOR SOO          #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

    if optimizationApproach == "SOO":

        # Path to store log data
        logPath = f"log/SOO_{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}.txt"

        # Path for storing parameter information related to the optimization
        paramInfoPath = f"SOO_paramInfo/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"

        # Path to store the results of the optimization process
        resultPath = f"SOO_results/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"

        # Path to store simulation data generated during optimization
        simPath = f"SOO_simulations/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"

        # Path to store target data used in the optimization
        targetPath = f"SOO_targets/{medium}_{hardeningLaw}_{shapeOfTheObject}_curve{curveIdentifier}"

        # Path to templates that assist in the optimization process, specific to the medium and object shape
        templatePath = f"templates/{medium}/{shapeOfTheObject}"
    
    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####          FOR MOO          #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

    elif optimizationApproach == "MOO":

        # Path to store log data
        logPath = f"log/MOO_{medium}_{hardeningLaw}_curve{curveIdentifier}.txt"

        # Path for storing parameter information related to the optimization
        paramInfoPath = f"MOO_paramInfo/{medium}_{hardeningLaw}_curve{curveIdentifier}"

        # Path to store the results of the optimization process
        resultPath = f"MOO_results/{medium}_{hardeningLaw}_curve{curveIdentifier}"

         # Path to store simulation data generated during optimization
        simPath = f"MOO_simulations/{medium}_{hardeningLaw}_curve{curveIdentifier}"

        # Path to store target data used in the optimization
        targetPath = f"MOO_targets/{medium}_{hardeningLaw}_curve{curveIdentifier}"

        # Path to templates that assist in the optimization process, specific to the medium and object shape
        templatePath = f"templates/{medium}"

    return locateProject, logPath, paramInfoPath, resultPath, simPath, templatePath, targetPath


    #####################################
    #####                           #####
    #####                           #####
    #####                           #####
    #####   READING, EXTRACTING,    #####
    #####    CREATINGFILES AND      #####
    #####        DIRECTORIES        #####
    #####                           #####
    #####                           #####
    #####                           #####
    #####################################

if __name__ == "__main__":

    # Read general settings from a configuration file
    generalSettings = pd.read_excel("configs/global_config.xlsx", nrows=1, engine="openpyxl")
    generalSettings = generalSettings.T.to_dict()[0]

    # Extract relevant settings
    optimizationApproach = generalSettings["optimizationApproach"]
    medium = generalSettings["medium (material)"]
    algorithmLabel = generalSettings["algorithmLabel"]
    hardeningLaw = generalSettings["hardeningLaw"]
    percentageDifference = generalSettings["percentageDifference"]
    shapeOfTheObject = generalSettings["shapeOfTheObject"]
    curveIdentifier = generalSettings["curveIdentifier"]
    numInitialSimulations = generalSettings["numInitialSimulations"]
    initialSimulationSpacing = generalSettings["initialSimulationSpacing"]

    # Based on the chosen optimization approach, create appropriate directories
    if optimizationApproach == "SOO":
        # Create directories for Single Objective Optimization (SOO)
        startFolder(optimizationApproach, medium, hardeningLaw, shapeOfTheObject, curveIdentifier)
        
    elif optimizationApproach == "MOO":
        # Split geometries if it's a Multi-Objective Optimization (MOO) scenario    
        geometries = shapeOfTheObject.split(",")

        # Create directories for Multi-Objective Optimization (MOO)
        startFolder(optimizationApproach, medium, hardeningLaw, geometries, curveIdentifier)