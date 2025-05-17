# USD/CHF Live Dashboard

Ce projet propose un tableau de bord web en temps réel pour suivre le cours USD/CHF. Il utilise un script de scraping pour récupérer régulièrement les prix depuis Investing.com, puis affiche ces données via une application Dash avec graphiques et indicateurs clés.

---

## Fonctionnalités

- Récupération automatique du prix USD/CHF toutes les 5 minutes.
- Historique des prix sauvegardé dans un fichier `price.txt`.
- Visualisation interactive des prix dans un graphique.
- Calcul du changement et de la volatilité sur les 7 derniers jours.
- Rapport quotidien affiché dans le dashboard.

---

## Installation et utilisation

1. Cloner le dépôt et se placer dans le dossier :
```bash
git clone https://github.com/ton-utilisateur/ton-depot.git
cd ton-depot

2. Créer et activer un environnement virtuel Python :

python3 -m venv venv
source venv/bin/activate

3. Installer les dépendances Python :

pip install dash pandas numpy plotly
Lancer le script de scraping (à lancer régulièrement, par exemple via cron) :
bash scraper.sh


4. Lancer le dashboard web :

python dashboard.py

5. Accéder au dashboard dans un navigateur à l’adresse :

(http://16.171.17.227:8050/)

6. Description des fichiers

dashboard.py : application Dash affichant le tableau de bord.
scraper.sh : script bash qui récupère le prix USD/CHF depuis Investing.com.
price.txt : fichier généré contenant l’historique des prix.

