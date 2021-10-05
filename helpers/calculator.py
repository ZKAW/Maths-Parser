# Expression calculator

import operator

from . import handler as exc

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
}

def split_expr(expression):
    SYMBOLS = ['+', '-', '*', '/', '(', ')']
    splited_expr = []
    pos = 0
    while pos < len(expression):
        char = expression[pos]

        if char == ' ': pass # Ignore white spaces
        elif char in SYMBOLS: # If char is a symbol
            splited_expr.append(char)
        elif char.isdigit(): # If char is a number
            num = float(char)
            while pos + 1 < len(expression) and expression[pos + 1].isdigit(): # Get entire number instead of single digit 
                pos += 1
                num = num * 10 + float(expression[pos]) # Extand number ten until entire number is present
                # Ex: 125 = 1*10 -> +2 -> 12 -> 2*10 -> +5 -> 125
            splited_expr.append(num)
        else: # Unknown operand, raise error
            return exc.raiseTypeError(command=expression, error=f"'{expression[pos]}' is not a valid operand")

        pos += 1
    return splited_expr

def evaluate(expression, i):
    n1 = expression[i-1] # Get element before symbol
    n2 = expression[i+1] # Get element after symbol
    res =  int(ops[expression[i]](n1,n2)) # Result of the operation

    # Replace operation by result of the operation
    expression[i] = res 
    expression.pop(i-1)
    expression.pop(i)
    return expression

def reduce(expression):
    # Calculate everything in the expression, and replace it by the result
    expression = calc_parentheses(expression)
    splited_expr = split_expr(expression)
    reduced_expr = calc_priority(splited_expr)
    final = calc_secondary(reduced_expr)
    result = ''.join([str(int) for int in final])
    return result

def calc_parentheses(expression):
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    center_expr = expression[ expression.rfind('(')+1 : expression.find(')') ] 

    # Replace calculated parentheses by result
    expression = expression.replace(f'({center_expr})', reduce(center_expr))
    return calc_parentheses(expression)

def calc_priority(expression, i=0):
    if '*' not in expression and '/' not in expression: return expression

    if expression[i] == '*' or expression[i] == '/':
        evaluate(expression, i)
        i = 0
    return calc_priority(expression, i+1)

def calc_secondary(expression, i=0):
    if '+' not in expression: return expression

    if expression[i] == '+':
        evaluate(expression, i)
        i = 0
    return calc_secondary(expression, i+1)

def calc(expression):
    if len(expression) == 1: return expression[0]

    # Calculate expression and return result
    return reduce(expression)