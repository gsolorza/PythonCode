
def pnumber(number):
    print(number)

def snumber(number):
    print(1+number)

function_list = [pnumber, snumber] 

def get_func(lista):
    for number in range(10):
        for l in lista:
            l(number)

get_func(function_list)