#Implementación de sDES en Python.
import fileinput as fp

#Recuperando las entradas en una lista.
inputs = []

for entrada in fp.input():
    inputs.append(entrada.strip())

print(inputs)