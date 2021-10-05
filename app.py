# Separate code in another local module to improve visibility
from helpers import validator, calculator

def solve(expression):
    validate = validator.checkSyntax(expression)
    if validate != True:
        return validate
    else:
        return calculator.calc(expression)

expression = input('Enter an expression to calculate: ')
print(solve(expression))