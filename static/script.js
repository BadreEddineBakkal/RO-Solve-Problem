//PL
function genererFormulaire() {
    var numVars = parseInt(document.getElementById('num_vars').value);
    var numCons = parseInt(document.getElementById('num_cons').value);
    var objContainer = document.getElementById('objectif_inputs');
    var consContainer = document.getElementById('contraintes_inputs');
    var btnGraphique = document.getElementById('btn_graphique');
    var graphWarning = document.getElementById('graph_warning');

    objContainer.innerHTML = 'Z = ';
    consContainer.innerHTML = '';

    for (var i = 1; i <= numVars; i++) {
        objContainer.innerHTML += '<input type="number" id="obj_x' + i + '" value="0" step="any"> x' + i + ' ';
        if (i < numVars) {
            objContainer.innerHTML += ' + ';
        }
    }

    for (var i = 1; i <= numCons; i++) {
        var consHtml = '<div class="equation-row" style="margin-bottom: 10px;">C' + i + ' : ';
        for (var j = 1; j <= numVars; j++) {
            consHtml += '<input type="number" id="cons_' + i + '_x' + j + '" value="0" step="any"> x' + j + ' ';
            if (j < numVars) {
                consHtml += ' + ';
            }
        }
        consHtml += ' &le; <input type="number" id="limite_' + i + '" value="0" step="any"></div>';
        consContainer.innerHTML += consHtml;
    }

    document.getElementById('dynamic_form_section').style.display = 'block';
    
    if (numVars === 2) {
        btnGraphique.disabled = false;
        btnGraphique.style.opacity = "1";
        btnGraphique.style.cursor = "pointer";
        graphWarning.style.display = "none";
    } else {
        btnGraphique.disabled = true;
        btnGraphique.style.opacity = "0.5";
        btnGraphique.style.cursor = "not-allowed";
        graphWarning.style.display = "block";
    }
}


function resoudre(methode) {
    var typeOpt = document.getElementById('type_optimisation').value;
    var numVars = parseInt(document.getElementById('num_vars').value);
    var numCons = parseInt(document.getElementById('num_cons').value);

    var coefficients_objectif = [];
    for (var i = 1; i <= numVars; i++) {
        coefficients_objectif.push(parseFloat(document.getElementById('obj_x' + i).value));
    }

    var matrice_ressources = [];
    var limites_ressources = [];
    for (var i = 1; i <= numCons; i++) {
        var ligne_contrainte = [];
        for (var j = 1; j <= numVars; j++) {
            ligne_contrainte.push(parseFloat(document.getElementById('cons_' + i + '_x' + j).value));
        }
        matrice_ressources.push(ligne_contrainte);
        limites_ressources.push(parseFloat(document.getElementById('limite_' + i).value));
    }

    var donnees = { 
        type_optimisation: typeOpt, 
        coefficients_objectif: coefficients_objectif, 
        matrice_ressources: matrice_ressources, 
        limites_ressources: limites_ressources 
    };
    
    var url_api = '/api/pl/graphique';
    if (methode === 'algebrique') {
        url_api = '/api/pl/algebrique';
    }

    fetch(url_api, { 
        method: 'POST', 
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(donnees) 
    })
    .then(function(reponse) {
        return reponse.json();
    })
    .then(function(resultat) {
        afficherResultat(resultat, methode);
    })
    .catch(function(erreur) {
        alert("Erreur de connexion.");
        console.error(erreur);
    });
}

function afficherResultat(resultat, methode) {
    var boiteResultat = document.getElementById('boite_resultat');
    var texteResultat = document.getElementById('texte_resultat');
    var imageContainer = document.getElementById('image_graphe_container');
    var imageResultat = document.getElementById('image_resultat');

    boiteResultat.style.display = 'block';
    
    if (resultat.succes) {
        var html_texte = '<p><strong>Statut :</strong> ' + resultat.message + '</p>' +
                         '<p><strong>Valeur Optimale (Z) :</strong> <span style="color: #00e5ff; font-size: 1.3em;">' + resultat.valeur_z_optimale + '</span></p><p><strong>Variables :</strong> ';
        
        for (var k = 0; k < resultat.valeurs_variables.length; k++) {
            html_texte += 'x' + (k + 1) + ' = ' + resultat.valeurs_variables[k] + ' &nbsp;&nbsp;';
        }
        html_texte += '</p>';
        
        texteResultat.innerHTML = html_texte;
        boiteResultat.style.borderTopColor = "#00e5ff";

        if (methode === 'graphique' && resultat.image_url) {
            imageResultat.src = resultat.image_url;
            imageContainer.style.display = 'block';
        } else {
            imageContainer.style.display = 'none';
        }
    } else {
        texteResultat.innerHTML = '<p style="color: red;"><strong>Erreur :</strong> ' + resultat.message + '</p>';
        boiteResultat.style.borderTopColor = "red";
        imageContainer.style.display = 'none';
    }
}

