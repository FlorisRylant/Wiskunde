from data import operators
from infix_to_tree import skip_haakjes

def tree_to_in(tree):
    tree = [str(i) for i in tree]
    ops = [i for i in tree if i in '+-/*^'] # maakt een lijst met alle operatoren in infix

    for op in ops:
        i = tree.index(op)
        del tree[i]
        while tree[i] != ',':
            i += 1
            if tree[i] == '(':
                i = skip_haakjes(tree, i)
        tree[i] = op+'$' # vervangt de , door de operator

    # dollartekens weghalen en output teruggeven
    tree = '$'.join(tree).replace('$$', '$').split('$')   
    return tree


def main():
    tr = ['/', '(', 'sin', '(', '^', '(', '-', '(', '4', ',', '5', ')', ',', '2', ')', ')', ')', ',', '6', ')']
    print(''.join(tree_to_in(tr)))

if __name__ == '__main__':
    main()