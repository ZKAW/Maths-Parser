# Expression calculator

import operator # Allow final calculation without multiple "if" condition
import re

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
}

NUMBERS = [str(n) for n in list(range(0,10))]
SYMBOLS = ['+', '-', '*', '/']
PARENTHESES = ['(', ')']

def split_expr(expression):
    splited_expr = re.split("([+-/*])", expression.replace(" ", "")) # Match mathematical regular expression
    if '' in splited_expr:
        raise SyntaxError("Invalid syntax for operator")

    if not any(x in expression for x in NUMBERS):
        raise ValueError("The expression must contain at least one number")
            
    for i in range(len(splited_expr)):
        if splited_expr[i] not in SYMBOLS+PARENTHESES: # If character is not a symbol
            try: splited_expr[i] = int(splited_expr[i])
            except: raise ValueError(f"Invalid character in expression: '{splited_expr[i]}'") # If character is not a number

    return splited_expr

def evaluate(expression, i):
    n1 = expression[i-1] # Get element before symbol
    symbol = expression[i] # Get the operator
    n2 = expression[i+1] # Get element after symbol
    res = int(ops[symbol](n1,n2)) # Result of the operation

    # Replace expression by result of the operation
    expression[i] = res 
    expression.pop(i-1)
    expression.pop(i)
    return expression

def reduce(expression):
    # Calculate the expression, with priority order 
    if expression.count('(') != expression.count(')'): raise SyntaxError("The brackets have never been opened or closed")

    expression = calc_parentheses(expression)
    res = calc_by_priority(split_expr(expression), priority=1) # Calculate priority first (*,/) then secondary (+,-)
    return ''.join([str(int) for int in res])

def calc_parentheses(expression):
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    center_expr = expression[ expression.rfind('(')+1 : expression.find(')') ]
    after_expr = expression.find(')')+1
    before_expr = expression.rfind('(')-1

    if after_expr < len(expression): # Verify if end of the expression reached
        if expression[after_expr] not in SYMBOLS+[')']:
            raise SyntaxError("Only symbols should be put after a parenthesis")
    
    if before_expr != -1: # Verify if start of the expression reached
        if expression[before_expr] not in SYMBOLS+['(']:
            raise SyntaxError("Only symbols should be put before a parenthesis")

    # Replace calculated parentheses by result
    expression = expression.replace(f'({center_expr})', reduce(center_expr))
    return calc_parentheses(expression)

def calc_by_priority(expression, i=0, priority=1): # Calc * /
    if '*' not in expression and '/' not in expression and priority==1: return calc_by_priority(expression, i=0, priority=2)
    elif '+' not in expression and '-' not in expression and priority==2: return expression
    elif expression[i] in SYMBOLS:
        evaluate(expression, i)
        i = 0

    return calc_by_priority(expression, i+1, priority=priority)

def calc(expression):
    return reduce(expression)