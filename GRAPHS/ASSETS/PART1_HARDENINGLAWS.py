import numpy as np

################################
##                            ##
##                            ##
##       HARDENING LAWS       ##
##                            ##
##                            ##
################################

################################
##                            ##
##           SWIFT            ##
##                            ##
################################

# This function calculates true stress based on the Swift law formula.
# It takes three input parameters: spec1, spec2, and spec3, as well as truePlasticStrain.
def swiftLaw(spec1, spec2, spec3, truePlasticStrain):
    # Calculate true stress using the Swift law formula:
    # True Stress = spec1 * (spec2 + truePlasticStrain) ** spec3
    trueStress = spec1 * (spec2 + truePlasticStrain) ** spec3
    
    # Return the calculated true stress value.
    return trueStress


################################
##                            ##
##            VOCE            ##
##                            ##
################################

# This function calculates true stress based on the Voce law formula.
# It takes four input parameters: spec1, spec2, spec3, and truePlasticStrain.
def voceLaw(spec1, spec2, spec3, truePlasticStrain):
    # Calculate true stress using the Voce law formula:
    # True Stress = spec1 + spec2 * (1 - exp(-spec3 * truePlasticStrain))
    
    # Calculate the exponential term within the formula.
    exponential_term = -spec3 * truePlasticStrain
    exp_result = np.exp(exponential_term)
    
    # Calculate the final true stress using the Voce law formula.
    trueStress = spec1 + spec2 * (1 - exp_result)
    
    # Return the calculated true stress value.
    return trueStress

################################
##                            ##
##       SWIFT-VOCE LAW       ##
##                            ##
################################

# This function calculates true stress based on a combination of Swift and Voce laws.
# It takes eight input parameters: spec1 through spec7, and truePlasticStrain.
def swiftAndVoceLaw(spec1, spec2, spec3, spec4, spec5, spec6, spec7, truePlasticStrain):
    # Calculate true stress using the Swift law formula.
    trueStressSwift = swiftLaw(spec2, spec3, spec4, truePlasticStrain)
    
    # Calculate true stress using the Voce law formula.
    trueStressVoce = voceLaw(spec5, spec6, spec7, truePlasticStrain)
    
    # Calculate the combined true stress using a weighted average of Swift and Voce stresses:
    # True Stress = spec1 * trueStressSwift + (1 - spec1) * trueStressVoce
    
    # Weighted average of the two stress components with weight spec1.
    weighted_trueStressSwift = spec1 * trueStressSwift
    
    # Weighted average of the two stress components with weight (1 - spec1).
    weighted_trueStressVoce = (1 - spec1) * trueStressVoce
    
    # Calculate the final true stress by combining the two components.
    trueStress = weighted_trueStressSwift + weighted_trueStressVoce
    
    # Return the calculated true stress value.
    return trueStress

################################
##                            ##
##         FLOWCURVE          ##
##                            ##
################################

# This function calculates the true stress based on a specified hardening law.
# It takes three input parameters: parameters (a dictionary of hardening law parameters),
# hardeningLaw (a string specifying the type of hardening law), and truePlasticStrain.

def findFlowCurve(parameters, hardeningLaw, truePlasticStrain):
    # Check which hardening law is specified and calculate the true stress accordingly.
    if hardeningLaw == "Swift":
        # Extract Swift law parameters from the dictionary.
        spec1, spec2, spec3 = parameters["spec1"], parameters["spec2"], parameters["spec3"]
        
        # Calculate true stress using the Swift law formula.
        trueStress = swiftLaw(spec1, spec2, spec3, truePlasticStrain)
    elif hardeningLaw == "Voce":
        # Extract Voce law parameters from the dictionary.
        spec1, spec2, spec3 = parameters["spec1"], parameters["spec2"], parameters["spec3"]
        
        # Calculate true stress using the Voce law formula.
        trueStress = voceLaw(spec1, spec2, spec3, truePlasticStrain)
    elif hardeningLaw == "SwiftVoce":
        # Extract Swift and Voce law parameters from the dictionary.
        spec1, spec2, spec3, spec4, spec5, spec6, spec7 = parameters["spec1"], parameters["spec2"], parameters["spec3"], parameters["spec4"], parameters["spec5"], parameters["spec6"], parameters["spec7"]
        
        # Calculate true stress using a combination of Swift and Voce laws.
        trueStress = swiftAndVoceLaw(spec1, spec2, spec3, spec4, spec5, spec6, spec7, truePlasticStrain)
    
    # Return the calculated true stress value based on the specified hardening law.
    return trueStress