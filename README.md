# RO Solve Problem

Application web développée avec **Flask** pour résoudre des problèmes de **Recherche Opérationnelle (RO)** : Programmation Linéaire et Théorie des Graphes, avec visualisation graphique des résultats.

## Fonctionnalités

### 📈 Programmation Linéaire
- **Méthode Algébrique (Simplexe)** : résolution via `scipy.optimize.linprog`, pour un nombre de variables et de contraintes quelconque.
- **Méthode Graphique** : résolution visuelle en 2D (2 variables) avec tracé des contraintes, de la zone des solutions admissibles et du point optimal.
- Maximisation ou minimisation, saisie dynamique du nombre de variables et de contraintes.

### 🕸️ Théorie des Graphes
- **Dijkstra** : plus court chemin (poids positifs).
- **Bellman-Ford** : plus court chemin (tolère les poids négatifs).
- **Kruskal** : arbre couvrant minimum (graphe non-orienté).
- **Ford-Fulkerson** : flot maximum (graphe orienté).
- Génération automatique d'une visualisation du graphe avec mise en évidence du résultat (chemin, arbre ou flot).

## Stack technique

- **Backend** : Python, Flask
- **Calcul scientifique** : SciPy, NumPy
- **Graphes** : NetworkX
- **Visualisation** : Matplotlib (rendu en image encodée en base64, envoyée au frontend)
- **Frontend** : HTML / CSS / JavaScript (vanilla)

## Structure du projet

```
RO_SloverProblem/
├── app.py                     # Point d'entrée Flask (routes pages + API)
├── core/
│   ├── linear_solver/
│   │   ├── algebrique.py      # Résolution PL par le Simplexe (scipy)
│   │   └── graphique.py       # Résolution PL par méthode graphique 2D
│   └── graph_solver/
│       ├── dijkstraApp.py
│       ├── bellmanFord.py
│       ├── kruskalApp.py
│       └── fordFulkerson.py
├── templates/
│   ├── home.html
│   ├── pagePL.html
│   └── pageGRAPHE.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/
├── requirements.txt
└── README.md
```

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/<votre-nom-utilisateur>/RO_SloverProblem.git
cd RO_SloverProblem
```

2. Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

L'application démarre sur [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Utilisation

- **Page d'accueil** : choisir entre "PL Problem" et "GRAPH Problem".
- **Programmation Linéaire** : définir le type d'optimisation, le nombre de variables et de contraintes, saisir les coefficients, puis lancer la résolution algébrique ou graphique (graphique disponible uniquement pour 2 variables).
- **Théorie des Graphes** : définir le type de graphe (orienté/non-orienté), ajouter les arcs (source, destination, poids), choisir un algorithme (Dijkstra, Bellman-Ford, Kruskal, Ford-Fulkerson) et lancer la résolution.

## API

| Route | Méthode | Description |
|---|---|---|
| `/api/pl/algebrique` | POST | Résout un programme linéaire (Simplexe) |
| `/api/pl/graphique` | POST | Résout un programme linéaire (méthode graphique 2D) |
| `/api/graphe/resoudre` | POST | Résout un problème de graphe selon l'algorithme choisi |

## Auteur

Projet réalisé dans le cadre d'un cours de Recherche Opérationnelle.
