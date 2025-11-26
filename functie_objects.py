from IOmaths.data import functions, operators

class Functie:
    def __init__(self, operator, *argumenten):
        self.__op = operator
        if type(argumenten) != tuple:
            argumenten = tuple(argumenten)
        self.__args = argumenten
        self.__onbekendes = set()
        for arg in self.__args:
            self.__onbekendes = self.__onbekendes.union(arg.get_onbekendes())

    def get_onbekendes(self): # geeft een set met alle onbekendes in de functie
        return self.__onbekendes
    
    def __call__(self, *vars): # vars is een dictionary met alle onbekendes, kan ook omzetten naar de dict
        if len(vars) == 1 and type(vars[0]) == dict:
            args = tuple([arg(vars[0]) for arg in self.__args]) # de argumenten, allemaal voor de gegeven waardes
            if self.__op == '+':
                return args[0] + args[1]
            if self.__op == '*':
                return args[0] * args[1]
            if self.__op == '^':
                return args[0] ** args[1]

            if self.__op in functions:
                return functions[self.__op]['f'](args)
            
        elif type(vars) == tuple or type(vars) == list:
            if len(vars) == len(self.__onbekendes):
                variabelen = {}
                for i, key in enumerate(sorted(self.__onbekendes)):
                    variabelen[key] = vars[i]
                return self(variabelen)
            raise KeyError(f"{len(self.__onbekendes)} onbekendes, {len(vars)} gegevens")
        elif type(vars) != dict:
            if len(self.__onbekendes) == 1:
                try:
                    return self(float(vars))
                except:
                    raise ValueError(f"{vars} past niet in de functie")
            raise ValueError(f"Meer dan 1 variabele gevraagd, 1 gegeven")
        
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
    

class Constante(Functie):
    def __init__(self, waarde):
        self.__val = float(waarde) # val kan een float of int zijn
        if self.__val%1 < 0.00005:
            self.__val = int(waarde)

    def __call__(self, vars):
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
    
    def __call__(self, vars):
        if self.__naam in vars:
            if isinstance(vars[self.__naam], str):
                return float(vars[self.__naam])
            return vars[self.__naam]
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
    y = Onbekende('y')
    f = Functie('min', a + b*x, y, a)
    print(f)
    print(f(0, 1))
    print(f({'y':10, 'x':5}))
    print(f.treerepr())

if __name__ == '__main__':
    main()