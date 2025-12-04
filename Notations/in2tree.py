# blok om ervoor te zorgen dat alles deftig geïmporteerd wordt
try: from basis import *
except: from Notations.basis import *

def in2tree(infix):
    """Sterk verbeterde versie van de eerste infix_to_tree:
    verbeteringen:
    - 41 regels code -> 20 regels
    - 8 variabelen met rare namen -> 3 variabelen die nuttiger aanvoelen
    - eleganter in het algemeen (alle randgevallen worden inherent gecompenseerd door de buffer en skip_haakjes)
    - dit algoritme is logischer
    - deze versie haalt onnodige haakjes weg
    - deze versie is compatibeler met unaire operatoren én robuuster
    input: lijst die opgedeeld is in de verschillende bouwsteentjes van een uitdrukking, alles in strings.
    output: lijst met zelfde bouwstenen maar in een boomstructuur: (op, arg1, arg2, ...)
    
    structuur algoritme:
    ├─ haakjesbuffer maken
    ├─┐  FUNCTIES BINNEN HAAKJES ZETTEN
    | ├─ positie functie vinden
    | └─ functie, '(' vervangen door '(', functie, ','
    |
    ├─┐  OVER OPERATOREN LOOPEN
    | ├─ positie van de operator vinden
    | ├─ sluithaakje toevoegen
    | └─ openhaakje, operator$ en ',' toevoegen vanvoor
    |
    ├─ onnodige haakjesparen verwijderen
    ├─ $-tekens weghalen
    └─ return infix
    """
    infix = ['('] + infix + [')'] # bufferzone om randgevallen handig op te vangen

    for op in functions: # zet alle functies binnen haakjes
        while op in infix:
            positie = infix.index(op)
            infix = infix[:positie] + ['(', f'{op}$', ','] + infix[positie+2:]

    for op in sorted(operators, key=lambda k: operators[k][0], reverse=True): # gaat over de operatoren van belangrijker naar minder (inverse iets belangrijker omdat die niet commutatief is)
        while op in infix: # blijft gaan zolang die operator erinzit -> zeker zorgen dat elke operator weggewerkt is!
            if operators[op][1]: positie = infix.index(op)      # bewerkingen van links naar rechts
            else: positie = len(infix)-1-infix[::-1].index(op)  # bewerkingen van rechts naar links
            infix[positie] = ',' # operator vervangen

            infix.insert(skip_haakjes(infix, positie+1)+1, ')') # voegt het sluithaakje toe aan de rechterkant
            infix = infix[:skip_haakjes(infix, positie-1)] + ['(', f'{op}$', ','] + infix[skip_haakjes(infix, positie-1):] # linkerdeel invoegen

    while '(' in infix: # onnodige haakjesparen verwijderen (de buffer aan de buitenkant blijft zeker over)
        positie = infix.index('(')
        if skip_haakjes(infix, positie+1) == skip_haakjes(infix, positie)-1: # kijkt of het teken erna een nutteloos hakenpaar vormt
            del infix[skip_haakjes(infix, positie)] # verwijdert nutteloos paar
            del infix[positie]
        infix[positie] = '($'

    infix = [i.replace('$', '') for i in infix] # alle dollartekens weghalen
    return infix

# testblok
def main():
    #expression = input('Geef een uitdrukking (geen functies): ')
    expression = ['sin', '(', '5', '*', 'pi', ')']
    expression = [e for e in expression]
    print(''.join(in2tree(expression)))

if __name__ == '__main__':
    main()