import re 

def validatePin(pin):   
        # dla wersji Python3.4
        '''
        if re.fullmatch("\d{4}|\d{6}", pin):
            return True
        else:
            return False'
        '''
        # ale to jest bezpieczniejsza opcja
        if re.match("\d{4}$|\d{6}$", pin):
            return True
        else:
            return False



for i in range(10):
    inputPin = input("Podaj pin: ")

    if validatePin(inputPin):
        print("success")
    else:
        print("fail")
print("end")