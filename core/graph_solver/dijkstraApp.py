import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

def run_dijkstra(donnees):
    try:
        type_graphe = donnees['type_graphe']
        arcs = donnees['arcs']
        depart = donnees['noeud_depart']
        arrivee = donnees['noeud_arrivee']

        if type_graphe == 'oriente':
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        for arc in arcs:
            u = arc['src']
            v = arc['dest']
            w = float(arc['poids'])
            G.add_edge(u, v, weight=w)

        longueur = nx.shortest_path_length(G, source=depart, target=arrivee, weight='weight', method='dijkstra')
        chemin = nx.shortest_path(G, source=depart, target=arrivee, weight='weight', method='dijkstra')
        
        chemin_str = ""
        for i in range(len(chemin)):
            chemin_str += str(chemin[i])
            if i < len(chemin) - 1:
                chemin_str += " ➔ "
                
        message_resultat = "Dijkstra : Plus court chemin de " + str(depart) + " à " + str(arrivee) + " est " + chemin_str + " (Coût: " + str(longueur) + ")"
        
        arcs_a_colorer = []
        for i in range(len(chemin) - 1):
            noeud_actuel = chemin[i]
            noeud_suivant = chemin[i+1]
            arcs_a_colorer.append((noeud_actuel, noeud_suivant))

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#000f1e')
        ax.set_facecolor('#000f1e')

        pos = nx.spring_layout(G, seed=42)

        nx.draw(G, pos, ax=ax, with_labels=True, node_color='#005b96', 
                node_size=1500, font_size=14, font_color='white', font_weight='bold', 
                edge_color='#b3cde0', width=1.5, arrowsize=20)

        if type_graphe == 'non_oriente':
            arcs_inverses = []
            for edge in arcs_a_colorer:
                u = edge[0]
                v = edge[1]
                arcs_inverses.append((v, u))
                
            for edge in arcs_inverses:
                arcs_a_colorer.append(edge)
            
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=arcs_a_colorer, 
                               edge_color='#00e5ff', width=3.5, arrowsize=25)

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

    except nx.NetworkXNoPath:
        return {"succes": False, "message": "Dijkstra : Aucun chemin entre " + str(depart) + " et " + str(arrivee) + "."}
    except Exception as e:
        return {"succes": False, "message": "Erreur dans Dijkstra: " + str(e)}