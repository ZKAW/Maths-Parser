import re

NUMBERS = [str(n) for n in list(range(0,10))]
SYMBOLS = ['+', '-', '*', '/']
PARENTHESES = ['(', ')']

def split_expr(expression):
    splited_expr = []
    pos = 0
    if not any(x in expression for x in NUMBERS):
        raise ValueError("L'expression doit contenir au minimum un chiffre")
    while pos < len(expression):
        char = expression[pos]
        if char == ' ': pass # Ignore white spaces
        elif char in SYMBOLS+PARENTHESES: # If char is a symbol
            splited_expr.append(char)
        elif char.isdigit(): # If char is a number
            num = float(char)
            while pos + 1 < len(expression) and expression[pos + 1].isdigit(): # Get entire number instead of single digit 
                pos += 1
                num = num * 10 + float(expression[pos]) # Extand number ten until entire number is present
                # Ex: 125 = 1*10 -> +2 -> 12 -> 2*10 -> +5 -> 125
            splited_expr.append(num)
        else: # Unknown operand, raise error
            raise TypeError(f"'{expression[pos]}' is not a valid operand")

        pos += 1
    return splited_expr

def calc_parentheses(expression): 
    if '(' not in expression: return expression
    
    # Get everything inside the deepest parentheses
    left_par = dict(map(reversed, enumerate(expression)))["("]
    right_par = expression.index(')')
    center_expr = expression[ left_par : right_par]

    if right_par < len(expression): # Verify if end of the expression reached
        if expression[right_par+1] not in SYMBOLS+[')']:
            raise SyntaxError("Seul les symboles sont acceptés après une parenthèse fermée")
    
    if left_par-1 != -1: # Verify if start of the expression reached
        if expression[left_par-1] not in SYMBOLS+['(']:
             raise SyntaxError("Seul les symboles sont acceptés avant une parenthèse ouverte")

    print(expression)
    for i in range(len(center_expr) + 2): expression.pop(left_par) # Remove calcul from the expression 
    expression.insert(left_par, '15') # Insert result into the expression (instead of the previous calcul)

    return calc_parentheses(expression)

expression = split_expr("2(10+(3*5)+1)+10")





print(expression)
print(calc_parentheses(expression))