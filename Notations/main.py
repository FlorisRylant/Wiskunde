try: # imports bij extern gebruik
    from Notations.basis import *
    from Notations.in2tree import in2tree
    from Notations.tree2in import tree2in
    from Notations.tree2post import tree2post
except: # imports bij intern gebruik
    from basis import *
    from in2tree import in2tree
    from tree2in import tree2in
    from tree2post import tree2post

def preprocess(expression):
    """
    Preprocessor:
    zet input (expression) om naar een bruikbare lijst voor de algoritmes:
    - als het al een lijst is wordt die nog naar een string omgezet en verwerkt (korter voor alle randgevallen)
    - als het een string is wordt elk speciaal teken omhult in $-tekens en later gesplitst (mits enige verfijning)
    - haakjesparen die slechts één ding bevatten worden verwijderd tenzij er een functie voor staat
    """
    if type(expression) == list: expression = ''.join([str(i) for i in expression])
    elif type(expression) != str: raise IOError(f'Type {type(expression)} unreadable')
    
    # hieronder is de code voor strings
    expression = f'${expression.lower()}$' # dollars aan de randen als buffer
    for thing in aliases: # vervangt de te vervangen dingen
        expression = expression.replace(thing, aliases[thing])
    if expression.count('(') != expression.count(')'): # kijkt na dat de haakjes overeenkomen
            raise SyntaxError(f'Parenthese mismatch: "(":{expression.count("(")}, ")":{expression.count(")")}')
    
    for thing in sorted(special.union(functions).union(operators), key=lambda k:len(k), reverse=True): # zet een $ bij elke scheiding en zet functies in uppercase (voor sinh en sin enzo)
        expression = expression.replace(thing, f'${thing.upper()}$') # upper zodat functies elkaar niet kunnen overriden
    expression = expression.lower()
    expression = expression.replace('$$', '$') # voor als er twee speciale dingen naast elkaar stonden
    expression = expression.split('$') # splitst alles en haalt de buffer weg

    # opvangen van unaire operatoren
    while '~' in expression:
        positie = len(expression)-1-expression[::-1].index('~')
        expression[positie] = '-' # zet om naar gewone min
        if expression[positie-1] in {'(', ','}.union(operators): # kijkt of het een unaire - is
            expression = expression[:positie] + ['(', '0'] + expression[positie:] # voegt de "(0" al toe
            positie += 3
            while expression[positie] not in ',)+-~': # kijkt of de min nog tot hier reikt
                positie = skip_haakjes(expression, positie) +1
            expression.insert(positie, ')') # voegt het sluithaakje toe
            
    while '??' in expression: # blok om faculteit te regelen
        positie = expression.index('??')
        expression[positie] = ')'
        positie = skip_haakjes(expression, positie-1) # gaat naar de andere kant van de haakjes
        expression.insert(positie, '(')
        expression.insert(positie, '!')

    # dubbele haakjesparen wegwerken:
    positie = 0
    while positie < len(expression)-1:
        if  expression[positie]=='(' and skip_haakjes(expression, positie+1)+1 == skip_haakjes(expression, positie) and (expression[positie+1]=='(' or expression[positie-1] not in functions):
            del expression[skip_haakjes(expression, positie)]
            del expression[positie]
        else:
            positie += 1

    return expression[1:-1] # haalt de buffer eraf


def convert(expression, naar='tree', gegeven='default', processed=False):
    naar, gegeven = naar.lower(), gegeven.lower()
    if not processed: expression = preprocess(expression) # wordt genegeerd als het al gedaan is om té veel nutteloos werk te vermijden
    if gegeven != 'default': # blok als het gegeven type geweten is
        if naar == gegeven: return expression

        if gegeven == 'infix': expression = in2tree(expression) # omzetten van infix naar tree
        elif gegeven == 'postfix': raise TypeError('Kan postfix niet omzetten naar andere types') # wiskundig niet altijd mogelijk
        elif gegeven != 'tree': raise TypeError(f'Kan {gegeven} niet omzetten naar tree (tussenstap).')

        if naar == 'tree': return expression
        elif naar == 'infix': return tree2in(expression)
        elif naar == 'postfix': return tree2post(expression)
        raise TypeError(f'Kan niet omzetten van tree naar {naar}.')
    
    ops = set(functions).union(operators)
    if expression[-1] in ops:
        return convert(expression, naar, 'postfix', True)
    if ',' in expression and expression[expression.index(',')-1] in ops:
        return convert(expression, naar, 'tree', True)
    return convert(expression, naar, 'infix', True)
    



def main():
    expr = 'min((sin(4), 10**0.1))'
    print(''.join(convert(expr, 'postfix')))

if __name__ == '__main__':
    main()