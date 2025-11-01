# portefeuille_fonctions_main.py
# ------------------------------------------------------------
# Objectif :
# Télécharger les prix d'actions Yahoo Finance,
# demander combien d'actions on détient,
# calculer la valeur du portefeuille,
# et tracer la courbe correspondante.
# ------------------------------------------------------------

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Liste des 10 plus grandes entreprises américaines (tickers Yahoo Finance)
DEFAULT_TOP10_US = ["NVDA","MSFT","AAPL","GOOGL","AMZN","JPM","META","TSLA","AVGO","LLY"]

# ------------------------------------------------------------
# 1️⃣ FONCTION : Télécharger les prix
# ------------------------------------------------------------
def get_prices(tickers, period="1y", interval="1d"):
    """
    Télécharge les prix ajustés (Close) depuis Yahoo Finance
    et renvoie un tableau (DataFrame) : dates × tickers.
    """
    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,   # ajuste les dividendes et splits
        progress=False
    )

    close = data["Close"]  # on garde juste la colonne des prix de clôture

    # Si un seul ticker → transformer en DataFrame pour garder le même format
    if isinstance(close, pd.Series):
        col_name = tickers if isinstance(tickers, str) else tickers[0]
        close = close.to_frame(name=col_name)

    close = close.dropna(how="all")  # supprime les lignes vides
    return close


# ------------------------------------------------------------
# 2️⃣ FONCTION : Demander les quantités détenues
# ------------------------------------------------------------
def ask_shares(tickers):
    """
    Demande à l'utilisateur combien d'actions il détient pour chaque ticker.
    Entrée vide = 0.
    """
    print("\nQuantités détenues :")
    shares = {}
    for t in tickers:
        s = input(f"  {t} : ").strip()
        shares[t] = float(s) if s else 0.0
    return shares


# ------------------------------------------------------------
# 3️⃣ FONCTION : Calculer la valeur du portefeuille dans le temps
# ------------------------------------------------------------
def portfolio_series(prices: pd.DataFrame, shares: dict) -> pd.Series:
    """
    Calcule la valeur du portefeuille à chaque date :
    somme( prix[ticker] × quantité[ticker] ).
    """
    s = pd.Series(shares).reindex(prices.columns).fillna(0.0)
    port = (prices * s).sum(axis=1)
    port.name = "Portfolio"
    return port


# ------------------------------------------------------------
# 4️⃣ FONCTION : Tableau récapitulatif du dernier jour
# ------------------------------------------------------------
def recap_table_last_day(prices: pd.DataFrame, shares: dict) -> pd.DataFrame:
    """
    Crée un tableau indiquant :
    - le dernier prix de chaque action
    - la quantité détenue
    - la valeur correspondante (prix × quantité)
    """
    last = prices.iloc[-1]  # dernière ligne = derniers prix connus
    recap = pd.DataFrame({
        "Price": last,
        "Qty": pd.Series(shares),
        "Value": last * pd.Series(shares)
    }).fillna(0.0).sort_values("Value", ascending=False)
    return recap


# ------------------------------------------------------------
# 5️⃣ FONCTION : Tracer la valeur du portefeuille
# ------------------------------------------------------------
def plot_portfolio(port: pd.Series):
    """Trace la courbe d'évolution de la valeur totale du portefeuille."""
    plt.figure(figsize=(10,5))
    plt.plot(port.index, port.values)
    plt.title("Valeur du portefeuille")
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 6️⃣ FONCTION PRINCIPALE : main()
# ------------------------------------------------------------
def main():
    """
    Fonction principale = le cœur du programme.
    Elle appelle toutes les autres étapes dans l'ordre logique.
    """
    print("=== Portefeuille mégacaps US (Yahoo Finance) ===")

    # Choix des paramètres de base
    period = input("Période ? (ex: 1y, 6mo, 3mo) [1y]: ").strip() or "1y"
    interval = input("Intervalle ? (1d, 1wk, 1mo) [1d]: ").strip() or "1d"
    tickers =  DEFAULT_TOP10_US

    # 1) Télécharger les prix
    prices = get_prices(tickers, period=period, interval=interval)
    print("\nTickers téléchargés :", ", ".join(prices.columns))
    print(prices.tail(9))

    # 2) Saisie des quantités
    shares = ask_shares(prices.columns.tolist())
    print("\nQuantités :", shares)

    # 3) Calculer la valeur du portefeuille
    port = portfolio_series(prices, shares)
    valeur_totale = float(port.iloc[-1])
    print(f"\nValeur actuelle du portefeuille : ${valeur_totale:,.2f}")

    # 4) Afficher un tableau récapitulatif du dernier jour
    recap = recap_table_last_day(prices, shares)
    with pd.option_context("display.float_format", "{:,.2f}".format):
        print("\n--- Récapitulatif ---")
        print(recap)

    # 5) Tracer la courbe
    plot_portfolio(port)


# ------------------------------------------------------------
# 7️⃣ Point d’entrée du script
# ------------------------------------------------------------
# Grâce à cette condition, le code s’exécute *seulement*
# si tu lances ce fichier directement (et pas quand tu l’importes ailleurs).
if __name__ == "__main__":
    main()
