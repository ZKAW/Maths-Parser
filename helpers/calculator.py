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
OPERANDS = ['+', '-', '*', '/']
PARENTHESES = ['(', ')']

def split_expr(expression):
    splited_expr = re.split("([+-/*])", expression.replace(" ", ""))
    for i in range(len(splited_expr)):
        if splited_expr[i] not in NUMBERS+OPERANDS+PARENTHESES:
            raise ValueError(f"Invalid operand")
        try:
            splited_expr[i] = int(splited_expr[i])
        except:
            pass
    
    return splited_expr

def evaluate(expression, i):
    n1 = expression[i-1] # Get element before symbol
    n2 = expression[i+1] # Get element after symbol    
    res =  int(ops[expression[i]](n1,n2)) # Result of the operation

    # Replace expression by result of the operation
    expression[i] = res 
    expression.pop(i-1)
    expression.pop(i)
    return expression

def reduce(expression):
    # Calculate the expression, with priority order 
    expression = calc_parentheses(expression)
    splited_expr = split_expr(expression)
    final = calc_secondary( calc_priority(splited_expr) ) # Calculate priority first (*,/) then secondary (+,-)
    result = ''.join([str(int) for int in final])
    return result

def calc_parentheses(expression):
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    center_expr = expression[ expression.rfind('(')+1 : expression.find(')') ]
    after_expr = expression.find(')')+1

    if after_expr < len(expression): # Verify if end of the expression reached
        if expression[after_expr] not in OPERANDS+[')']:
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
    if '+' not in expression: return expression

    if expression[i] == '+':
        evaluate(expression, i)
        i = 0
    return calc_secondary(expression, i+1)

def calc(expression):
    if len(expression) == 1: return expression[0]

    # Calculate expression and return result
    return reduce(expression)