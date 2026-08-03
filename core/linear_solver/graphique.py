import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from core.linear_solver.algebrique import resoudre_programme_lineaire
import matplotlib

matplotlib.use('Agg') 

def resoudre_programme_graphique(coefficients_objectif, matrice_ressources, limites_ressources, type_optimisation):
    try:
        resultat_algebrique = resoudre_programme_lineaire(
            coefficients_objectif, matrice_ressources, limites_ressources, type_optimisation
        )
        
        if not resultat_algebrique['succes']:
            return resultat_algebrique

        fig, ax = plt.subplots(figsize=(8, 6))
        
        max_val = 50 
        if len(limites_ressources) > 0:
            plus_grand_chiffre = max(limites_ressources)
            if plus_grand_chiffre > 0:
                max_val = plus_grand_chiffre
        
        x_vals = np.linspace(0, max_val, 400)
        
        for i in range(len(limites_ressources)):
            a1 = matrice_ressources[i][0]
            a2 = matrice_ressources[i][1]
            b = limites_ressources[i]
            
            if a2 != 0:
                # a1*x1 + a2*x2 <= b  ==>  x2 = (b - a1*x1) / a2
                y_vals = (b - a1 * x_vals) / a2
                ax.plot(x_vals, y_vals, label=f'Contrainte {i+1}')
                ax.fill_between(x_vals, 0, y_vals, alpha=0.1) 
            else:
                ax.axvline(x=b/a1, label=f'Contrainte {i+1}', color='red')
        
        
        opt_x1 = resultat_algebrique['valeurs_variables'][0]
        opt_x2 = resultat_algebrique['valeurs_variables'][1]
        
        ax.plot(opt_x1, opt_x2, 'r*', markersize=15, label='Point Optimal')
        

        valeur_z = resultat_algebrique["valeur_z_optimale"]
        texte_z = f'Z = {valeur_z}'
        ax.annotate(texte_z, (opt_x1, opt_x2), textcoords="offset points", xytext=(10,10), ha='center')

        
        ax.set_xlim((0, max_val))
        ax.set_ylim((0, max_val))
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_title('Méthode Graphique (Zone des solutions)')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        
        
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        
       
        donnees_image = img.getvalue()                        
        image_encodee = base64.b64encode(donnees_image)       
        plot_url = image_encodee.decode('utf8')               
        
        plt.close()

        return {
            "succes": True,
            "message": "Solution Graphique générée.",
            "valeur_z_optimale": resultat_algebrique['valeur_z_optimale'],
            "valeurs_variables": resultat_algebrique['valeurs_variables'],
            "image_url": f"data:image/png;base64,{plot_url}"
        }

    except Exception as e:
        return {"succes": False, "message": f"Erreur Graphique: {str(e)}"}