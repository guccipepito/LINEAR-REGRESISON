# -*- coding: utf-8 -*-
"""

________  ___  ___  ________  ________  ___  ________  _______   ________  ___  _________  ________
|\   ____\|\  \|\  \|\   ____\|\   ____\|\  \|\   __  \|\  ___ \ |\   __  \|\  \|\___   ___\\   __  \
\ \  \___|\ \  \\\  \ \  \___|\ \  \___|\ \  \ \  \|\  \ \   __/|\ \  \|\  \ \  \|___ \  \_\ \  \|\  \
 \ \  \  __\ \  \\\  \ \  \    \ \  \    \ \  \ \   ____\ \  \_|/_\ \   ____\ \  \   \ \  \ \ \  \\\  \
  \ \  \|\  \ \  \\\  \ \  \____\ \  \____\ \  \ \  \___|\ \  \_|\ \ \  \___|\ \  \   \ \  \ \ \  \\\  \
   \ \_______\ \_______\ \_______\ \_______\ \__\ \__\    \ \_______\ \__\    \ \__\   \ \__\ \ \_______\
    \|_______|\|_______|\|_______|\|_______|\|__|\|__|     \|_______|\|__|     \|__|    \|__|  \|_______|


_    _ _  _ ____ ____ ____    ____ ____ ____ ____ ____ ____ ____ _ ____ _  _
|    | |\ | |___ |__| |__/    |__/ |___ | __ |__/ |___ [__  [__  | |  | |\ |
|___ | | \| |___ |  | |  \    |  \ |___ |__] |  \ |___ ___] ___] | |__| | \|

"""

# Installation of necessary libraries
!pip install yfinance scikit-learn matplotlib pandas

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
from datetime import datetime

# Téléchargement des données historiques de l'action
def download_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data['Close'], stock.info['shortName']

# Régression linéaire pour prédire le prix de l'action
def linear_regression_prediction(data, short_name):
    X = np.arange(len(data)).reshape(-1, 1)
    y = data.values.reshape(-1, 1)

    # Normalisation des caractéristiques
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Paramètres pour la recherche de grille
    param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}

    # Régression Ridge avec validation croisée
    ridge = Ridge()
    grid_search = GridSearchCV(ridge, param_grid, cv=5)
    grid_search.fit(X_scaled, y)

    # Meilleurs hyperparamètres
    best_alpha = grid_search.best_params_['alpha']

    # Régression Ridge avec les meilleurs hyperparamètres
    final_ridge = Ridge(alpha=best_alpha)
    final_ridge.fit(X_scaled, y)

    # Prédiction sur la dernière observation
    last_observation = X[-1].reshape(1, -1)
    predicted_price = final_ridge.predict(scaler.transform(last_observation))[0][0]

    # Plot des résultats
    plt.figure(figsize=(10, 6))
    plt.plot(X, y, color='blue', label='Données historiques')
    plt.plot(X, final_ridge.predict(X_scaled), color='red', linestyle='--', label='Régression Ridge (predicted_price: {:.2f})'.format(predicted_price))
    plt.xlabel('Jours')
    plt.ylabel('Prix de l\'action')
    plt.title('Prédiction du prix de l\'action {} avec régression Ridge'.format(short_name))
    plt.legend()
    plt.show()

    return predicted_price

# Paramètres
ticker = 'BFH'  # Ticker de l'action (Microsoft dans cet exemple)
start_date = '2023-01-01'  # Date de début des données historiques
end_date = datetime.now().strftime("%Y-%m-%d")  # Date de fin des données historiques (aujourd'hui)

# Téléchargement des données historiques
stock_data, short_name = download_stock_data(ticker, start_date, end_date)

# Prédiction avec régression linéaire optimisée (Ridge)
predicted_price = linear_regression_prediction(stock_data, short_name)

print("Prix prédit de l'action avec régression Ridge :", predicted_price)
