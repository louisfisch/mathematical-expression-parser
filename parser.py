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
    'atan2': math.atan2,
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
    'hypot': math.hypot,
    'ldexp': math.ldexp,
    'log': math.log,
    'log10': math.log10,
    'modf': math.modf,
    'pow': math.pow,
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

    def isNext(self, value):
        return self.string[self.index:self.index+len(value)] == value

    def popIfNext(self, value):
        if self.isNext(value):
            self.index += len(value)
            return True
        return False

    def popExpected(self, value):
        if not self.popIfNext(value):
            raise Exception("Expected '" + value + "' at index " + str(self.index))


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

    def parseArguments(self):
        args = []
        self.skipWhitespace()
        self.popExpected('(')
        while not self.popIfNext(')'):
            self.skipWhitespace()
            if len(args) > 0:
                self.popExpected(',')
                self.skipWhitespace()
            args.append(self.parseExpression())
            self.skipWhitespace()
        return args

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
            args = self.parseArguments()
            return float(function(*args))
        
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
