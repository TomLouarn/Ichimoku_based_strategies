import random as rd
from typing import List, Tuple


class Carte:
    """
    Représente une carte de Blackjack.

    Attributs
    ---------
    couleur : str
        La “famille” : coeur, carreau, trèfle, pique.
    nom : str
        Le libellé affiché : "as", "2", ..., "roi".
    valeur : int
        La valeur utilisée pour calculer le total d’une main :
        - as = 11 (on l’ajustera à 1 si on dépasse 21)
        - 2..10 = face value
        - valet/dame/roi = 10

    Pourquoi séparer `nom` et `valeur` ?
    ------------------------------------
    - `nom` sert à l'affichage (humain),
    - `valeur` sert au calcul (machine).
    Cela évite d’avoir des dicts imbriqués et simplifie tout le code.
    """

    def __init__(self, couleur: str, nom: str, valeur: int) -> None:
        self.couleur = couleur
        self.nom = nom
        self.valeur = valeur

    def __str__(self) -> str:
        """Affichage propre d’une carte (utilisé par print())."""
        return f"{self.nom} de {self.couleur}"


class Deck:
    """
    Représente un paquet de cartes de 52 cartes.

    Responsabilités
    ---------------
    - Construire les 52 cartes
    - Mélanger le paquet
    - Distribuer N cartes (pop depuis la fin de la liste)

    💡 À retenir
    ------------
    - `rd.shuffle(liste)` mélange sur place.
    - `list.pop()` retire et renvoie le dernier élément (O(1)).
    - On distribue par la fin car c’est très rapide en liste Python.
    """

    def __init__(self) -> None:
        self.cartes: List[Carte] = []

        couleurs: List[str] = ["coeur", "carreau", "trèfle", "pique"]
        # Liste de tuples (nom_affiché, valeur_numérique)
        hauteurs: List[Tuple[str, int]] = [
            ("as", 11),
            ("2", 2), ("3", 3), ("4", 4), ("5", 5),
            ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10),
            ("valet", 10), ("dame", 10), ("roi", 10),
        ]

        # Génération des 52 cartes via produit cartésien
        for c in couleurs:
            for nom, val in hauteurs:
                self.cartes.append(Carte(c, nom, val))

    def shuffle(self) -> None:
        """Mélange le paquet si on a au moins 2 cartes."""
        if len(self.cartes) > 1:
            rd.shuffle(self.cartes)

    def deal(self, number: int) -> List[Carte]:
        """
        Distribue `number` cartes du sommet (fin de la liste).

        Paramètres
        ----------
        number : int
            Combien de cartes on veut tirer.

        Retour
        ------
        List[Carte] : les cartes distribuées (peut être vide si paquet épuisé).
        """
        cartes_melangees: List[Carte] = []
        for _ in range(number):
            if self.cartes:               # évite IndexError si paquet vide
                cartes_melangees.append(self.cartes.pop())
        return cartes_melangees


class Hand:
    """
    Représente la main d’un joueur (ou du dealer).

    Responsabilités
    ---------------
    - Conserver la liste des cartes
    - Calculer la valeur avec la gestion des As (11 -> 1 si besoin)
    - Savoir si la main est un blackjack (exactement 2 cartes valant 21)
    - Afficher la main (avec carte cachée du dealer si nécessaire)

    💡 À retenir (As)
    -----------------
    1) On compte d’abord l’As comme 11.
    2) Si total > 21, on convertit des As en 1 (on enlève 10) jusqu’à repasser ≤ 21
       ou jusqu’à ce qu’il n’y ait plus d’As à convertir.
    """

    def __init__(self, dealer: bool = False) -> None:
        self.cartes: List[Carte] = []
        self.dealer: bool = dealer

    def add_carte(self, cartes_liste: List[Carte]) -> None:
        """
        Ajoute des cartes à la main.

        Pourquoi `extend` et pas `append` ?
        -----------------------------------
        - `extend` ajoute chaque élément d’une liste.
        - `append` ajouterait la **liste entière** comme un seul élément.
        Ici on veut étendre la main avec N cartes individuelles.
        """
        self.cartes.extend(cartes_liste)

    def calcul_valeur(self) -> int:
        """Calcule le total actuel en gérant dynamiquement les As."""
        total = 0
        nb_as = 0

        for carte in self.cartes:
            total += carte.valeur
            if carte.nom == "as":
                nb_as += 1

        # Ajustement des As : 11 -> 1 tant qu'on dépasse 21
        while total > 21 and nb_as > 0:
            total -= 10   # 11 - 10 = 1 (on “rabaisse” un As)
            nb_as -= 1

        return total

    def get_valeur(self) -> int:
        """Expose proprement la valeur courante de la main."""
        return self.calcul_valeur()

    def is_blackjack(self) -> bool:
        """
        Un blackjack = 2 cartes exactement totalisant 21 (As + 10).
        Note : Si on a plus de 2 cartes et 21, ce n’est PAS un blackjack.
        """
        return len(self.cartes) == 2 and self.get_valeur() == 21

    def display(self, show_all_dealer_cards: bool = False) -> None:
        """
        Affiche la main. Si c’est le dealer et qu’on ne doit pas tout montrer,
        on cache sa première carte (sauf si blackjack).

        Paramètres
        ----------
        show_all_dealer_cards : bool
            True pour montrer toutes les cartes du dealer (phase finale),
            False pour cacher la première (phase initiale).
        """
        print(f'''{"Main du Dealer" if self.dealer else "Ta main"} :''')

        for index, carte in enumerate(self.cartes):
            if (index == 0
                and self.dealer
                and not show_all_dealer_cards
                and not self.is_blackjack()):
                print("- Carte cachée")
            else:
                print("-", carte)

        # On affiche la valeur seulement pour le joueur
        if not self.dealer:
            print("Valeur :", self.get_valeur())
        print()


