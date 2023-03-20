def ord_dh(csp):
    vars = csp.get_all_unasgn_vars()
    big = (vars[0], 0)
    for var in vars:
        cons = csp.get_cons_with_var(var)
        num = 0
        for con in cons:
        #Greater than 1 as there must be another unassigned var in constraint beside current var
            if con.get_n_unasgn() > 1:
                num += 1
        if num > big[1]:
            big = (var, num)
    return big[0]

def ord_mrv(csp):
    ordList = csp.get_all_unasgn_vars()
    next = ordList[0]
    for var in ordList:
        if len(var.cur_domain()) < len(next.cur_domain()):
            next = var
    return next
