from flask import Flask, render_template, request, jsonify
import traceback

# =====================================================================
# IMPORTATION DYAL LES MODULES (L'Architecture dyalk)
# =====================================================================

# 1. Module de Programmation Linéaire (PL)
try:
    from core.linear_solver.algebrique import resoudre_programme_lineaire
    from core.linear_solver.graphique import resoudre_programme_graphique
except ImportError as e:
    print(f"⚠️ Attention: Problème d'importation dans le module PL: {e}")

# 2. Module de Théorie des Graphes
try:
    from core.graph_solver.dijkstraApp import run_dijkstra
    from core.graph_solver.bellmanFord import run_bellman
    from core.graph_solver.kruskalApp import run_kruskal
    from core.graph_solver.fordFulkerson import run_ford
except ImportError as e:
    print(f"⚠️ Attention: Problème d'importation dans le module Graphes: {e}")


app = Flask(__name__)

# =====================================================================
# ROUTES DYAL L'INTERFACE FRONTEND (Les pages HTML)
# =====================================================================

@app.route('/')
def home():
    """Route dyal l'page d'accueil (Le Menu Principal)"""
    return render_template('home.html')

@app.route('/programmation-lineaire')
def page_pl():
    """Route dyal l'interface de Programmation Linéaire"""
    return render_template('pagePL.html')

@app.route('/theorie-des-graphes')
def page_graphe():
    """Route dyal l'interface de Théorie des Graphes"""
    return render_template('pageGRAPHE.html')


# =====================================================================
# ROUTES DYAL L'API BACKEND (L'Calcul w Rsim)
# =====================================================================

# --- API 1: Programmation Linéaire (Méthode du Simplexe / Algébrique) ---
@app.route('/api/pl/algebrique', methods=['POST'])
def api_pl_algebrique():
    try:
        donnees = request.json
        reponse = resoudre_programme_lineaire(
            coefficients_objectif=donnees.get('coefficients_objectif'),
            matrice_ressources=donnees.get('matrice_ressources'),
            limites_ressources=donnees.get('limites_ressources'),
            type_optimisation=donnees.get('type_optimisation')
        )
        return jsonify(reponse)
    except Exception as e:
        print(traceback.format_exc()) # Kat-biyyen l'erreur f l'terminal
        return jsonify({"succes": False, "message": f"Erreur Serveur (Simplexe): {str(e)}"})


# --- API 2: Programmation Linéaire (Méthode Graphique 2D) ---
@app.route('/api/pl/graphique', methods=['POST'])
def api_pl_graphique():
    try:
        donnees = request.json
        reponse = resoudre_programme_graphique(
            coefficients_objectif=donnees.get('coefficients_objectif'),
            matrice_ressources=donnees.get('matrice_ressources'),
            limites_ressources=donnees.get('limites_ressources'),
            type_optimisation=donnees.get('type_optimisation')
        )
        return jsonify(reponse)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"succes": False, "message": f"Erreur Serveur (PL Graphique): {str(e)}"})


# --- API 3: Théorie des Graphes (Routeur Dynamique) ---
@app.route('/api/graphe/resoudre', methods=['POST'])
def api_graphe_resoudre():
    try:
        donnees = request.json
        algo = donnees.get('algo_graphe')

        # L'Mowajih (Router): Kiy-sifet l'data l'fichier lli m-kellef b l'algorithme
        if algo == 'dijkstra':
            reponse = run_dijkstra(donnees)
        elif algo == 'bellman':
            reponse = run_bellman(donnees)
        elif algo == 'kruskal':
            reponse = run_kruskal(donnees)
        elif algo == 'ford':
            reponse = run_ford(donnees)
        else:
            return jsonify({"succes": False, "message": "Algorithme non reconnu par le serveur !"})
            
        return jsonify(reponse)
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"succes": False, "message": f"Erreur Serveur (Graphe): {str(e)}"})


