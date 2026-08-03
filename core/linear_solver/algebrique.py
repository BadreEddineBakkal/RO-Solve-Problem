from scipy.optimize import linprog

def resoudre_programme_lineaire(coefficients_objectif, matrice_ressources, limites_ressources, type_optimisation):
    try:
        c = []
        if type_optimisation == 'max':
            for val in coefficients_objectif:
                c.append(-val) 
        else:
            for val in coefficients_objectif:
                c.append(val)
                
        A_ub = matrice_ressources
        b_ub = limites_ressources
        
        bounds = []
        for i in range(len(coefficients_objectif)):
            bounds.append((0, None))
        
        resultat = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if resultat.success:
            if type_optimisation == 'max':
                valeur_z = -resultat.fun
            else:
                valeur_z = resultat.fun
                
            valeurs_x = []
            for x in resultat.x:
                valeurs_x.append(round(x, 2))
            
            return {
                "succes": True,
                "message": "Solution optimale trouvée (Simplexe).",
                "valeur_z_optimale": round(valeur_z, 2),
                "valeurs_variables": valeurs_x
            }
        else:
            return {"succes": False, "message": f"Pas de solution : {resultat.message}"}
            
    except Exception as e:
        return {"succes": False, "message": f"Erreur mathématique: {str(e)}"}