from IOmaths.infix_to_tree import skip_haakjes

def tree_to_post(tree):
    tree = [str(i) for i in tree]
    while '(' in tree:
        i1 = tree.index('(')
        i2 = skip_haakjes(tree, i1)
        if i1 > i2: # zorgt dat i1 de kleinste is
            i2 += i1
            i1 = i2 - i1
            i2 -= i1
        tree[i2] = tree[i1-1] # zet de operator / functie erachter op de plek van )
        del tree[i1-1] # haalt functie ( weg
        del tree[i1-1]
    while ',' in tree:
        tree.remove(',')

    return tree

def main():
    tr = ['sin', '(', '/', '(', '^', '(', '-', '(', '4', ',', '5', ')', ',', '2', ')', ',', '6', ')', ')']
    print(tree_to_post(tr))

if __name__ == '__main__':
    main()