# =====================================================================
# LANCEMENT DYAL L'APPLICATION FLASK
# =====================================================================
if __name__ == '__main__':
    # debug=True kat-khelli l'serveur y-dir auto-restart melli t-beddel chi fichier
    app.run(debug=True, port=5000)






# from flask import Flask, render_template, request, jsonify

# # =====================================================================
# # IMPORTATION DYAL LES MODULES
# # =====================================================================

# # 1. Module de Programmation Linéaire (PL)
# from core.linear_solver.algebrique import resoudre_programme_lineaire
# from core.linear_solver.graphique import resoudre_programme_graphique

# # 2. Module de Théorie des Graphes
# from core.graph_solver.dijkstraApp import run_dijkstra
# from core.graph_solver.bellmanFord import run_bellman
# from core.graph_solver.kruskalApp import run_kruskal
# from core.graph_solver.fordFulkerson import run_ford


# app = Flask(__name__)

# # =====================================================================
# # ROUTES DYAL L'INTERFACE FRONTEND (Les pages HTML)
# # =====================================================================

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/programmation-lineaire')
# def page_pl():
#     return render_template('pagePL.html')

# @app.route('/theorie-des-graphes')
# def page_graphe():
#     return render_template('pageGRAPHE.html')


# # =====================================================================
# # ROUTES DYAL L'API BACKEND (L'Calcul w Rsim)
# # =====================================================================

# # --- API 1: Programmation Linéaire (Méthode du Simplexe / Algébrique) ---
# @app.route('/api/pl/algebrique', methods=['POST'])
# def api_pl_algebrique():
#     try:
#         donnees = request.json
        
#         # Kan-jbdou l'arqam b tariqa 3adiya (Tableau)
#         coef_obj = donnees['coefficients_objectif']
#         mat_res = donnees['matrice_ressources']
#         lim_res = donnees['limites_ressources']
#         type_opt = donnees['type_optimisation']
        
#         # Kan-ssiftouhom l-fonction
#         reponse = resoudre_programme_lineaire(coef_obj, mat_res, lim_res, type_opt)
        
#         return jsonify(reponse)
        
#     except Exception as e:
#         print("Erreur Simplexe :", e) # Affichage simple d-l'erreur
#         return jsonify({"succes": False, "message": "Erreur Serveur: " + str(e)})


# # --- API 2: Programmation Linéaire (Méthode Graphique 2D) ---
# @app.route('/api/pl/graphique', methods=['POST'])
# def api_pl_graphique():
#     try:
#         donnees = request.json
        
#         coef_obj = donnees['coefficients_objectif']
#         mat_res = donnees['matrice_ressources']
#         lim_res = donnees['limites_ressources']
#         type_opt = donnees['type_optimisation']
        
#         reponse = resoudre_programme_graphique(coef_obj, mat_res, lim_res, type_opt)
        
#         return jsonify(reponse)
        
#     except Exception as e:
#         print("Erreur Graphique :", e)
#         return jsonify({"succes": False, "message": "Erreur Serveur: " + str(e)})


# # --- API 3: Théorie des Graphes (Routeur Dynamique) ---
# @app.route('/api/graphe/resoudre', methods=['POST'])
# def api_graphe_resoudre():
#     try:
#         donnees = request.json
#         algo = donnees['algo_graphe'] # Blast .get()

#         if algo == 'dijkstra':
#             reponse = run_dijkstra(donnees)
#         elif algo == 'bellman':
#             reponse = run_bellman(donnees)
#         elif algo == 'kruskal':
#             reponse = run_kruskal(donnees)
#         elif algo == 'ford':
#             reponse = run_ford(donnees)
#         else:
#             return jsonify({"succes": False, "message": "Algorithme non reconnu par le serveur !"})
            
#         return jsonify(reponse)
        
#     except Exception as e:
#         print("Erreur Graphe :", e)
#         return jsonify({"succes": False, "message": "Erreur Serveur: " + str(e)})


# # =====================================================================
# # LANCEMENT DYAL L'APPLICATION FLASK
# # =====================================================================
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)