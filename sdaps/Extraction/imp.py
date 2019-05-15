import inspect

def fun(var):
    for fi in reversed(inspect.stack()):
            names = [var_name for var_name,
                     var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) == 1:
                return names[0]
            else:
                return names

a = ['hwhw', 34, 'df']

print(fun(a))