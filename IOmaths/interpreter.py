from IOmaths.data import operators, functions, special, aliases
special_things = special.union(functions).union(operators) # handig als alles vervangen moet worden

from IOmaths.infix_to_tree import in_to_tree
from IOmaths.tree_to_infix import tree_to_in
from IOmaths.tree_to_postfix import tree_to_post

def preprocessor(expression): # splitst alles op        
    if type(expression) == list:
        if len(set(aliases.keys()).intersection(expression)) == 0: # als er niets vervangen moet worden kan een list zo door
            return expression
        else:
            expression = ''.join(expression) # gaat verder met het string_to_list-programma

    if type(expression) == str:
        for a in aliases: # vervangt alle aliases
            expression = expression.replace(a, aliases[a])
        for thing in special_things:
            expression = expression.replace(thing, '$'+thing+'$')
        expression = '$' + expression + '$' # zorgt dat de eerste en laatste in de lijst zeker leeg zijn
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
        if start[1:].count('(') == 0:
            gegevenstype = 'infix'
        else:
            gegevenstype = 'tree'
        for i, thing in enumerate(start[:-1]):
            if start[i+1] == '(' and not thing in set(operators.keys()).union(functions.keys()) and gegevenstype != 'infix': # kijkt of er voor elk haakje een operator staat
                gegevenstype = 'infix'

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