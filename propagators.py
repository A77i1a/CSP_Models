# =============================
# Student Names: Justin Woo, Attila Tavakolli, Matthew Woo
def prop_BT(csp, newVar=None):
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    prune = []
    con = []

    if not newVar: #When newVar is not instantiated
        con = csp.get_all_nary_cons(1)
        for c in con: #Retrieve all constraints that include only one variable
            if c.get_n_unasgn() == 1:
                var = c.get_unasgn_vars()
                for val in var[0].cur_domain():
                    if not c.check_var_val(val,var[0]): #Loop through domain of var, if any value does not satisfy
                        prune.append((var[0],val))      #constraints then prune them
                        var[0].prune_value(val)
                    if var[0].cur_domain() == 0: #Empty domain means no satisfying tuple so return false
                        return False, prune
        return True, prune

    #When newVar is instantiated
    con = csp.get_cons_with_var(newVar) #Retrieve all constraints that include newVar
    for c in con:
        for var in c.get_unasgn_vars(): #Check any unassigned variables in the constraint
            for val in var.cur_domain(): #If a value in the domain does not satisfy constraint
                if not c.check_var_val(var,val): #then prune them
                    prune.append((var,val))
                    var.prune_value(val)
            if var.cur_domain_size() == 0:
                return False, prune
    return True, prune        

def prop_GAC(csp, newVar=None):
    pruned = []
    queue = []
    #Initialize queue based on what newVar equals
    if not newVar: #newVar = None
        startCons = csp.get_all_cons()
    else:
        startCons = csp.get_cons_with_var(newVar)
    
    for x in startCons: #Set up hyper arcs
        for var in x.get_scope():
            queue.append((var,x))
    
    while len(queue) != 0:
        con = queue.pop(0) #con equals constraint in current hyper arc
        var = con[0] #var in the con
        removed = False
        for x in var.cur_domain():
            if not con[1].check_var_val(var,x): #Check if domain value is valid, if not then prune
                removed = True
                pruned.append((var,x)) 
                var.prune_value(x)
        
        if removed: #If a value was removed then check neighbours
            for x in csp.get_cons_with_var(var):
                for k in x.get_scope(): #If tuple not already in queue and not assigned then add them
                    if ((k,x) not in queue) and (k != var) and not k.is_assigned():
                        queue.append((k,x)) #Add hyper arc to queue
    return csp, pruned


