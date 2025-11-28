from matplotlib import pyplot as plt

X = list(range(10))
Y = [x*x for x in X]
print(X, Y)
plt.plot(X, Y)
plt.show()