from IOmaths.interpreter import convert, functions, operators
from IOmaths.infix_to_tree import skip_haakjes
from functie_objects import Functie, Constante, Onbekende

def functie_recursie(tree): # maakt van een boom een functie
    if '(' not in tree: # eindnode van de tree
        if tree[0].isnumeric():
            return Constante(tree[0])
        return Onbekende(tree[0])
    if tree[0] in functions or tree[0] in operators:
        args = []
        i = 2
        j = 2
        while i < len(tree):
            if tree[i] == '(':
                i = skip_haakjes(tree, i)
            elif tree[i] == ',':
                args.append(tree[j:i])
                j = i+1
                i += 1
            i += 1
        args.append(tree[j:-1])
        args = tuple([functie_recursie(a) for a in args])
        return Functie(tree[0], *args) # de asterisk voor args "unpackt" de tuple
    raise KeyError(f'Kan {tree[0]} niet in een functie steken')

def maak_functie(start):
    start = convert(start) # zet om naar tree
    return functie_recursie(start)

def print_functie(f):
    print(''.join(convert(f.treerepr(), 'infix')))


def main():
    f = maak_functie('(5+x)*x')
    print_functie(f)
    print(f"f(4) = {f(4)}")

if __name__ == '__main__':
    main()