#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config as config
import constantes as constantes
from flask import request, render_template, session, redirect, url_for
from flask import Blueprint
from db.db_objects import db_objects

ajout_blueprint = Blueprint( name='ajout_blueprint', 
                             import_name = __name__,
                             template_folder='templates')

modification_blueprint = Blueprint(  name='modification_blueprint', 
                                    import_name = __name__,
                                    template_folder='templates')

# Object de la base de données
db = db_objects()

# Page ajout objet
@ajout_blueprint.route('/ajout', methods=('GET', 'POST'))
def ajout():
    """
        Page ajout d'un objet
    """
    return render_template( 'ajout_modification.html'
                            
                        )

# Page modification d'objet
@modification_blueprint.route('/modification', methods=('GET', 'POST'))
def modification():
    """
        Page modification d'un objet
    """
    # Récupère l'ID de l'objet à afficher
    if request.method == 'GET':
        id = request.args.get('id')

        return render_template( 'ajout_modification.html',
                                objet = db.get_objet(id=id),
                                categorie = db.get_categories(),
                                sous_categorie = db.get_sous_categories(),
                                images2D = db.get_images2D_objet(id=id),
                                images3D = db.get_images3D_objet(id=id)
                            )
    
    return redirect(url_for('liste_objets_blueprint.liste_objets'))