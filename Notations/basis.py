from math import sin, cos, tan, pi, tau, e, log, inf, floor, ceil

def cot(theta):
    if sin(theta) == 0:
        return inf
    return cos(theta)/sin(theta)

def faculteit(n, _=0): # de underscore is om extra variabelen op te vangen die kunnen voortvloeien uit notatie-programma's
    if n%1 != 0 or n < 0:
        raise ValueError(f'Kan {n}! niet berekenen.')
    if int(n) == 0:
        return 1
    return int(n)*faculteit(n-1)

def ln(x):
    return log(x)

def skip_haakjes(iter, startpos, first_recursion=True): # geeft terug hoeveel posities hij naar rechts moet gaan
    if iter[startpos] == ')':
        i = startpos-1
        while iter[i:startpos].count('(') != iter[i:startpos].count(')')+1 and i>=0: # het haakje op starpos wordt niet meegeteld
            i -= 1
        return i
    elif iter[startpos] == '(':
        i = startpos+1
        while iter[startpos:i+1].count('(') != iter[startpos:i+1].count(')') and i<len(iter):
            i += 1
        return i
    else:
        return startpos


aliases = {';':',', '[':'(', ']':')', '**':'^', '!':'??', '-':'~', ' ':''} # vervangt ook de - en ! zodat dat niet in de preprocessor apart moet
constants = {'pi':pi, 'tau':tau, 'e':e, 'inf':inf}
special = {',', '(', ')', '~', '??'}
functions = {'sin':sin, 'cos':cos, 'tan':tan, 'cot':cot, 'log':log, 'ln':ln, '!':faculteit, 'floor':floor, 'ceil':ceil, 'round':round, 'min':min, 'max':max}
operators = {'+':(1, True), '-':(1.1, True), '*':(2, True), '/':(2.1, True), '^':(3, False)} # tuple: (precedence, left-to-right)

def main():
    lijst = ['sin', '(', 2, '+', '(', 'pi', '*', 4, ')', ')']
    for i in range(len(lijst)):
        print(skip_haakjes(lijst, i), lijst[i])


if __name__ == '__main__':
    main()