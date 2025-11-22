from math import sin, cos, tan, sqrt, pi
def cot(theta):
    return cos(theta)/sin(theta)

functions = {'min':{'f':min, 'args':2},
             'max':{'f':max, 'args':2},
             'sin':{'f':sin, 'args':1},
             'cos':{'f':cos, 'args':1},
             'tan':{'f':tan, 'args':1},
             'cot':{'f':cot, 'args':1},
             'sqrt':{'f':sqrt, 'args':1}} # f = verwijzing naar de functie, args = aantal argumenten

special = {'(', ')', ','}

operators = {'^':{'prec':4, 'LtoR':False},
             '*':{'prec':3, 'LtoR':True},
             '/':{'prec':3, 'LtoR':True},
             '+':{'prec':2, 'LtoR':True},
             '-':{'prec':2, 'LtoR':True},
             }

aliases = {'**':'^', ';':',', '[':'(', ']':')', 'V':'sqrt'}