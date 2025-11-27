def func(*args, **kwargs):
    gegevens = {'pi':3.1415, 'e':2.78}
    gegevens.update(kwargs)
    print(args, len(args))
    print(gegevens, len(gegevens))

d1 = {'a':5, 'b':3}
d2 = {'c':4, 'b':9}
print(d1, d2)
d3 = d1 | d2
print(d1, d2, d3)