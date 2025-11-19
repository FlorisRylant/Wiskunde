from data import functions, operators, special

def in_to_tree(infix): # infix = lijst met in volgorde de delen van de uitdrukking (bv [4, '+', 'x'])
    special_chars = special.union(functions, operators)
    ops = []
    for op in '-+*/^': # maakt een lijst met alle operatoren in infix
        ops.extend([op for _ in range(infix.count(op))])
    
    places = set()
    for i, op in enumerate(infix):
        if op in operators.keys():
            places.add(i)

    for op in ops: # 'bubbelt' elke operator een voor een naar de juiste plek
        p = operators[op]['prec']
        l = infix.index(op) # startpositie van die operator
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
            elif str(infix[l]) in operators and operators[infix[l]]['prec'] <= p:
                infix.insert(l+1, '(')
                infix.insert(l+1, op+'$')
                l_go = False
                r += 2
            elif infix[l] == '(':
                infix.insert(l, op+'$')
                l_go = False
                r += 1
            elif infix[l] == ')':
                i = l # bevriest tijdelijk het starthaakje
                l -= 1
                while infix[l:i+1].count('(') != infix[l:i+1].count(')'): # blijft gaan tot hij bij het haakje sluiten zit
                    l -= 1
            

                


    print(infix)


def main():
    in_to_tree(['(', 4, '-', 5, ')', '^', 2, '/', 6])

if __name__ == '__main__':
    main()