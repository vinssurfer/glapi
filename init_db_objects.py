import sys
import sqlite3
import config as config

import logging
from logFileAndConsole import logger # Import de l'objet logger pour les logs

conn = sqlite3.connect(config.db_ObjectsPath())
conn.row_factory = sqlite3.Row

force = False

DB_NAME = "DB objets"

# si des arguments sont passés
if len(sys.argv) > 1:
    if sys.argv[1] == 'force':
        force = True
        logger.addLog(DB_NAME + " Création de la base de donnée des objets.",logging.INFO)

if not force:
    n = input("Supression des anciennes tables (o/n): ")
    if n == 'o':
        logger.addLog(DB_NAME + " Suppression des tables",logging.INFO)
        
        try:
            conn.execute("DROP TABLE IF EXISTS objets;").fetchall()
            conn.execute("DROP TABLE IF EXISTS categories;").fetchall()
            conn.execute("DROP TABLE IF EXISTS sous_categories;").fetchall()
            conn.execute("DROP TABLE IF EXISTS images;").fetchall()
        except:
            logger.addLog(DB_NAME + " Erreur suppression tables !",logging.ERROR)

# ---------------------------------------- CREATION DES TABLES ---------------------------------------- 
logger.addLog(DB_NAME + " Création des tables",logging.INFO)

try:
    #Création de la table objets
    conn.execute("""CREATE TABLE IF NOT EXISTS objets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL,
    id_categories INTEGER,
    id_sous_categories INTEGER,
    description TEXT,
    premiere_page INTEGER,
    UNIQUE(id)
    );""").fetchall() 
except:
    logger.addLog(DB_NAME + " Erreur création table objets !",logging.ERROR)

try:
    #Création de la table de categories
    conn.execute("""CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
    );""").fetchall() 
except:
    logger.addLog(DB_NAME + " Erreur création table categories !",logging.ERROR)

try:
    #Création de la table de sous-categories
    conn.execute("""CREATE TABLE IF NOT EXISTS sous_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categories INTEGER,
    nom TEXT NOT NULL
    );""").fetchall() 
except:
    logger.addLog(DB_NAME + " Erreur création table sous_categories !",logging.ERROR)

try:
    #Création de la table de images
    conn.execute("""CREATE TABLE IF NOT EXISTS images (
    id_objets INTEGER,
    image3D INTEGER,
    ordre INTEGER,
    fichier TEXT NOT NULL
    );""").fetchall() 
except:
    logger.addLog(DB_NAME + " Erreur création table comptes !",logging.ERROR)
    
conn.commit()
conn.close()