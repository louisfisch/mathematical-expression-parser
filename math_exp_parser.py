import math


_CONSTANTS = {
    'pi' : math.pi,
    'e' : math.e,
    'phi': (1 + 5 ** .5) / 2
}

_FUNCTIONS = {
    'abs': abs,
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
#   'atan2': math.atan2 - Not supported yet. Use `atan(x/y)`
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
#   'hypot': math.hypot, - Not supported yet. Use `sqrt(x*x + y*y)`
    'ldexp': math.ldexp,
    'log': math.log,
    'log10': math.log10,
    'modf': math.modf,
#   'pow': math.pow, - Not supported yet. Use `x**y`
    'radians': math.radians,
    'sin': math.sin,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh
}

class Parser:
    def __init__(self, string, vars = None):
        self.string = string
        self.index = 0
        self.vars = {} if vars == None else vars.copy()
        for constant in _CONSTANTS.keys():
            if self.vars.get(constant) != None:
                raise Exception("Cannot redefine the value of " + var)

    def getValue(self):
        value = self.parseExpression()
        self.skipWhitespace()
        
        if self.hasNext():
            raise Exception(
                "Unexpected character found: '" + self.peek() + "' at index " + str(self.index)
            )
        return value

    def peek(self):
        return self.string[self.index:self.index + 1]

    def hasNext(self):
        return self.index < len(self.string)

    def skipWhitespace(self):
        while self.hasNext():
            if self.peek() in ' \t\n\r':
                self.index += 1
            else:
                return

    def parseExpression(self):
        return self.parseAddition()
    
    def parseAddition(self):
        values = [self.parseMultiplication()]
        
        while True:
            self.skipWhitespace()
            char = self.peek()
            
            if char == '+':
                self.index += 1
                values.append(self.parseMultiplication())
            elif char == '-':
                self.index += 1
                values.append(-1 * self.parseMultiplication())
            else:
                break
        
        return sum(values)

    def parseMultiplication(self):
        values = [self.parseParenthesis()]
            
        while True:
            self.skipWhitespace()
            char = self.peek()
                
            if char == '*':
                self.index += 1
                values.append(self.parseParenthesis())
            elif char == '/':
                div_index = self.index
                self.index += 1
                denominator = self.parseParenthesis()
                     
                if denominator == 0:
                    raise Exception(
                        "Division by 0 kills baby whales (occured at index " + str(div_index) + ")"
                    )
                values.append(1.0 / denominator)
            else:
                break
                     
        value = 1.0
        
        for factor in values:
            value *= factor
        return value

    def parseParenthesis(self):
        self.skipWhitespace()
        char = self.peek()
        
        if char == '(':
            self.index += 1
            value = self.parseExpression()
            self.skipWhitespace()
            
            if self.peek() != ')':
                raise Exception(
                    "No closing parenthesis found at character " + str(self.index)
                )
            self.index += 1
            return value
        else:
            return self.parseNegative()

    def parseNegative(self):
        self.skipWhitespace()
        char = self.peek()
        
        if char == '-':
            self.index += 1
            return -1 * self.parseParenthesis()
        else:
            return self.parseValue()

    def parseValue(self):
        self.skipWhitespace()
        char = self.peek()
        
        if char in '0123456789.':
            return self.parseNumber()
        else:
            return self.parseVariable()
 
    def parseVariable(self):
        self.skipWhitespace()
        var = []
        while self.hasNext():
            char = self.peek()
            
            if char.lower() in '_abcdefghijklmnopqrstuvwxyz0123456789':
                var.append(char)
                self.index += 1
            else:
                break
        var = ''.join(var)
        
        function = _FUNCTIONS.get(var.lower())
        if function != None:
            arg = self.parseParenthesis()
            return float(function(arg))
        
        constant = _CONSTANTS.get(var.lower())
        if constant != None:
            return constant

        value = self.vars.get(var, None)
        if value != None:
            return float(value)
            
        raise Exception("Unrecognized variable: '" + var + "'")

    def parseNumber(self):
        self.skipWhitespace()
        strValue = ''
        decimal_found = False
        char = ''

        while self.hasNext():
            char = self.peek()            
            
            if char == '.':
                if decimal_found:
                    raise Exception(
                        "Found an extra period in a number at character " + str(self.index) + ". Are you European?"
                    )
                decimal_found = True
                strValue += '.'
            elif char in '0123456789':
                strValue += char
            else:
                break
            self.index += 1

        if len(strValue) == 0:
            if char == '':
                raise Exception("Unexpected end found")
            else:
                raise Exception(
                    "I was expecting to find a number at character " + str(self.index) + " but instead I found a '" + char + "'. What's up with that?")

        return float(strValue)

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

    # If Python made some silly precision error 
    # like x.99999999999996, just return x+1 as an integer 
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
