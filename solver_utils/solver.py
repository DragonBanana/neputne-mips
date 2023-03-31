from ortools.linear_solver import pywraplp
from .data import Data
import datetime

class Solver:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        if verbose:
            self.solver.EnableOutput()
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.objective = self.solver.Objective()
        self.data = None

    def load_input(self, data: Data):
        self.data = data
        self.log("Initializing variables...")
        self.init_vars()
        self.log("Initializing constraints...")
        self.init_constraints()

    def init_vars(self):
        raise NotImplementedError("Solvers must implement init_vars()")
    
    def init_constraints(self):
        raise NotImplementedError("Solvers must implement init_constraints()")
    
    def init_objective(self):
        raise NotImplementedError("Solvers must implement init_objective()")

    def log(self, msg: str):
        if self.verbose:
            print(f"{datetime.datetime.now()}: {msg}")

    def solve(self):
        self.init_objective()
        status = self.solver.Solve()
        self.log(f"Problem solved with status {status}")
        return status == pywraplp.Solver.OPTIMAL

    def results(self):
        raise NotImplementedError("Solvers must implement results()")

    def score(self) -> float:
        return self.objective.Value()