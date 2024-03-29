# Expression calculator

import operator # Allow final calculation without multiple "if" statments
import re

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
}

NUMBERS = [str(n) for n in list(range(0,10))]
SYMBOLS = ['+', '-', '*', '/', '.']
PARENTHESES = ['(', ')']

def tokenize(expression):
    if type(expression) == list: return expression
    # Check if every character in expression is allowed
    expression = expression.replace(' ','')
    if not any(x in expression for x in NUMBERS):
        raise ValueError("The expression must contain at least one number")

    for i in expression:
        if i not in SYMBOLS+PARENTHESES+NUMBERS:
            raise ValueError(f"Invalid token in expression: '{i}'")

    # Use regex to tokenize the expression (ex: 12*(4+2) -> ['12','*','(','4','+','2',')'])
    splited_expr = re.split('([()+/*-])', expression)
    while '' in splited_expr: splited_expr.remove('')

    for i in range(len(splited_expr)):
        try: splited_expr[i] = float(splited_expr[i])
        except: pass

    return splited_expr

def evaluate(expression, i):
    try:
        n1 = expression[i-1] 
        symbol = expression[i] 
        n2 = expression[i+1] 
        res = float(ops[symbol](n1,n2)) # Calc expression 
    except (IndexError, TypeError):
        return SyntaxError("Syntax error with operators, expected syntax: 'n1' 'operator' 'n2'")

    # Replace expression by the result of the operationz
    expression[i] = res 
    expression.pop(i-1)
    expression.pop(i)
    return expression

def calc(expression): # Calculate the mathematical expression, with priority order
    if len(expression) < 1:
        raise TypeError("The expression must contain at least one number")
    elif expression.count('(') != expression.count(')'): 
        raise SyntaxError("The parentheses are not opened or closed correctly")
    elif expression[0] in SYMBOLS:
        raise SyntaxError("The expression cannot start with a symbol")

    splited_expr = tokenize(expression) # Split expression in multiple tokens
    splited_expr = calc_parentheses(splited_expr) # Calculate every parentheses
    res = calc_by_priority(splited_expr) # Calculate * / first, then + -
    return ''.join([str(float) for float in res])

def calc_parentheses(expression): 
    if '(' not in expression: return expression

    # Get everything inside the deepest parentheses
    left_par = dict(map(reversed, enumerate(expression)))["("]
    right_par = left_par+1
    while expression[right_par] != ')': right_par += 1
    center_expr = expression[ left_par+1 : right_par]

    # Check parentheses syntax
    if right_par+1 < len(expression): 
        if expression[right_par+1] not in SYMBOLS+[')']:
            raise SyntaxError("Only symbols are accepted after a closed parentheses")
    
    if left_par-1 != -1: 
        if expression[left_par-1] not in SYMBOLS+['(']:
            raise SyntaxError("Only numbers are accepted before a open parentheses")

    for i in range(len(center_expr) + 2): expression.pop(left_par) # Remove calcul from the expression 
    expression.insert(left_par, float(calc(center_expr))) # Insert result into the expression (instead of the previous calcul)

    return calc_parentheses(expression)

def calc_by_priority(expression, i=0, priority=1):
    if '*' not in expression and '/' not in expression and priority==1: return calc_by_priority(expression, i=0, priority=2)
    elif '+' not in expression and '-' not in expression and priority==2: return expression

    if expression[i] in ['*','/'] and priority==1:
        evaluate(expression, i)
        i = 0
    elif expression[i] in ['+','-'] and priority==2:
        evaluate(expression, i)
        i = 0

    return calc_by_priority(expression, i+1, priority=priority)