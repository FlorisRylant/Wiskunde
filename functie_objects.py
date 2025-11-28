from IOmaths.data import functions, operators
from math import pi, e, tau
from matplotlib import pyplot as plt
constantes = {'pi':pi, 'e':e, 'tau':tau}

class Functie:
    """
    Functie-class:
    structuur: operator / functie (je kan een binaire operator ook zien als functie) en argumenten
    => Parent-class van Onbekende en Constante omdat die een groot deel hetzelfde doen als Functie
    self.__op = operator / functie
    self.__args = tuple met argumenten, allemaal van het type Functie, Constante of Onbekende

    METHODS:
    intern:
    get_onbekendes() -> geeft een lijst met alle onbekendes in die functie
    treerepr() -> geeft de tree-notatie: robuuster dan infix, gemakkelijker voor computers en vrij simpel om te zetten

    extern:
    __call__(*vars) -> vult de variabelen in in de functie en heeft de output in een int/float
    de normale bewerkingen tussen functies (+, -, *, / en **) -> geven een Functie-object terug
    __str__() -> functie in basic infixnotatie
    __repr__() -> informatie over de functie, slecht leesbaar bij ingewikkelde structuren
    """
    def __init__(self, operator, *argumenten):
        self.__op = operator
        if type(argumenten) != list:
            argumenten = list(argumenten)
        if self.__op in operators: # kijkt of hij de operator moet vervangen door het inverse
            if self.__op == '-':
                argumenten[1] = Functie('*', Constante(-1), argumenten[1])
                self.__op = '+'
            elif self.__op == '/':
                argumenten[1] = Functie('^', argumenten[1], Constante(-1),)
                self.__op = '*'
        self.__args = tuple(argumenten)
        self.__onbekendes = set()
        for arg in self.__args:
            self.__onbekendes = self.__onbekendes.union(arg.get_onbekendes())

    def get_onbekendes(self): # geeft een set met alle onbekendes in de functie
        return self.__onbekendes
    
    def __call__(self, *vartuple, **vardict): # vars is een dictionary met alle onbekendes, kan ook omzetten naar de dict
        vars = constantes | vardict # voegt de constantes bij de vardict om de variabelen samen te krijgen
        if set(vars.keys()).issuperset(self.get_onbekendes()): # kijkt of alles gegeven is
            args = tuple([arg(0, **vars) for arg in self.__args]) # de argumenten, allemaal voor de gegeven waardes
            if self.__op == '+':
                return args[0] + args[1]
            if self.__op == '*':
                return args[0] * args[1]
            if self.__op == '^':
                if (args[0])**2 < 0.000001:
                    return 0
                return args[0] ** args[1]

            if self.__op in functions:
                return functions[self.__op]['f'](*args)
            raise NameError(f'Operator {self.__op} niet gevonden')
        
        vars = {}
        for c in constantes:
            vars[c] = constantes[c]
        if len(vartuple) == len(self.get_onbekendes()): # als ook de constanten zoals pi gegeven zijn
            for i, geg in enumerate(sorted(self.get_onbekendes())):
                vars[geg] = vartuple[i]
        elif len(vartuple) == len(self.get_onbekendes().difference(vars.keys())): # als enkel de echte variabelen gegeven zijn
            for i, geg in enumerate(sorted(self.get_onbekendes().difference(vars.keys()))): # voegt alle anderen toe
                vars[geg] = vartuple[i]
        else:
            raise IOError(f'Gegevens {vartuple} en {vardict} zijn ongeldig.')
        return self(0, **vars)

    def __add__(self, other):
        if isinstance(other, Functie):
            return Functie('+', self, other)
        raise TypeError(f'Kan type {type(other)} niet als functie interpreteren.')
    
    def __mul__(self, other):
        if isinstance(other, Functie):
            return Functie('*', self, other)
        raise TypeError(f'Kan type {type(other)} niet als functie interpreteren.')

    def __pow__(self, other):
        if isinstance(other, Functie):
            return Functie('^', self, other)
        raise TypeError(f'Kan type {type(other)} niet als functie interpreteren.')

    def __sub__(self, other):
        if isinstance(other, Functie):
            return Functie('+', self, Functie('*', Constante(-1), other))
        raise TypeError(f'Kan type {type(other)} niet als functie interpreteren.')
    
    def __truediv__(self, other):
        if isinstance(other, Functie):
            return Functie('*', self, Functie('^', Constante(-1), other))
        raise TypeError(f'Kan type {type(other)} niet als functie interpreteren.')

    def __str__(self):
        if self.__op in '+*^':
            return f"({self.__args[0]}{self.__op}{self.__args[1]})"
        out = str(self.__op) + '('
        for arg in self.__args:
            out += str(arg)
            out += ', '
        out = out[:-2] + ')'
        return out

    def __repr__(self):
        out = f"Functie({self.__op}):\n- "
        for arg in self.__args:
            out += str(arg)
            out += '\n- '
        out = out[:-2] + "Variabelen: " + ', '.join(self.__onbekendes)
        return out
    
    def treerepr(self): # omzetten naar interpreteerbare treecode
        out = self.__op + '('
        for a in self.__args:
            out += a.treerepr() + ','
        return out[:-1] + ')'
    
    def simplified(self): # dit gaat een totaal stort worden op vlak van pointers
        arg = []
        for a in enumerate(self.__args):
            arg.append(a.simplified())
        if min([type(a)==Constante for a in arg]): # kijkt of alle argumenten constanten zijn
            return Constante(self(0)) # geeft simpele vorm terug
        return self
    
    def grafiek(self, x_lims=(-10, 10), y_lims=(-10, 10), n=200):
        plt.cla()
        X = [x_lims[0] + i*(x_lims[1]-x_lims[0])/n for i in range(n+1)]
        try:
            Y = [self(x) for x in X]
        except:
            raise IOError(f'Kan geen 2D-grafiek maken van deze functie.')
        plt.plot(X, Y)
        plt.ylim(*y_lims)
        plt.xlim(*x_lims)
        plt.show()
    

