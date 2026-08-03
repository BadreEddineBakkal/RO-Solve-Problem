import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

def run_kruskal(donnees):
    try:

        type_graphe = donnees['type_graphe']
        arcs = donnees['arcs']

        if type_graphe == 'oriente':
            return {"succes": False, "message": "Kruskal nécessite un graphe Non-Orienté (Désactivez les flèches)."}

        G = nx.Graph()

        for arc in arcs:
            u = arc['src']
            v = arc['dest']
            w = float(arc['poids'])
            G.add_edge(u, v, weight=w)

        MST = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
        
        
        poids_total = 0
        for edge in MST.edges(data=True):
            data_arc = edge[2] 
            poids_total = poids_total + data_arc['weight']
            
       
        message_resultat = "Kruskal : L'Arbre Couvrant Minimum (MST) a été trouvé. Coût total = " + str(poids_total)
        
        
        arcs_a_colorer = []
        for edge in MST.edges():
            arcs_a_colorer.append(edge)

        
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#000f1e')
        ax.set_facecolor('#000f1e')

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='#005b96', 
                node_size=1500, font_size=14, font_color='white', font_weight='bold', 
                edge_color='#b3cde0', width=1.5, arrowsize=20)

        
        arcs_inverses = []
        for edge in arcs_a_colorer:
            u = edge[0]
            v = edge[1]
            arcs_inverses.append((v, u))
            
        for edge in arcs_inverses:
            arcs_a_colorer.append(edge)
            
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=arcs_a_colorer, edge_color='#00e5ff', width=3.5)
        
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

    except Exception as e:
        return {"succes": False, "message": "Erreur dans Kruskal: " + str(e)}