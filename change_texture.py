from pygltflib import GLTF2
from pygltflib.utils import Image, ImageFormat

# Chemins des fichiers (adaptez-les à votre projet)
input_gltf_path = "static/3D_images/poule.gltf"  # Ou .gltf
new_texture_path = "static/textures/test.png"  # Texture uploadée par l'utilisateur
output_gltf_path = "static/temp/new_poule.gltf"   # Fichier modifié à servir au frontend

# Étape 1 : Charger le modèle
gltf = GLTF2().load(input_gltf_path)

# Étape 2 : Identifier la texture à remplacer
# Inspection rapide du modèle (à adapter selon la structure de votre modèle)
# Exemple : supposons que le premier matériau utilise une baseColorTexture (texture principale PBR)
if gltf.materials and gltf.materials[0].pbrMetallicRoughness:
    base_color_texture_info = gltf.materials[0].pbrMetallicRoughness.baseColorTexture
    if base_color_texture_info:
        old_texture_index = base_color_texture_info.index
        print(f"Ancienne texture index : {old_texture_index}")
        old_image_index = gltf.textures[old_texture_index].source
        print(f"Ancienne image index : {old_image_index}")

# Étape 3 : Ajouter la nouvelle image (référence externe)
new_image = Image()
new_image.uri = new_texture_path  # Nom du fichier servi dans /static/
gltf.images.append(new_image)

# Étape 4 : Créer une nouvelle texture pointant vers la nouvelle image
new_texture_index = len(gltf.textures)  # Index de la nouvelle texture
from pygltflib import Texture as GlTFTexture
new_texture = GlTFTexture()
new_texture.source = len(gltf.images) - 1  # Index de la nouvelle image
gltf.textures.append(new_texture)

# Étape 5 : Mettre à jour le matériau pour utiliser la nouvelle texture
gltf.materials[0].pbrMetallicRoughness.baseColorTexture.index = new_texture_index

# Optionnel : Supprimer l'ancienne texture et image pour nettoyer (facultatif)
# del gltf.textures[old_texture_index]
# del gltf.images[old_image_index]
# Attention : ajustez les indices des autres références si nécessaire

# Étape 6 : Sauvegarder le modèle modifié (en GLB pour un fichier unique, ou GLTF pour externe)
gltf.save(output_gltf_path)  # Sauvegarde en GLB si l'original était GLB, sinon GLTF

print("Modèle modifié sauvegardé avec succès.")