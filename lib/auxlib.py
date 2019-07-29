import sympy
import sympy.functions.elementary.exponential as symExp

constant = sympy.symbols('constant')

def get_constant(): return constant

def integrateFunc(func, variable, bounds=None, paramsToSub = {}, conds='none'):
	if bounds == None:
		func_int = sympy.integrate(func.subs(paramsToSub), variable, conds=conds) + constant
	else:
		func_int = sympy.integrate(func.subs(paramsToSub), (variable, bounds[0], bounds[1]))
	return func_int