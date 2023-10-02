from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from sklearn.gaussian_process.kernels import RBF
import os
from modules.helper import *

class bayesianOptimization():

    def start(kendi, data):        
        kendi.info = data
        kendi.verbose = 1
        kendi.random_state = 123 
        kendi.init_points = 0
        kendi.iterations = 1 
        kendi.acquisitionFunction = UtilityFunction(kind='poi', xi=0.1)
        kendi.GP_kernel = RBF(length_scale=1, length_scale_bounds=(1e-3, 1e3)) 
        kendi.alpha = 1e-9
        kendi.normalize_y=True
        kendi.n_restarts_optimizer=5
        kendi.logger = JSONLogger(path=f"optimizers/logs.json", reset=False)
    
    def initializeOptimizer(self, lossFunction, param_bounds, loadingProgress = True):
        self.param_bounds = param_bounds
        self.loadingProgress = loadingProgress
        bo_instance = BayesianOptimization(
            f = lossFunction,
            pbounds = param_bounds, 
            verbose = self.verbose,
            random_state = self.random_state,
            bounds_transformer = None,
            allow_duplicate_points = False,
        )
        bo_instance.set_gp_params(
            kernel=self.GP_kernel,
            alpha=self.alpha,
            normalize_y=self.normalize_y,
            n_restarts_optimizer=self.n_restarts_optimizer,
            random_state=self.random_state
        )
        self.optimizer = bo_instance
        if loadingProgress == False:
            self.optimizer.subscribe(Events.OPTIMIZATION_STEP, self.logger)
        else:
            projectPath = self.info["projectPath"]
            logPath = self.info["logPath"]
            if os.path.exists(f"{projectPath}/optimizers/logs.json"):
                load_logs(self.optimizer, logs=[f"optimizers/logs.json"]);
                printLog("BO optimizer is now aware of {} points.".format(len(self.optimizer.space)), logPath)
                self.optimizer.subscribe(Events.OPTIMIZATION_STEP, self.logger)
        
        
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