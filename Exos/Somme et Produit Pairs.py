import math

def list_nbr_pairs(n:int = 20) -> list[int]:
    """nombre = list(range(1, n+1))
    return nombre"""
    nombre = [i for i in range(1, n+1) if i % 2 == 0]
    return nombre

print(list_nbr_pairs(20))

def carré (n: int = 20) -> list[int]:
    pairs = [x for x in range (1,21) if x%2 ==0]
    return list(map(lambda x:x*x, pairs))

print(carré())

""" def carré(n) -> list[int]:
    nombre = [i*i for i in range(1,n+1) if i % 2 == 0 """

def somme (n:int = 20) -> int :
    return sum(carré(n))

print(somme(20))

def produit(n:int=20) -> int:
    P = 1
    for val in carré(n):
        P *= val
    return P

print(produit(20))