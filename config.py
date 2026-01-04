import os, sys
import sqlite3
import hashlib
import constantes as constantes

def img_2D_Path(fichier : str):
    """
    Retourne le chemin vers le fichier de l'images 2D
    
    :param fichier: nom du fichier 2D
    :type fichier: str
    """
    return '/static/Objets2DImages/' + fichier

def img_3D_Path(fichier : str):
    """
    Retourne le chemin vers le fichier de l'images 3D
    
    :param fichier: nom du fichier 3D
    :type fichier: str
    """
    return '/static/Objets3DImages/' + fichier

def db_ObjectsPath():
    """
    Retourne le chemin vers la base de données des objets
    """
    pathname = os.path.dirname(sys.argv[0])

    # Chemin vers la base de données
    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        return '/var/www/' + constantes.SITE_NAME.lower() + '/static/objects.db'
    elif sys.platform == "win32":
        # Windows
        return pathname + '\\static\\objects.db'

def db_UserPath():
    """
    Retourne le chemin vers la base de données des utilisateurs
    """
    pathname = os.path.dirname(sys.argv[0])

    # Chemin vers la base de données
    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        return '/var/www/' + constantes.SITE_NAME.lower() + '/static/users.db'
    elif sys.platform == "win32":
        # Windows
        return pathname + '\\static\\users.db'

def log_path():
    """
    Retourne le chemin du fichier log
    """
    pathname = os.path.dirname(sys.argv[0])

    # Chemin vers le fichier log
    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        return '/var/www/' + constantes.SITE_NAME.lower() + '/static/log'
    elif sys.platform == "win32":
        # Windows
        return pathname + '\\static\\log'

def check_dbs_log_file():
    """
    Vérification que les bases de données et le fichier log existe
    Sinon création des fichiers
    """
    # Contrôle si le fichier de la base de données des objets existe
    if not os.path.exists(db_ObjectsPath()):
        # Création du fichier        
        pathname = os.path.dirname(sys.argv[0])
        if sys.platform == "win32":
            os.system('python ' + pathname + '\\init_db_Objects.py force') # Création de la base vide
        else:
            os.system('python /var/www/' + constantes.SITE_NAME.lower() + '/init_db_Objects.py force') # Création de la base vide

    # Contrôle si le fichier log existe
    if not os.path.exists(log_path()):
        # Création du fichier
        fichierlog = open(log_path(), "w")
        fichierlog.close()  

def get_db_objects_connection():
    """ 
    Retourne une connexion à la base de données
    """
    conn = sqlite3.connect(db_ObjectsPath())
    conn.row_factory = sqlite3.Row
    return conn

def get_db_user_connection():
    """
    Retourne une connexion à la base de données
    """
    conn = sqlite3.connect(db_UserPath())
    conn.row_factory = sqlite3.Row
    return conn

def hashing(value):
    """
    Fonction d'encryption des mots de passe

    :param value: valeur à crypter
    :type value: any
    """
    hash_object = hashlib.md5(bytes(str(value), encoding='utf-8'))
    hex_dig= hash_object.hexdigest()
    return hex_dig 
