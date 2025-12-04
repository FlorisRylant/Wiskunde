try: from basis import *
except: from Notations.basis import *

def tree2in(tree):
    tree = ['('] + tree + [')'] # bufferzone

    for op in functions: # zet alle functies buiten haakjes
        while op in tree:
            positie = tree.index(op)
            tree = tree[:positie-1] + [op+'$', '('] + tree[positie+2:] # vervangt "(op," door "op("

    for op in sorted(operators, key=lambda k: operators[k][0], reverse=True): # gaat over de operatoren van belangrijker naar minder (helpt met haakjeslogica)
        while op in tree:
            positie = tree.index(op)-1 # gaat naar het haakje voor de operator
            tree[skip_haakjes(tree, positie+3)+1] = op+'$' # vervangt het haakje na het eerste argument door "op$"
            tree = tree[:positie+1] + tree[positie+3:] # haalt "op," weg

            if tree[positie-1][0] not in operators or (tree[positie-1][0]==op and operators[op][0]%1==0) and tree[skip_haakjes(tree, positie) + 1][0] not in operators:
                # checkt dat er links geen hogere operator staat (houdt rekening met associativiteit) en dan of er rechts geen staat
                del tree[skip_haakjes(tree, positie)] # haalt het sluithaakje weg
                del tree[positie] 
    
    tree = [i.replace('$', '') for i in tree[1:-1]] # alle dollartekens weghalen en de open- en sluithaakjes
    return tree


def main():
    expression = ['(', 'sin', ',', '(', '*', ',', '5', ',', '(','-', ',', '2', ',', 'pi', ')', ')', ')']
    print(tree2in(expression))

if __name__ == '__main__':
    main()