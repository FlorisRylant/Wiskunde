from IOmaths.data import operators, functions, special, aliases
special_things = special.union(functions).union(operators) # handig als alles vervangen moet worden

from IOmaths.infix_to_tree import in_to_tree, skip_haakjes
from IOmaths.tree_to_infix import tree_to_in
from IOmaths.tree_to_postfix import tree_to_post

def preprocessor(expression): # splitst alles op        
    if type(expression) == list:
        if len(set(aliases.keys()).intersection(expression)) == 0: # als er niets vervangen moet worden kan een list zo door
            return expression
        else:
            expression = ''.join(expression) # gaat verder met het string_to_list-programma

    if type(expression) == str:
        expression = '$' + expression + '$' # zorgt dat de eerste en laatste in de lijst zeker leeg zijn
        for i, thing in enumerate(expression):
            if thing == '-' and expression[i-1] in {'$', '(', ','}.union(operators): # kijkt of de - achter een operator of speciaal teken komt
                if expression[i:skip_haakjes([c for c in expression], i)].count(',') == 0: # kijkt of er achter een tree-vorm komt
                    expression = expression[:i] + '~' + expression[i+1:] # vervangt unaire -
        for a in aliases: # vervangt alle aliases
            expression = expression.replace(a, aliases[a])
        for thing in special_things:
            expression = expression.replace(thing, '$'+thing+'$')
        expression = expression.replace('~', '-')
        expression = expression.replace('$$', '$')
        return expression.split('$')[1:-1] # geeft de lijst terug zonder de eerste en laatste
    
    raise TypeError(f"Kan geen {type(expression)} omzetten.")

def convert(start, typ='tree'):
    start = preprocessor(start)

    typ = typ.lower().strip()
    if not typ in ['tree', 'postfix', 'infix']:
        raise IOError(f"Kan niet omzetten naar {typ}")
    
    # type van het gegeven afleiden
    if start[-1] in special_things and start[-1] != ')':
        gegevenstype = 'postfix'
    else:
        gegevenstype = 'infix'
        if not start[0] in operators: # kijkt dat hij al zeker geen treestructuur heeft vanvoor
            for i in range(1, len(start)-1): # gaat over alles in de lijst buiten de twee randpunten
                if start[i] in operators and (start[i-1]=='(' or start[i-1]==','): # kijkt of het treenotatie impliceert
                    gegevenstype = 'tree'
                    break
        else: # als hij wél begint met een treestructuur
            gegevenstype = 'tree'          

    # afhandelen van het omzetten
    if gegevenstype == typ:
        return start
    if gegevenstype == 'infix':
        start = in_to_tree(start)
    elif gegevenstype == 'postfix':
        raise TypeError('Kan postfix niet naar een andere structuur omzetten')
    
    if typ == 'tree':
        return start
    elif typ == 'infix':
        return tree_to_in(start)
    elif typ == 'postfix':
        return tree_to_post(start)
    else:
        raise TypeError(f'Omzetting van {type(start)} naar {typ} onmogelijk')
    

def main():
    gegeven = ['sin','(', '(', 4, '-', 5, ')', '^', 2,')', '/', 6]
    post = convert(gegeven, 'Postfix')
    print(post)
    print(''.join(post))


if __name__ == '__main__':
    main()