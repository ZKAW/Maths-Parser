from helpers import calculator

def solve(expression):
    return calculator.calc(expression)

expression = input('Enter an expression to calculate: ')
print(f"{expression} = {solve(expression)}")