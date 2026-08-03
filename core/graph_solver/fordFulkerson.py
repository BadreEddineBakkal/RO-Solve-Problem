import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

def run_ford(donnees):
    try:
        
        type_graphe = donnees['type_graphe']
        arcs = donnees['arcs']
        depart = donnees['noeud_depart']
        arrivee = donnees['noeud_arrivee']

        if type_graphe != 'oriente':
            return {"succes": False, "message": "Ford-Fulkerson nécessite un graphe Orienté (avec des flèches)."}

        G = nx.DiGraph()

        
        for arc in arcs:
            u = arc['src']
            v = arc['dest']
            w = float(arc['poids'])
            
            G.add_edge(u, v, capacity=w, weight=w)

        resultat_flot = nx.maximum_flow(G, depart, arrivee)
        valeur_flot = resultat_flot[0]
        dict_flot = resultat_flot[1]
        
        message_resultat = "Ford-Fulkerson : Le flot maximum de " + str(depart) + " à " + str(arrivee) + " est de " + str(valeur_flot)
        
        arcs_a_colorer = []
        for u in dict_flot:
            for v in dict_flot[u]:
                if dict_flot[u][v] > 0:
                    arcs_a_colorer.append((u, v))

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#000f1e')
        ax.set_facecolor('#000f1e')

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='#005b96', 
                node_size=1500, font_size=14, font_color='white', font_weight='bold', 
                edge_color='#b3cde0', width=1.5, arrowsize=20)

        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=arcs_a_colorer, edge_color='#00e5ff', width=3.5, arrowsize=25)
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_color='red', font_size=12)

        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
        img.seek(0)
        
        donnees_image = img.getvalue()
        image_encodee = base64.b64encode(donnees_image)
        plot_url = image_encodee.decode('utf8')
        
        plt.close()

        image_final_url = "data:image/png;base64," + plot_url

        return {
            "succes": True, 
            "message": message_resultat, 
            "image_url": image_final_url
        }

    except nx.NetworkXError:
        message_erreur = "Ford-Fulkerson : Vérifiez que la Source (" + str(depart) + ") et le Puits (" + str(arrivee) + ") existent."
        return {"succes": False, "message": message_erreur}
    except Exception as e:
        return {"succes": False, "message": "Erreur dans Ford-Fulkerson: " + str(e)}