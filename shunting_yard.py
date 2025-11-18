from wiskundedata import functions, aliases, operators, special

def shunting_yard(expression):
    """
    Deze functie zet een menselijk geschreven uitdrukking om naar RPN.
    Ondersteunt enkel standaardfuncties en bewerkingen
    Structuur:
    - expressie wordt mooi gevormd
    - expressie wordt gesplitst (hier worden variabelen zoals 'x' al mooi gescheiden)
    - shunting yard-algoritme
    Het resultaat van het algoritme wordt teruggegeven.
    
    De functie kan vastlopen bij (althans de gevonden errors):
    - haakjes komen niet overeen
    - ',' gebruikt zonder '(' ervoor
    - een functie gebruiken zonder haakjes
    
    Iets van de vorm '4pi' wordt teruggegeven alsof het één getal is
    -> handig voor verdere verwerking later
    """

    # preprocessor: alles 'schoonmaken'
    expression = expression.strip().lower()
    for a in aliases: # vervangt de aliases
        expression = expression.replace(a, aliases[a])

    # expressie in delen splitsen (gescheiden door $) die om de beurt overlopen worden
    for f in set(functions.keys()).union(operators.keys()).union(special):
        expression = expression.replace(f, '$'+f+'$')
    expression = expression.replace('$$', '$') # voorkomt problemen met twee operatoren naast elkaar
    expression = expression.strip('$') # zorgt dat er geen lege items aan de randen zitten
    expression = expression.split('$')
    
    # daadwerkelijke algoritme (zie wikipedia voor deftige uitleg, dan snap je de comments hier)
    out = []      # de uiteindelijke output
    op_stack = [] # de operator-qeue
    for thing in expression: # gaat over alles in 'expression'
        if thing == '(':
            op_stack.append(thing)
        elif thing == ')':
            while (len(op_stack) != 0) and (op_stack[-1] != '('):
                out.append(op_stack.pop()) # operatoren naar out poppen
            if len(op_stack) == 0: # als er geen ( is
                raise IndexError('Haakjes komen niet overeen') # stopt de functie ook meteen
            op_stack.pop() # haalt ( weg
            if (len(op_stack) != 0) and (op_stack[-1] in functions): # voegt eventuele functie toe
                out.append(op_stack.pop())
        elif thing == ',':
            while (len(op_stack) != 0) and (op_stack[-1] != '('):
                out.append(op_stack.pop()) # operatoren naar out poppen
            if len(op_stack) == 0: # als er geen ( is
                raise IndexError('Haakjes komen niet overeen') # stopt de functie ook meteen
        elif thing in functions:
            op_stack.append(thing)
        elif thing in operators:
            while (len(op_stack) != 0) and (op_stack[-1] != '('):
                if operators[thing]['prec'] > operators[op_stack[-1]]['prec']:
                    break # jaja slechte code maar anders was het een while-voorwaarde van een meter breed
                if operators[thing]['prec'] == operators[op_stack[-1]]['prec'] and not(operators[thing]['LtoR']):
                    break # zie twee regels hierboven
                out.append(op_stack.pop())
            op_stack.append(thing)
        else: # getallen en variabelen komen hier vanzelf terecht
            out.append(thing)
    if '(' in op_stack:
        raise IndexError('Haakjes komen niet overeen')
    out.extend(reversed(op_stack))
    
    return out

def main():
    print(shunting_yard('sin(5pi-4)*3^2'))

if __name__ == '__main__':
    main()