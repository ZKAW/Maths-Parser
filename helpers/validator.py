# Syntax validator

from . import handler as exc

def checkSyntax(expression):

    # Define the allowed operands
    numbers = [str(n) for n in list(range(0,10))] # Create list of num [0-9] and convert to str
    symbols = ['+','-','*','/']
    parentheses = ['(',')']

    allowed_operands = numbers + symbols + parentheses

    # Check if expression contains number
    if not any(x in numbers for x in expression): 
        return exc.raiseTypeError(command=expression, error='The expression must contain at least one number')

    for i in range(len(expression)):
        # Set empty element to empty string
        # Check if expression match the allowed operands

        if i-1 < 0: previousChar = ''
        else: previousChar = expression[i-1]
    
        if i+1 > len(expression)-1: nextChar = ''
        else: nextChar = expression[i+1]
        
        # Check if expression match the allowed operands
        if expression[i] not in allowed_operands: 
            return exc.raiseTypeError(command=expression, error=f"'{expression[i]}' is not a valid operand")

        # Check symbol syntax
        if expression[i] in symbols:
            if i == 0:
                return exc.raiseSyntaxError(command=expression, charPos=i, error=f"The expression can't start with a symbol")
            elif i == len(expression)-1:
                return exc.raiseSyntaxError(command=expression, charPos=i, error=f"The expression can't end with a symbol")
            elif (previousChar not in numbers) and (previousChar != ')'):
                return exc.raiseSyntaxError(command=expression, charPos=i)
            elif (nextChar not in numbers) and (nextChar != '('):
                return exc.raiseSyntaxError(command=expression, charPos=i)

        # Check parenthesis syntax
        if expression[i] in parentheses:
            if (expression[i] == '(') and (expression.count('(') > expression.count(')')):
                return exc.raiseSyntaxError(command=expression, charPos=i, error='The paranthesis has never been closed')
            elif (expression[i] == ')') and (expression.count(')') > expression.count('(')):
                return exc.raiseSyntaxError(command=expression, charPos=i, error='The paranthesis has never been opened')

            elif expression[i] == ')' and previousChar in symbols:
                return exc.raiseSyntaxError(command=expression, charPos=i)
            elif expression[i] == '(' and (nextChar in symbols or nextChar == ')'):
                return exc.raiseSyntaxError(command=expression, charPos=i)
            elif expression[i] == '(' and (previousChar == ')' or previousChar == '(' or previousChar in numbers): 
                return exc.raiseSyntaxError(command=expression, charPos=i)
            elif expression[i] == ')' and nextChar in numbers: 
                return exc.raiseSyntaxError(command=expression, charPos=i)

    return True