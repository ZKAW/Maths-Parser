# Expression calculator

import operator # Allow final calculation without multiple "if" condition
import re

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
}

# TODO: float result instead of int // rebuild calc_parentheses to use list instead of str

NUMBERS = [str(n) for n in list(range(0,10))]
SYMBOLS = ['+', '-', '*', '/']
PARENTHESES = ['(', ')']

def split_expr(expression):
    maths_reg = re.compile('(\d+|[^ 0-9])')
    splited_expr = re.findall(maths_reg, expression)

    if not any(x in expression for x in NUMBERS):
        raise ValueError("L'expression doit contenir au minimum un chiffre")
            
    for i in range(len(splited_expr)):
        if splited_expr[i] not in SYMBOLS+PARENTHESES: # If character is not a symbol
            try: splited_expr[i] = int(splited_expr[i])
            except: raise ValueError(f"Donnée invalide dans l'expression: '{splited_expr[i]}' pos: {i}") # If character is not a number

    return splited_expr

def evaluate(expression, i):
    try:
        n1 = expression[i-1] # Get element before symbol
        symbol = expression[i] # Get the operator
        n2 = expression[i+1] # Get element after symbol
    except IndexError:
        raise SyntaxError("Syntaxte invalide au niveau des opérateurs, syntaxe attendue: 'n1' 'opérateur' 'n2'")
    res = int(ops[symbol](n1,n2)) # Result of the operation

    # Replace expression by result of the operation
    expression[i] = res 
    expression.pop(i-1)
    expression.pop(i)
    return expression

def calc(expression): # Calculate the mathematical expression, with priority order 
    if expression.count('(') != expression.count(')'): 
        raise SyntaxError("Les parenthèses n'ont pas été ouvertes ou fermées correctement")
    
    expression = calc_parentheses(expression) # Calculate every parentheses first
    res = calc_by_priority(split_expr(expression)) # Calculate * / first then + -
    res = ''.join([str(int) for int in res])
    return res

def calc_parentheses(expression): 
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    center_expr = expression[ expression.rfind('(')+1 : expression.find(')') ]
    after_expr = expression.find(')')+1
    before_expr = expression.rfind('(')-1

    if after_expr < len(expression):
        if expression[after_expr] not in SYMBOLS+[')']:
            raise SyntaxError("Seul les symboles sont acceptés après une parenthèse fermée")
    
    if before_expr != -1:
        if expression[before_expr] not in SYMBOLS+['(']:
            raise SyntaxError("Seul les symboles sont acceptés avant une parenthèse ouverte")

    expression = expression.replace(f'({center_expr})', calc(center_expr))
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