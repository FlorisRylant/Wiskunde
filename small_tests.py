lijst = ['a', '-', 'b', ',', '-', 'c', ')']
print(lijst[3::-1])
print(lijst.index('-'))
print(len(lijst)-1-lijst[::-1].index('-'))