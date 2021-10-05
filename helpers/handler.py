# Exception handler

def raiseSyntaxError(command, charPos=0, error='invalid syntax'):
    arrowCursor = ' '*charPos
    return(
        f'    {command}\n' \
        f'    {arrowCursor}^\n'\
        f'SyntaxError: {error}'
    )

def raiseTypeError(command, error='unexpected token'):
    return(
        f'    {command}\n' \
        f'TypeError: {error}'
    )