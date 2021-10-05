# Expression calculator

import operator
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
    splited_expr = re.split("([+-/*])", expression.replace(" ", ""))
    for i in range(len(splited_expr)):
        if splited_expr[i] not in NUMBERS+SYMBOLS+PARENTHESES: raise ValueError(f"Invalid operand")
        
        # Convert string number into integer
        try: splited_expr[i] = int(splited_expr[i])
        except: pass
    
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
    splited_expr = split_expr(expression)
    final = calc_secondary( calc_priority(splited_expr) ) # Calculate priority first (*,/) then secondary (+,-)
    return ''.join([str(int) for int in final])

def calc_parentheses(expression):
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    center_expr = expression[ expression.rfind('(')+1 : expression.find(')') ]
    after_expr = expression.find(')')+1

    if after_expr < len(expression): # Verify if end of the expression reached
        if expression[after_expr] not in SYMBOLS+[')']:
            raise SyntaxError("Only symbols should be put after a parenthesis")

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
    if '+' not in expression and '-' not in expression: return expression

    if expression[i] == '+' or expression[i] == '-':
        evaluate(expression, i)
        i = 0
    return calc_secondary(expression, i+1)

def calc(expression):
    if len(expression) == 1: return expression[0]
    else: return reduce(expression)