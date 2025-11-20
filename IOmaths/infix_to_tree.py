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
    special_chars = special.union(functions, operators)
    ops = []
    for op in '-+*/^': # maakt een lijst met alle operatoren in infix
        ops.extend([op for _ in range(infix.count(op))])
    
    places = []
    for i, op in enumerate(infix):
        if op in operators.keys():
            places.append(i)
    offset = 0

    while len(places) != 0: # 'bubbelt' elke operator een voor een naar de juiste plek
        l = places.pop(0) + offset # startpositie van die operator
        op = infix[l]
        infix[l] = ','
        r = l # rechter-'bubbel'
        l_go = True
        r_go = False
        while l_go or r_go:
            l -= int(l_go) # naar buiten bubbelen als ze nog niet geblokkeerd zijn
            r += int(r_go)
            if l < 0:
                infix = [op+'$', '('] + infix
                l_go = False
                r += 2
                offset += 2
            elif str(infix[l]) in operators and operators[infix[l]]['prec'] <= operators[op]['prec']:
                infix.insert(l+1, '(')
                infix.insert(l+1, op+'$')
                l_go = False
                r += 2
                offset += 2
            elif infix[l] == '(':
                infix.insert(l, op+'$')
                l_go = False
                r += 1
                offset += 1
            elif infix[l] == ')':
                i = l # bevriest tijdelijk het starthaakje
                l -= 1
                while infix[l:i+1].count('(') != infix[l:i+1].count(')'): # blijft gaan tot hij bij het haakje sluiten zit
                    l -= 1
            

                
    print(infix)


def main():
    infx = ['(', '(', 4, '-', 5, ')', '^', 2, ')', '/', 6]
    #in_to_tree(infx)
    print(skip_haakjes(infx, 0))

if __name__ == '__main__':
    main()