from data import functions, operators, special

def skip_haakjes(lijst, startpos): # springt over het haakjesblok waar hij zit, anders blijft hij gewoon
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

def verwerk_afwerking(lijst, positie, invoegen, pos2): # regelt heel het ergerlijke blok om alles aan te passen in één keer
    for i in reversed(invoegen):
        lijst.insert(positie, i)
    return False, pos2+len(invoegen), lijst

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
            if r >= len(infix):
                infix.append(')')
                r_go = False
            elif str(infix[r]) in operators and operators[infix[r]]['prec'] <= operators[op]['prec']:
                infix.insert(r, ')')
                r_go = False
            elif infix[r] == '(':
                r = skip_haakjes(infix, r)
            elif infix[r] == ')':
                i = skip_haakjes(infix, r)
                if i > 0 and (infix[i-1] in functions.keys() or infix[i-1][-1] == '$'): # kijkt of het haakjes van een functie zijn of niet
                    infix.insert(r, ')')
                r_go = False

            if l < 0:
                l_go, r, infix = verwerk_afwerking(infix, 0, [op+'$', '('], r)
            elif str(infix[l]) in operators and operators[infix[l]]['prec'] <= operators[op]['prec']:
                l_go, r, infix = verwerk_afwerking(infix, l+1, [op+'$', '('], r)
            elif infix[l] == '(':
                if l == 0 or (infix[l-1] not in functions.keys() and '$' not in infix[l-1]):
                    l_go, r, infix = verwerk_afwerking(infix, l, [op+'$'], r)
                else:
                    l_go, r, infix = verwerk_afwerking(infix, l+1, [op+'$', '('], r)
            elif infix[l] == ')':
                l = skip_haakjes(infix, l)

    # dollartekens weghalen en output teruggeven
    infix = '$'.join(infix).replace('$$', '$').split('$')   
    return infix

def main():
    infx = ['sin','(', '(', 4, '-', 5, ')', '^', 2,')', '/', 6]
    print(in_to_tree(infx))


if __name__ == '__main__':
    main()