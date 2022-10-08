# When we decorate a function with a class, the function is automatically
#  passed as the first argument to the init constructor. We set this function
#   as an attribute in our object. If we print multiply_together now, we can
#    see it is an instance of the Power class.

class Power(object):
    def __init__(self,func):
        self._func = func

    def __call__(self,a,b):
        retval = self._func(a,b)
        return retval**2
    
    def __str__(self):
        return "a new func name"

@Power
def mul(a,b):
    return a*b

print(mul(2,2))
print(mul)

class Power2(object):
    def __init__(self,arg):
        self._arg = arg
        print(f"power2 get value {arg}")

    def __call__(self,*param_arg):
        if len(param_arg) == 1:
            #如果给Power2传递过参数，__call__里面才会把func对象作为参数传递进来
            def wrapper(a,b):
                return param_arg[0](a,b)**self._arg
            return wrapper
        else:
            #如果没有给Power2传递过参数，__init__中就把func对象传递进来了
            retval = self._arg(param_arg[0],param_arg[1])
            return retval**2
    
    def __str__(self):
        return "a new func name"

@Power2(3) # 如果这里传递了参数，那么power的__init__时就只会得到这个参数，不会得到func
def mul2(a,b):
    return a*b

print(mul2(2,2))
print(mul)