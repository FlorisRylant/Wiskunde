from data import functions, operators, special

def skip_haakjes(lijst, startpos):
    if lijst[startpos] == ')':
        increment = -1
        i = startpos
        startpos += 1
    else:
        increment = 1
        i = startpos + 1
    while lijst[min(i, startpos):max(i, startpos)].count(')') != lijst[min(i, startpos):max(i, startpos)].count('('):
        i += increment
    if increment == 1:
        i -= 1
    return i

def in_to_tree(infix): # infix = lijst met in volgorde de delen van de uitdrukking (bv [4, '+', 'x'])
    infix = [str(i) for i in infix]
    ops = [i for i in infix if i in '+-/*^'] # maakt een lijst met alle operatoren in infix
    
    for op in ops: # 'bubbelt' elke operator een voor een naar de juiste plek
        r = infix.index(op) # startpositie van die operator
        l = r
        infix[l] = ','
        l_go, r_go = True, True
        while l_go or r_go:
            l -= int(l_go) # naar buiten bubbelen als ze nog niet geblokkeerd zijn
            r += int(r_go)
            if l < 0:
                infix = [op+'$', '('] + infix
                l_go = False
                r += 2
            elif str(infix[l]) in operators and operators[infix[l]]['prec'] <= operators[op]['prec']:
                infix.insert(l+1, '(')
                infix.insert(l+1, op+'$')
                l_go = False
                r += 2
            elif infix[l] == '(':
                if l == 0 or (infix[l-1] not in functions.keys() and (type(infix[l-1])==str and '$' not in infix[l-1])):
                    infix.insert(l, op+'$')
                else:
                    infix.insert(l+1, '(')
                    infix.insert(l+1, op+'$')
                l_go = False
                r += 1
            elif infix[l] == ')':
                l = skip_haakjes(infix, l)

            if r >= len(infix):
                infix.append(')')
                r_go = False
            elif str(infix[r]) in operators and operators[infix[r]]['prec'] <= operators[op]['prec']:
                infix.insert(r, ')')
                r_go = False
            elif infix[r] == ')':
                r_go = False
            elif infix[r] == '(':
                r = skip_haakjes(infix, r)
    # dollartekens weghalen en output teruggeven
    infix = '$'.join(infix).replace('$$', '$').split('$')   
    return infix

def main():
    infx = ['max', '(', '(', 4, '-', 5, ')', ',', 2,')']
    print(in_to_tree(infx))

if __name__ == '__main__':
    main()