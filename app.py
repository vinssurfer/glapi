#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import os
from pygltflib import GLTF2
from werkzeug.utils import secure_filename
import shutil
import uuid
import base64
from pygltflib import Buffer, BufferView, Image as GlTFImage

import constantes as constantes
import config as config
from logFileAndConsole import logger # Import de l'objet logger pour les logs

config.check_dbs_log_file() # Contrôle des bases de données et fichier log

# Déclaration des pages
from pages.index.index import index_blueprint
from pages.objet.objet import objet_blueprint
from pages.admin.liste_objets.liste_objets import liste_objets_blueprint

# Lancement de l'application    
app = Flask(__name__)
app.debug = False # Activation du debug de flask
app.secret_key = constantes.KEY # Clef secrète afin de pouvoir chiffrer les infos de session
app.jinja_env.trim_blocks = True # Suppression des sauts de ligne avec les bloc Jinja
app.jinja_env.lstrip_blocks = True # Suppression des espace et tab avec les bloc Jinja

# Ajout des pages dans l'app
app.register_blueprint(index_blueprint)
app.register_blueprint(objet_blueprint)
app.register_blueprint(liste_objets_blueprint)

"""
# Configuration des dossiers
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'static', '3D_images')
TEXTURES_DIR = os.path.join(BASE_DIR, 'static', 'textures')
TEMP_DIR = os.path.join(BASE_DIR, 'static', 'temp')

# Créer le dossier temp s'il n'existe pas
os.makedirs(TEMP_DIR, exist_ok=True)

# Extensions autorisées
ALLOWED_EXTENSIONS = {'gltf', 'glb', 'png', 'jpg', 'jpeg'}

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

# Page index
@app.route('/')
def index():
    # Lister les modèles disponibles pour le frontend
    models = [f for f in os.listdir(MODELS_DIR) if allowed_file(f, {'gltf', 'glb'})]
    return render_template('index.html', models=models)

# Nouvelle route pour servir les textures embarquées extraites
@app.route('/embedded_texture/<temp_filename>')
def serve_embedded_texture(temp_filename):
    temp_path = os.path.join(TEMP_DIR, temp_filename)
    if not os.path.exists(temp_path):
        return "Texture non trouvée", 404
    
    with open(temp_path, 'rb') as f:
        return f.read(), 200, {'Content-Type': 'image/png'}  # Assume PNG ; ajustez si nécessaire

@app.route('/get_model_info', methods=['GET'])
def get_model_info():
    model_filename = request.args.get('model')
    if not model_filename or not allowed_file(model_filename, {'gltf', 'glb'}):
        return jsonify({'error': 'Modèle invalide'}), 400

    model_path = os.path.join(MODELS_DIR, model_filename)
    gltf = GLTF2().load(model_path)

    original_textures = []

    if gltf.materials:
        for material_idx, material in enumerate(gltf.materials):
            if material.pbrMetallicRoughness and material.pbrMetallicRoughness.baseColorTexture:
                tex_index = material.pbrMetallicRoughness.baseColorTexture.index
                if tex_index is not None and tex_index < len(gltf.textures or []):
                    texture = gltf.textures[tex_index]
                    img_index = texture.source
                    if img_index is not None and img_index < len(gltf.images or []):
                        image = gltf.images[img_index]

                        # Cas 1 : Texture externe (uri)
                        if image.uri:
                            # Chemin relatif adapté
                            basename = os.path.basename(image.uri)
                            possible_paths = [
                                f"/static/textures/{basename}",
                                f"/static/3D_image/{basename}"
                            ]
                            texture_url = None
                            for path in possible_paths:
                                full_path = os.path.join(BASE_DIR, 'static', path.lstrip('/')[7:])  # Correction chemin
                                if os.path.exists(full_path.replace('/static/', '')):
                                    texture_url = path
                                    break
                            if not texture_url:
                                texture_url = image.uri  # Fallback

                            original_textures.append({
                                'url': texture_url,
                                'type': 'external'
                            })

                        # Cas 2 : Texture embarquée (bufferView ou data URI)
                        elif image.bufferView is not None or (image.uri and image.uri.startswith('data:')):
                            # Générer un nom temporaire unique pour cette texture extraite
                            temp_texture_filename = f"embedded_{uuid.uuid4().hex}.png"
                            temp_texture_path = os.path.join(TEMP_DIR, temp_texture_filename)

                            if image.uri and image.uri.startswith('data:'):
                                # Data URI base64
                                header, encoded = image.uri.split(',', 1)
                                image_data = base64.b64decode(encoded)
                            else:
                                # BufferView binaire
                                buffer_view = gltf.bufferViews[image.bufferView]
                                buffer = gltf.buffers[buffer_view.buffer]
                                
                                # Chargement du GLB binaire complet
                                with open(model_path, 'rb') as f:
                                    f.seek(buffer_view.byteOffset or 0)
                                    length = buffer_view.byteLength
                                    image_data = f.read(length)

                            # Sauvegarder temporairement l'image extraite
                            with open(temp_texture_path, 'wb') as f:
                                f.write(image_data)

                            texture_url = f"/embedded_texture/{temp_texture_filename}"
                            original_textures.append({
                                'url': texture_url,
                                'type': 'embedded'
                            })

    # Retourner la première texture principale (baseColor) ou une liste
    primary_texture = original_textures[0]['url'] if original_textures else None

    return jsonify({
        'original_texture': primary_texture,
        'all_textures': [item['url'] for item in original_textures],
        'textures_info': original_textures  # Pour debug ou affichage multiple
    })

@app.route('/modify_texture', methods=['POST'])
def modify_texture():
    data = request.form
    model_filename = data.get('model')          # Nom du modèle choisi
    texture_target = data.get('texture_target', 'baseColorTexture')  # Par défaut baseColor

    if not model_filename or not allowed_file(model_filename, {'gltf', 'glb'}):
        return jsonify({'error': 'Modèle invalide'}), 400

    if 'texture' not in request.files:
        return jsonify({'error': 'Aucune texture fournie'}), 400

    texture_file = request.files['texture']
    if texture_file.filename == '' or not allowed_file(texture_file.filename, {'png', 'jpg', 'jpeg'}):
        return jsonify({'error': 'Texture invalide'}), 400

    # 1. Sauvegarder la texture uploadée
    texture_filename = secure_filename(texture_file.filename)
    texture_path = os.path.join(TEXTURES_DIR, texture_filename)
    texture_file.save(texture_path)

    # 2. Charger le modèle original
    original_path = os.path.join(MODELS_DIR, model_filename)
    gltf = GLTF2().load(original_path)

    # 3. Ajouter la nouvelle image (référence externe)
    from pygltflib import Image
    new_image = Image()
    new_image.uri = f"../textures/{texture_filename}"  # Chemin relatif depuis temp/
    gltf.images.append(new_image)

    # 4. Créer une nouvelle texture
    from pygltflib import Texture as GlTFTexture
    new_texture = GlTFTexture()
    new_texture.source = len(gltf.images) - 1
    gltf.textures.append(new_texture)
    new_texture_index = len(gltf.textures) - 1

    # 5. Appliquer la nouvelle texture au(x) matériau(x)
    # Ici on applique à tous les matériaux pour plus de simplicité ; vous pouvez cibler un matériau spécifique
    if gltf.materials:
        for material in gltf.materials:
            if material.pbrMetallicRoughness:
                if texture_target == 'baseColorTexture':
                    if material.pbrMetallicRoughness.baseColorTexture is None:
                        from pygltflib import TextureInfo
                        material.pbrMetallicRoughness.baseColorTexture = TextureInfo()
                    material.pbrMetallicRoughness.baseColorTexture.index = new_texture_index
                # Vous pouvez ajouter d'autres cas : normalTexture, metallicRoughnessTexture, etc.

    # 6. Générer un nom unique pour le modèle temporaire
    temp_filename = f"modified_{uuid.uuid4().hex}.glb"  # Toujours en GLB pour un fichier autonome plus simple
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    # 7. Sauvegarder en GLB (format binaire compact)
    gltf.save(temp_path)

    # 8. Retourner l'URL du modèle modifié
    model_url = f"/static/temp/{temp_filename}"
    return jsonify({
        'success': True,
        'model_url': model_url,
        'texture_applied': texture_filename,
        'original_texture': None  # Le frontend appellera get_model_info pour l'original
    })

# Optionnel : Nettoyage périodique du dossier temp (à exécuter via cron ou tâche planifiée)
@app.route('/cleanup_temp')
def cleanup_temp():
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur suppression {file_path}: {e}")
    return "Dossier temp nettoyé."

if __name__ == '__main__':
    app.run(debug=True)
"""