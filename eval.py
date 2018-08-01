import math
from parser import Parser

def evaluate(expression, vars = None):
    try:
        p = Parser(expression, vars)
        value = p.getValue()
    except Exception as (ex):
        msg = ex.message
        raise Exception(msg)

    # Return an integer type if the answer is an integer 
    if int(value) == value:
        return int(value)

    # If Python made some silly precision error like x.99999999999996, just return x+1 as an integer 
    epsilon = 0.0000000001
    if int(value + epsilon) != int(value):
        return int(value + epsilon)
    if int(value - epsilon) != int(value):
        return int(value)
    return value

if __name__ == "__main__":
    print evaluate("cos(x+4*3) + 2 * 3", { 'x': 5  })
    print evaluate("exp(0)")
    print evaluate("-(1 + 2) * 3")
    print evaluate("(1-2)/3.0 + 0.0000")
    print evaluate("abs(-2) + pi / 4")
    print evaluate("(x + e * 10) / 10", { 'x' : 3 })
    print evaluate("1.0 / 3 * 6")
    print evaluate("(1 - 1 + -1) * pi")
    print evaluate("cos(pi) * 1")
    print evaluate("atan2(2, 1)")
    print evaluate("hypot(5, 12)")
    print evaluate("pow(3, 5)")
