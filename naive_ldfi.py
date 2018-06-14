from ldfi_py.pbool import *
import ldfi_py.pilp
import ldfi_py.psat

class NaiveLDFI():
    def __init__(self):
        self.graphs = []

    def add_graph(self, graph):
        self.graphs.append([graph.label, graph.active_nodeset()])

    def current_formula(self):
        outerset = set()
        for trace in self.graphs:
            labels = filter(lambda x: x != trace[0], map(lambda x: x.label, trace[1]))
            #print "LABELS is " + str(sorted(labels))
            if labels is None:
                print("ONO")
            outerset.add(frozenset(labels))


        conjuncts = None
        for inner in outerset:
            disjunction = None
            for item in inner:
                if disjunction is None:
                    disjunction = Literal(item)
                else:
                    disjunction = OrFormula(Literal(item), disjunction)
            if conjuncts is None:
                conjuncts = disjunction
            else:
                conjuncts = AndFormula(disjunction, conjuncts)

        #print "CONJ " + str(conjuncts)
        return conjuncts

    def suggestions(self):
        formula = self.current_formula()
        #print("Create a formula %s" % str(formula))
        cnf = CNFFormula(formula)
        #print("CNF %s" %str(cnf) )

        #print( "clauses " + str(len(cnf.conjuncts())) )

        s = ldfi_py.pilp.Solver(cnf)
        #s = ldfi_py.psat.Solver(cnf)
        
        crs = s.solutions()
        '''
        while True:
            try:
                sol = next(crs)
                print( "ESS " + str(list(sol)) )
            except StopIteration:
                break
        '''

        return crs

#class NaiveLDFIWrapper():

