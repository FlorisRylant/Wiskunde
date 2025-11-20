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

def pas_posities_aan(lijst, i, keer=1):
    for l in lijst:
        if l >= i:
            l += keer
    return lijst

def in_to_tree(infix): # infix = lijst met in volgorde de delen van de uitdrukking (bv [4, '+', 'x'])
    special_chars = special.union(functions, operators)
    ops = []
    for op in '-+*/^': # maakt een lijst met alle operatoren in infix
        ops.extend([op for _ in range(infix.count(op))])
    
    places = []
    for i, op in enumerate(infix):
        if op in operators.keys():
            places.append(i)
    offset = 0

    for op in ops: # 'bubbelt' elke operator een voor een naar de juiste plek
        l = infix.index(op) # startpositie van die operator
        infix[l] = ','
        r = l # rechter-'bubbel'
        l_go = True
        r_go = True
        while l_go or r_go:
            l -= int(l_go) # naar buiten bubbelen als ze nog niet geblokkeerd zijn
            r += int(r_go)
            if l < 0:
                infix = [op+'$', '('] + infix
                l_go = False
                r += 2
                places = pas_posities_aan(places, l, 2)
            elif str(infix[l]) in operators and operators[infix[l]]['prec'] <= operators[op]['prec']:
                infix.insert(l+1, '(')
                infix.insert(l+1, op+'$')
                l_go = False
                r += 2
                places = pas_posities_aan(places, l, 2)
            elif infix[l] == '(':
                infix.insert(l, op+'$')
                l_go = False
                r += 1
                places = pas_posities_aan(places, l)
            elif infix[l] == ')':
                l = skip_haakjes(infix, l)

            if r >= len(infix):
                infix.append(')')
                r_go = False
                places = pas_posities_aan(places, r)
            elif str(infix[r]) in operators and operators[infix[r]]['prec'] <= operators[op]['prec']:
                infix.insert(r, ')')
                r_go = False
                places = pas_posities_aan(places, r)
            elif infix[r] == ')':
                r_go = False
                places = pas_posities_aan(places, r)
            elif infix[r] == '(':
                r = skip_haakjes(infix, r)
            
    for i, thing in enumerate(infix):
        if type(thing) == str:
            infix[i] = thing.replace('$', '')
                
    return infix

def main():
    infx = ['(', '(', 4, '-', 5, ')', '^', 2, ')', '/', 6]
    print(in_to_tree(infx))

if __name__ == '__main__':
    main()