//GRAPHE
function genererFormulaireGraphe() {
    var numArcs = parseInt(document.getElementById('num_arcs').value);
    var algo = document.getElementById('algo_graphe').value;
    var arcsContainer = document.getElementById('arcs_inputs');
    var extraInputs = document.getElementById('extra_inputs');
    var labelArrivee = document.getElementById('label_arrivee');
    var inputArrivee = document.getElementById('noeud_arrivee');

    arcsContainer.innerHTML = '';
    for (var i = 1; i <= numArcs; i++) {
        arcsContainer.innerHTML += 
            '<div style="margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">' +
                '<span style="color: #00e5ff; font-weight: bold; width: 60px;">Arc ' + i + ' :</span>' +
                '<input type="text" id="src_' + i + '" placeholder="Source" style="width: 100px; text-transform: uppercase;">' +
                '<span style="color: white; font-weight: bold;"> ➔ </span>' +
                '<input type="text" id="dest_' + i + '" placeholder="Dest" style="width: 100px; text-transform: uppercase;">' +
                '<span style="color: #b3cde0; margin-left: 10px;"> Poids : </span>' +
                '<input type="number" id="poids_' + i + '" value="1" style="width: 80px;">' +
            '</div>';
    }

    extraInputs.style.display = 'block';
    if (algo === 'ford') {
        labelArrivee.style.display = 'inline-block'; 
        inputArrivee.style.display = 'inline-block';
    } else if (algo === 'kruskal') {
        extraInputs.style.display = 'none';
    } else {
        labelArrivee.style.display = 'inline-block'; 
        inputArrivee.style.display = 'inline-block';
    }
    document.getElementById('dynamic_form_graphe').style.display = 'block';
}

function resoudreGraphe() {
    var algo = document.getElementById('algo_graphe').value;
    var typeGraphe = document.getElementById('type_graphe').value;
    var numArcs = parseInt(document.getElementById('num_arcs').value);
    var noeudDepart = document.getElementById('noeud_depart').value.toUpperCase();
    
    var noeudArrivee = null;
    if (algo !== 'kruskal') {
        noeudArrivee = document.getElementById('noeud_arrivee').value.toUpperCase();
    }

    var arcs = [];
    for (var i = 1; i <= numArcs; i++) {
        var src = document.getElementById('src_' + i).value.toUpperCase();
        var dest = document.getElementById('dest_' + i).value.toUpperCase();
        var poids = parseFloat(document.getElementById('poids_' + i).value);
        if (src && dest) {
            arcs.push({ src: src, dest: dest, poids: poids });
        }
    }

    var donnees = { 
        algo_graphe: algo, 
        type_graphe: typeGraphe, 
        arcs: arcs, 
        noeud_depart: noeudDepart, 
        noeud_arrivee: noeudArrivee 
    };

    fetch('/api/graphe/resoudre', { 
        method: 'POST', 
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(donnees) 
    })
    .then(function(reponse) {
        return reponse.json();
    })
    .then(function(resultat) {
        afficherResultatGraphe(resultat);
    })
    .catch(function(erreur) {
        alert("Erreur de connexion.");
        console.error(erreur);
    });
}

function afficherResultatGraphe(resultat) {
    var boiteResultat = document.getElementById('boite_resultat_graphe');
    var texteResultat = document.getElementById('texte_resultat_graphe');
    var imageContainer = document.getElementById('image_graphe_container');
    var imageResultat = document.getElementById('image_resultat_graphe');

    boiteResultat.style.display = 'block';

    if (resultat.succes) {
        texteResultat.innerHTML = '<p style="color: #00e5ff; font-size: 1.2em;"><strong>Natija :</strong> ' + resultat.message + '</p>';
        boiteResultat.style.borderTopColor = "#00e5ff";
        if (resultat.image_url) {
            imageResultat.src = resultat.image_url;
            imageContainer.style.display = 'block';
        }
    } else {
        texteResultat.innerHTML = '<p style="color: red;"><strong>Erreur :</strong> ' + resultat.message + '</p>';
        boiteResultat.style.borderTopColor = "red";
        imageContainer.style.display = 'none';
    }
}