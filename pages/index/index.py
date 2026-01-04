#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config as config
import constantes as constantes
from flask import render_template, session
from flask import Blueprint
from db.db_objects import db_objects

index_blueprint = Blueprint(name='index_blueprint', 
                            import_name = __name__,
                            template_folder='templates')

# Object de la base de données
db = db_objects()

# Page d'index
@index_blueprint.route('/')
def index():
    """
        Page d'index
    """
 
    return render_template( 'index.html',
                            listeObjetsPremierePage = db.get_objets_premiere_page()
                            )