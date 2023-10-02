from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from sklearn.gaussian_process.kernels import RBF
import os
from ASSETS.PART2_ASSTFUNCT import *

class bayesianOptimization():

    def start(kendi, data):        
        kendi.info = data
        kendi.verbose = 1
        kendi.random_state = 123 
        kendi.init_points = 0
        kendi.iterations = 1 
        kendi.acquisitionFunction = UtilityFunction(kind='POI', xi=0.1)
        kendi.GP_kernel = RBF(length_scale=1, length_scale_bounds=(1e-3, 1e3)) 
        kendi.alpha = 1e-9
        kendi.normalize_y=True
        kendi.n_restarts_optimizer=5
        kendi.logger = JSONLogger(path=f"MODELS/logs.json", reset=False)
    
    def initializeOptimizer(kendi, errorFunction, rangeConstraints, progressStatus = True):
        kendi.param_bounds = rangeConstraints
        kendi.loadingProgress = progressStatus
        optimizationObject = BayesianOptimization(
            f = errorFunction,
            pbounds = rangeConstraints, 
            verbose = kendi.verbose,
            random_state = kendi.random_state,
            bounds_transformer = None,
            allow_duplicate_points = False,
        )
        optimizationObject.set_gp_params(
            kernel=kendi.GP_kernel,
            alpha=kendi.alpha,
            normalize_y=kendi.normalize_y,
            n_restarts_optimizer=kendi.n_restarts_optimizer,
            random_state=kendi.random_state
        )
        kendi.optimizer = optimizationObject
        if progressStatus == False:
            kendi.optimizer.subscribe(Events.OPTIMIZATION_STEP, kendi.logger)
        else:
            pathForProject = kendi.info["pathForProject"]
            pathForLog = kendi.info["pathForLog"]
            if os.path.exists(f"{pathForProject}/MODELS/logs.json"):
                load_logs(kendi.optimizer, logs=[f"MODELS/logs.json"]);
                printLog("BO optimizer is now aware of {} points.".format(len(kendi.optimizer.space)), pathForLog)
                kendi.optimizer.subscribe(Events.OPTIMIZATION_STEP, kendi.logger)
        
        
    def run(self):
        self.optimizer.maximize(
            init_points = self.init_points if self.loadingProgress == False else 0, 
            n_iter = self.iterations,   
            acquisition_function=self.acquisitionFunction
        )
    
    def suggest(self):
        next_point = self.optimizer.suggest(self.acquisitionFunction)
        return next_point
        
    def outputResult(self):
        solution_dict = self.optimizer.max["params"]
        solution_tuple = tuple(solution_dict.items())
        best_solution_loss = self.optimizer.max["target"]
        return solution_dict, solution_tuple, best_solution_loss