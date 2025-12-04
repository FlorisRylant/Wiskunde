try: from basis import *
except: from Notations.basis import *

def tree2post(tree):
    """
    Vrij simpel algoritme om van boomstructuur naar postfix te gaan:
    Loopt over alle operatoren en functies
    -> zet ze achter hun argumenten
    -> verwijder de haakjes van die operator / functie

    Verwijder alle overblijvende komma's
    -> klaar
    """
    for op in set(functions).union(operators):
        while op in tree:
            positie = tree.index(op) - 1 # gaat naar het haakje links van de operator of functie
            tree[skip_haakjes(tree, positie)] = op+'$' # vervangt rechterhaakje
            del tree[positie] # haalt '(' weg
            del tree[positie] # haalt de operator weg

    while ',' in tree: # haalt alle komma's weg
        del tree[tree.index(',')]
    
    tree = [i.replace('$', '') for i in tree] # alle dollartekens weghalen
    return tree


def main():
    expression = ['(', 'sin', ',', '(', '*', ',', '5', ',', '(','-', ',', '2', ',', 'pi', ')', ')', ')']
    print(tree2post(expression))

if __name__ == '__main__':
    main()