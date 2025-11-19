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
        return out[:-4]
    

class Constante(Functie):
    def __init__(self, waarde):
        self.__val = float(waarde) # val kan een float of int zijn
        if self.__val%1 < 0.00005:
            self.__val = int(waarde)

    def __call__(self, x):
        return self.__val
    
    def __str__(self):
        return str(self.__val)
    
    def __repr__(self):
        return f"Constante({self.__val})"
    
    def get_onbekendes(self):
        return set()


class Onbekende(Functie):
    def __init__(self, naam):
        self.__naam = naam # moet een string zijn
    
    def __call__(self, x):
        return x
    
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


def main():
    a = Constante(2)
    b = Constante(-4)
    x = Onbekende('x')
    f = Functie('min', Functie('+', a, Functie('*', b, x)), a, b)
    print(f)
    print(f.get_onbekendes())

if __name__ == '__main__':
    main()