class Constante(Functie):
    def __init__(self, waarde):
        self.__val = float(waarde) # val kan een float of int zijn
        if self.__val%1 < 0.00005:
            self.__val = int(waarde)

    def __call__(self, *args, **kwargs):
        return self.__val
    
    def __str__(self):
        return str(self.__val)
    
    def __repr__(self):
        return f"Constante({self.__val})"
    
    def get_onbekendes(self):
        return set()
    
    def treerepr(self):
        return str(self.__val)
    
    def simplified(self):
        return self


class Onbekende(Functie):
    def __init__(self, naam):
        self.__naam = naam # moet een string zijn
    
    def __call__(self, *args, **kwargs):
        if self.__naam in kwargs:
            if isinstance(kwargs[self.__naam], str):
                return float(kwargs[self.__naam])
            return kwargs[self.__naam]
        raise KeyError(f"Variabele {self.__naam} niet gegeven")
    
    def __str__(self):
        return self.__naam
    
    def __repr__(self):
        return f"Onbekende({self.__naam})"
    
    def get_naam(self):
        return self.__naam
    
    def __eq__(self, other):
        return self.__naam == other.get_naam()
    
    def __lt__(self, other):
        return self.__naam < other.get_naam()
    
    def get_onbekendes(self): # om de onbekendes te laten opzalmen
        return {self.__naam}

    def treerepr(self):
        return self.__naam
    
    def simplified(self):
        return self


def main():
    a = Constante(2)
    b = Constante(-4)
    x = Onbekende('x')
    f = Functie('min', a + b*x, x, a)
    print(f)
    print(f(5))
    print(f.treerepr())
    f.grafiek()

if __name__ == '__main__':
    main()