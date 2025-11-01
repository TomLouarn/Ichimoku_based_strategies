"""
L'idée de ce code est de déterminer quel est le meilleur voyage possible
compte tenu d'un budget et d'une durée déterminée.
"""

import math
from pprint import pprint

# ======================
#   DONNÉES DE BASE
# ======================
cities = [
    {"city": "Paris",  "flight": 200, "hotel": 20, "car": 200},
    {"city": "London", "flight": 250, "hotel": 30, "car": 120},
    {"city": "Dubai",  "flight": 370, "hotel": 15, "car": 80},
    {"city": "Mumbai", "flight": 450, "hotel": 10, "car": 70},
]

# ======================
#   FONCTIONS DE BASE
# ======================

def final_price(city_row: dict, duration: int) -> float:
    """
    Calcule le coût total pour une ville donnée et une durée donnée.
    """
    flight = city_row["flight"]
    hotel  = city_row["hotel"] * duration
    car    = city_row["car"] * math.ceil(duration / 7)  # semaine commencée
    return flight + hotel + car


def cheapest_city(duration: int):
    """
    Trouve la ville la moins chère pour une durée donnée.
    """
    best_row = min(cities, key=lambda row: final_price(row, duration))
    return best_row["city"], final_price(best_row, duration)


def most_expensive_city(duration: int):
    """
    Trouve la ville la plus chère pour une durée donnée.
    """
    worst_row = max(cities, key=lambda row: final_price(row, duration))
    return worst_row["city"], final_price(worst_row, duration)


# ======================
#   ENTRÉES UTILISATEUR
# ======================

def number_of_days():
    """
    Demande à l'utilisateur un nombre de jours (entier positif).
    """
    while True:
        try:
            days = int(input("Combien de jours de vacances ? "))
            if days < 0:
                print("Veuillez renseigner un entier positif.")
                continue
            return days
        except ValueError:
            print("Veuillez renseigner un entier positif.")


def budget():
    """
    Demande à l'utilisateur son budget (entier positif).
    """
    while True:
        try:
            budg = int(input("Quel est votre budget ? "))
            if budg < 0:
                print("Veuillez renseigner un entier positif.")
                continue
            return budg
        except ValueError:
            print("Veuillez renseigner un entier positif.")


# ======================
#   VERSION 1 — BOUCLE WHILE
# ======================

def max_days_slow(budget: int):
    """
    Pour un budget donné, calcule le nombre maximum de jours abordables
    dans chaque ville, à l’aide d’une simple boucle `while`.
    """
    results = []

    for row in cities:
        d = 0
        # On augmente d tant que le prix reste <= budget
        while final_price(row, d) <= budget:
            d += 1
        # d dépasse la limite → on prend d-1
        results.append((row["city"], max(0, d - 1)))

    # Extraction des séjours les plus longs et plus courts
    max_d = max(results, key=lambda x: x[1])[1]
    min_d = min(results, key=lambda x: x[1])[1]
    longest  = [r for r in results if r[1] == max_d]
    shortest = [r for r in results if r[1] == min_d]

    return results, longest, shortest


# ======================
#   VERSION 2 — RECHERCHE BINAIRE (ARBRE DICHOTOMIQUE)
# ======================

def max_days_fast(budget: int):
    """
    Même résultat que max_days_slow(), mais méthode de recherche binaire :
    on divise l’intervalle [0, 365] en deux à chaque étape pour aller plus vite.
    """
    results = []

    for row in cities:
        lo, hi = 0, 365  # bornes de recherche (0 à 365 jours)
        while lo < hi:
            mid = (lo + hi + 1) // 2  # milieu (biaisé vers le haut)
            if final_price(row, mid) <= budget:
                lo = mid  # mid abordable → on tente plus grand
            else:
                hi = mid - 1  # mid trop cher → on réduit
        results.append((row["city"], lo))

    # Extraction des séjours les plus longs et plus courts
    max_d = max(results, key=lambda x: x[1])[1]
    min_d = min(results, key=lambda x: x[1])[1]
    longest  = [r for r in results if r[1] == max_d]
    shortest = [r for r in results if r[1] == min_d]

    return results, longest, shortest


# ======================
#   PROGRAMME PRINCIPAL
# ======================

if __name__ == "__main__":

    n = number_of_days()
    b = budget()

    print("\n=== Comparaison des coûts pour", n, "jours ===")
    print("→ Moins chère :", cheapest_city(n))
    print("→ Plus chère  :", most_expensive_city(n))

    print("\n=== Version lente (boucle while) ===")
    results, longest, shortest = max_days_slow(b)
    pprint(results)
    print("→ Séjour le plus long :", longest)
    print("→ Séjour le plus court :", shortest)

    print("\n=== Version rapide (recherche binaire) ===")
    results, longest, shortest = max_days_fast(b)
    pprint(results)
    print("→ Séjour le plus long :", longest)
    print("→ Séjour le plus court :", shortest)
