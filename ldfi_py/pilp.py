from . import pbool
from pulp import *


class SATVars:
    def __init__(self):
        self.name2var = {}
        self.var2name = {}

    def lookupName(self, name):
        if name not in self.name2var:
            lpv = LpVariable(name, 0, 1, "Integer")
            #print "LPV " + str(lpv)
            self.name2var[name] = lpv
            self.var2name[lpv] = name
            
        return self.name2var[name]

    def lookupVar(self, var):
        return self.var2name[var]
    
    def allVars(self):
        for key in self.var2name:
            yield key

class Solver:
    def __init__(self, cnf):
        #cnf = pbool.CNFFormula(formula)
        self.problem = LpProblem("LDFI", LpMinimize)

        self.vars = SATVars()
        self.satformula = []
        for clause in cnf.conjuncts():
            satclause = list(map(self.vars.lookupName, clause))
            #print( "SATCLAUSE " + str(list(satclause)) )
            self.satformula.append(list(satclause))
            constraint = sum(satclause) >= 1
            self.problem += constraint

        self.problem += sum( list(self.vars.allVars()) )
        #print(self.problem)

    def solutions(self):
        def unVar(var):
            if value(var) == 1.0:
                return var
            else:
                return 1 - var

        while True: 
            status = self.problem.solve()
            #print "STATUS " + str(LpStatus[status])
            if status != 1:
                return
            ret = filter(lambda x: value(x) == 1.0, self.vars.allVars())
            newsum = sum(map(unVar, self.vars.allVars()))
            yield ret
            self.problem += (newsum <= len(list(self.vars.allVars())) - 1)

