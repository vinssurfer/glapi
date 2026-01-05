#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config as config
import constantes as constantes
from flask import request, render_template, session, redirect, url_for
from flask import Blueprint
from db.db_objects import db_objects

liste_objets_blueprint = Blueprint( name='liste_objets_blueprint', 
                                    import_name = __name__,
                                    template_folder='templates')

# Object de la base de données
db = db_objects()

# Page liste des objets
@liste_objets_blueprint.route('/liste_objets')
def liste_objets():
    """
        Page listant les objets
    """
    return render_template( 'liste_objets.html',
                            liste_objets = db.get_liste_objets()
                        )