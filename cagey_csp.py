from cspbase import *
import itertools
from math import prod

def binary_ne_grid(cagey_grid):
    var_array = [] #List to hold all the variables of the grid
    n = cagey_grid[0] #Dimension of the grid
    dom = [i for i in range(1, n + 1)] #Domain of the variables
    sat_tuples = [[o, x] for (o, x) in itertools.permutations(range(1, n+1), 2)] #Satisfiable tuples of the binary constraints
    #Getting all possible variable cells
    arr = itertools.product(dom, dom)
    var_array = [Variable("Cell({},{})".format(x,y), dom) for (x,y) in arr]
    csp = CSP("binary_cagey", var_array)
    for i in range(n):
        #Create the binary constraints
        rowc = var_array[i * n : (i+1) * n]
        colc = [var_array[j] for j in range(i, n*n, n)]
        for (o, x) in itertools.combinations(rowc, 2):
            con = Constraint("C({},{})".format(o, x), [o, x])
            con.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(con)
        for (o, x) in itertools.combinations(colc, 2):
            con = Constraint("C({},{})".format(o, x), [o, x])
            con.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(con)

    return csp, var_array


def nary_ad_grid(cagey_grid):
    var_array = [] #List to hold all the variables of the grid
    n = cagey_grid[0] #Dimension of the grid
    dom = [i for i in range(1, n + 1)] #Domain of the variables
    sat_tuples = [x for x in itertools.permutations(range(1, n+1), n)]
    arr = itertools.product(dom, dom)
    var_array = [Variable("Cell({},{})".format(x,y), dom) for (x,y) in arr]
    csp = CSP("nary_cagey", var_array)
    for i in range(n):
        rowc = var_array[i * n : (i+1) * n]
        colc = [var_array[j] for j in range(i, n*n, n)]
        for x in itertools.combinations(rowc, n):
            con = Constraint("C({})".format(x), x)
            con.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(con)
        for x in itertools.combinations(colc, n):
            con = Constraint("C({})".format(x), x)
            con.add_satisfying_tuples(sat_tuples)
            csp.add_constraint(con)

    return csp, var_array

def cagey_csp_model(cagey_grid):
    csp, var_array = binary_ne_grid(cagey_grid)
    # Dimension of the board
    n = cagey_grid[0]
    for cage in cagey_grid[1]:
        # Amount of cells in cage
        cagesize = len(cage[1])
        sat_vals = []
        scope = [var_array[(n * (y-1)) + (x-1)] for (y, x) in cage[1]]
        opVar = Variable("Cage_op(" + str(cage[0]) + ":" + cage[2] + ":" + str(scope) + ")", ['+','-','*','/','?'])
        con = Constraint("Cage(" + str(cage[0]) + ":" + cage[2] + ":" + str(scope) + ")", [opVar] + scope)
        var_array.append(opVar)
        # Create satisfiable tuples for constraint
        if cagesize == 1:
            sat_vals = [[cage[2]] + list(x) for x in itertools.product(scope[0].domain(),repeat=cagesize)]
        else:
            if cage[2] == "+" or cage[2] == "?":
                sat_vals = [["+"] + list(x) for x in itertools.product(scope[0].domain(),repeat=cagesize) if sum(x) == cage[0]]
                con.add_satisfying_tuples(sat_vals)
            if cage[2] == "*" or cage[2] == "?":
                sat_vals = [["*"] + list(x) for x in itertools.product(scope[0].domain(),repeat=cagesize) if prod(x) == cage[0]]
                con.add_satisfying_tuples(sat_vals)
            if cage[2] == "-" or cage[2] == "?":
                sat_vals = [["-"] + list(x) for x in itertools.product(scope[0].domain(),repeat=cagesize) if x[0] - sum(x[1:]) == cage[0]]
                con.add_satisfying_tuples(sat_vals)
            if cage[2] == "/" or cage[2] == "?":
                sat_vals = [["/"] + list(x) for x in itertools.product(scope[0].domain(),repeat=cagesize) if x[0] / prod(x[1:]) == cage[0]]
                con.add_satisfying_tuples(sat_vals)
        
        csp.add_var(opVar)
        csp.add_constraint(con)
    return (csp, var_array)
