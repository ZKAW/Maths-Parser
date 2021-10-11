import eel
from helpers import calculator

eel.init('web')

@eel.expose()
def solve(expression):
    try:
        res = calculator.calc(expression)
        print(f"{expression} = {res}")
        return res
    except Exception as ex:
        return(f'error={ex}')

eel.start('index.html', block=False)

while True:
    eel.sleep(10)