class Game:
    """
    Orchestration d’une partie :
    - demande du nombre de parties
    - boucle parties
    - distribution initiale
    - tour du joueur (hit/stand)
    - tour du dealer (tire jusqu’à 17)
    - évaluation du vainqueur

    💡 À retenir (contrôle de flux)
    -------------------------------
    - `continue` : passe à la partie suivante (boucle) quand l’issue est déjà connue.
    - On isole la logique “qui gagne ?” dans `check_winner` pour clarifier.
    """

    def check_winner(self, player_hand: Hand, dealer_hand: Hand, final: bool = False) -> bool:
        """
        Décide si la partie est terminée et annonce un résultat.

        Paramètres
        ----------
        player_hand : Hand
        dealer_hand : Hand
        final : bool
            False -> détection “immédiate” (bust/blackjack)
            True  -> comparaison finale (après tour du dealer)

        Retour
        ------
        bool : True si on doit arrêter la partie (issue connue).
        """
        if not final:
            # 1) Fin immédiate côté joueur ?
            if player_hand.get_valeur() > 21:
                print("Tu as dépassé 21. Le Dealer gagne.")
                return True
            if player_hand.is_blackjack():
                print("Blackjack ! Tu gagnes 🎉")
                return True
            # 2) Fin immédiate côté dealer ?
            if dealer_hand.is_blackjack():
                print("Blackjack du Dealer... Perdu.")
                return True
            return False

        # Comparaison finale (les deux mains sont “fermées”)
        pv = player_hand.get_valeur()
        dv = dealer_hand.get_valeur()

        if dv > 21:
            print("Le Dealer dépasse 21. Tu gagnes 🎉")
        elif pv > dv:
            print("Gagné !")
        elif pv < dv:
            print("Perdu.")
        else:
            print("Égalité (push).")
        return True

    def play(self) -> None:
        """Boucle principale du jeu (multi-parties)."""
        # ---- Demande robuste du nombre de parties
        game_to_play = 0
        while game_to_play <= 0:
            try:
                game_to_play = int(input("Combien de parties voulez-vous jouer ? "))
            except Exception:
                print("Vous devez renseigner un nombre entier positif.")

        # ---- Boucle des parties
        for game_number in range(1, game_to_play + 1):
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # Distribution initiale (2 cartes chacun)
            player_hand.add_carte(deck.deal(2))
            dealer_hand.add_carte(deck.deal(2))

            # Affichage de début
            print()
            print("*" * 30)
            print(f"Partie {game_number} / {game_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            # Check immédiat (bust/blackjack)
            if self.check_winner(player_hand, dealer_hand):
                continue  # partie terminée, on passe à la suivante

            # ---- Tour du joueur : hit/stand
            while player_hand.get_valeur() < 21:
                choix = input("Voulez-vous une nouvelle carte ? [Non, Oui] ").strip().lower()
                print()

                # Normaliser la réponse
                if choix in {"oui", "o", "yes", "y"}:
                    player_hand.add_carte(deck.deal(1))
                    player_hand.display()

                    # Bust/Blackjack après pioche ?
                    if self.check_winner(player_hand, dealer_hand):
                        break
                elif choix in {"non", "n", "no"}:
                    break
                else:
                    print("Réponds par Oui/O ou Non/N, stp.")

            # Si le joueur a bust, on relance une partie
            if player_hand.get_valeur() > 21:
                continue

            # ---- Tour du Dealer : tire jusqu’à 17 inclus
            print("Tour du Dealer...")
            dealer_hand.display(show_all_dealer_cards=True)

            while dealer_hand.get_valeur() < 17:
                dealer_hand.add_carte(deck.deal(1))
                dealer_hand.display(show_all_dealer_cards=True)

            # Si une issue est évidente, on enchaîne
            if self.check_winner(player_hand, dealer_hand):
                continue

            # ---- Comparaison finale
            print("Résultat final")
            player_hand.display()
            dealer_hand.display(show_all_dealer_cards=True)
            self.check_winner(player_hand, dealer_hand, final=True)

        print("\nMerci d'avoir joué !")


if __name__ == "__main__":
    g = Game()
    g.play()
