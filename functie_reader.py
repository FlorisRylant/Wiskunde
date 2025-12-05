from Notations.basis import *
from Notations.main import convert
from functie_objects import Functie, Constante, Onbekende

def functie_recursie(tree):
    """
    Maakt van een lijst die een gesplitste treeweergave voorstelt een Functie-tree.
    - Steekt de operator (voor de haakjes) in self.__op
    - Recurseert over de argumenten en steekt die dan in self.__args
    
    Als het een constante of een onbekende is wordt dat in de respectievelijke functie gestoken."""
    if '(' not in tree: # eindnode van de tree
        if tree[0].isnumeric():
            return Constante(tree[0])
        return Onbekende(tree[0])
    if tree[1] in functions or tree[1] in operators:
        tree = tree[1:-1] # haalt het begin- en eindhaakje eraf
        args = []
        i = 2
        start = 2
        while i < len(tree):
            if tree[i] == ',':
                args.append(functie_recursie(tree[start:i]))
                i += 1 # gaat naar vlak achter de komma
                start = i
            i = skip_haakjes(tree, i)+1
        args.append(functie_recursie(tree[start:]))

        args = tuple(args)
        return Functie(tree[0], *args) # de asterisk voor args "unpackt" de tuple
    raise KeyError(f'Kan {tree[0]} niet in een functie steken')

def maak_functie(start):
    """
    Maakt van eender welke notatie een werkende Functie-structuur
    """
    start = convert(start) # zet om naar tree
    return functie_recursie(start)

def print_functie(f):
    print(''.join(convert(f.treerepr(), 'infix', 'tree')))


def main():
    h = maak_functie('min(max(5, x), sin(-4^2))')
    print_functie(h)
    print(''.join(h.treerepr()))

if __name__ == '__main__':
    main()