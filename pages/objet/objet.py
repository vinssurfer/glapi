#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config as config
import constantes as constantes
from flask import request, render_template, session, redirect, url_for
from flask import Blueprint
from db.db_objects import db_objects

objet_blueprint = Blueprint(name='objet_blueprint', 
                            import_name = __name__,
                            template_folder='templates')

# Object de la base de données
db = db_objects()

# Page objet
@objet_blueprint.route('/objet', methods=['GET'])
def objet():
    """
        Page d'un objet
    """
    # Récupère l'ID de l'objet à afficher
    if request.method == 'GET':
        id = request.args.get('id')

        return render_template( 'objet.html',
                                objet = db.get_objet(id = id),
                                images2D = db.get_images2D_objet(id = id),
                                image3D = db.get_image3D_objet(id = id)
                            )
    
    return redirect(url_for('index_blueprint.index'))