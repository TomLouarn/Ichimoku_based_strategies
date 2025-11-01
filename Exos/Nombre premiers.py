""" L'objectif de ce code est de familiariser avec des noyaux de bases
    de Python grâce à la manipulation des nombre premiers"""

import math

def is_prime(n: int) -> bool :
    """ Renvoie True si n is a prime et False si n is a composite """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n))+1, 2) :
        if n % i == 0:
            break
    else:
        return True
    return False

n = int(input("Quel nombre ? "))
print(f"{n} est un nombre premier ? {is_prime(n)}")

def first_prime_above(n = 100) -> int :
    i = n
    while is_prime(i) is False:
        i += 1
    return i

k = int(input("Supérieur à quel nombre ? "))
print(f"Le premier nombre premier supérieur à {k} est : {first_prime_above(k)}")

""" Crible d'Eratosthène"""

def crible(n:int) -> list[int] :
    if n < 2:
        return []

    is_prime_list = [True] * (n+1)
    is_prime[0] = is_prime_list[1] = False

    p = 2
    while p*p <= n :
        if is_prime_list[p]:
            for m in range(p*p, n+1, p):
                is_prime_list[m] = False
        p +=1

    return [i for i in range(2, n+1) if is_prime_list[i]]

i = int(input("Crible d'Eratostène jusqu'à quel nombre ?"))
print(crible(i))


"""Premier nombre premier en dessous d'un certain nombre"""

def is_prime(n:int) -> bool:
    if n<2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, int(math.sqrt(n))+1,2):
            if n % i == 0:
                break
        else :
            return True
    return False

P1 = is_prime(13)
P2 = is_prime(14)
P3 = is_prime(21)

print(P1, P2, P3)

def list_prime(n:int) -> list[int] :
    if n<2:
        return []
    else:
        primes = []
        for i in range(2, n+1):
            if is_prime(i) is True:
                primes.append(i)
        return primes

Test = list_prime(13)
print(Test)

def first_prime_belox(n: int = 100) -> int :
    return list_prime(n)[-1]

Test = first_prime_below(100)
print(Test)