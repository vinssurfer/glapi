import sqlite3
import config

class db_objects():
    """
        Class permettant la gestion des objets dans la base de données
    """
    def __init__(self):
        """
            Gestion de la base de données des objets
        """
        self.db_path = config.db_ObjectsPath()

    def __get_db_connection(self):
        """ 
            Retourne une connexion à la base de données
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
     
    def get_objets_premiere_page(self):
        """
            Retourne la liste des objets qui doivent être présent sur la première page.

            Liste contenant :
                id, nom, prix, fichier (chemin du fichier de l'image 2D)
        """
        conn = self.__get_db_connection()       
        sql = """SELECT o.id as id,
                        o.nom as nom,
                        o.prix as prix,
                        i.fichier as fichier
                FROM objets as o

                INNER JOIN images as i
                ON i.id_objets = o.id

                WHERE o.premiere_page = 1 AND i.image3D = 0
        """
        req = conn.execute(sql).fetchall()
        conn.close()

        # Conversion du résultat de la requête en liste
        list = []
        for line in req:
            list.append({
                'id': line['id'],
                'nom': line['nom'],
                'prix': line['prix'],
                'fichier': config.img_2D_Path(line['fichier'])
            })

        return list

    def get_objet(self, id : int):     
        """
        Retourne les informations d'un objet sauf la liste des images
        
        :param id: id de l'objet
        :type id: int
        """
        conn = self.__get_db_connection()       
        sql = """SELECT o.id as id,
                        o.nom as nom,
                        o.prix as prix,
                        o.id_categories as id_categories,
                        o.id_sous_categories as id_sous_categories,
                        o.description as description,
                        o.premiere_page as premiere_page,
                        c.nom as categorie,
                        sc.nom as sous_categorie
                FROM objets as o

                INNER JOIN categories as c
                ON c.id= o.id_categories

                INNER JOIN sous_categories as sc
                ON sc.id= o.id_sous_categories

                WHERE o.id =
        """ + str(id)

        req = conn.execute(sql).fetchall()
        conn.close()

        # Conversion du résultat de la requête en liste
        list = []
        for line in req:
            list.append({
                'id': line['id'],
                'nom': line['nom'],
                'prix': line['prix'],
                'id_categories': line['id_categories'],
                'id_sous_categories': line['id_sous_categories'],
                'description': line['description'],
                'premiere_page': line['premiere_page'],
                'categorie': line['categorie'],
                'sous_categorie': line['sous_categorie']
            })

        return list[0]
    
    def get_images2D_objet(self, id : int):
        """
        Retourne la liste des images 2D d'un objet
        
        :param id: id de l'objet
        :type id: int
        """
        conn = self.__get_db_connection()       
        sql = """SELECT i.fichier as fichier
                FROM images as i

                WHERE i.id_objets = """ + str(id) + """ AND image3D = 0 ORDER BY i.ordre"""

        req = conn.execute(sql).fetchall()
        conn.close()

        # Conversion du résultat de la requête en liste
        list = []
        for line in req:
            list.append({
                'fichier': config.img_2D_Path(line['fichier'])
            })
                
        return list
    
    def get_image3D_objet(self, id : int):
        """
        Retourne l'image 3D d'un objet
        
        :param id: id de l'objet
        :type id: int
        """
        conn = self.__get_db_connection()       
        sql = """SELECT i.fichier as fichier
                FROM images as i

                WHERE i.id_objets = """ + str(id) + """ AND image3D = 1 LIMIT 1"""

        req = conn.execute(sql).fetchall()
        conn.close()
   
        chemin = ""
        if len(req) >= 1:
            chemin = config.img_3D_Path(req[0]['fichier'])

        return chemin
    
    def get_liste_objets(self):     
        """
        Retourne la liste des objets avec la première image 2D
        """
        conn = self.__get_db_connection()       
        sql = """SELECT o.id as id,
                        o.nom as nom,
                        o.prix as prix,
                        o.id_categories as id_categories,
                        o.id_sous_categories as id_sous_categories,
                        o.description as description,
                        o.premiere_page as premiere_page,
                        c.nom as categorie,
                        sc.nom as sous_categorie,
                        (SELECT i.fichier
                         FROM images as i
                         WHERE i.id_objets = o.id AND i.image3D=0 LIMIT 1) as fichier2D
                FROM objets as o

                INNER JOIN categories as c
                ON c.id= o.id_categories

                INNER JOIN sous_categories as sc
                ON sc.id= o.id_sous_categories
        """

        req = conn.execute(sql).fetchall()
        conn.close()

        # Conversion du résultat de la requête en liste
        list = []
        for line in req:
            list.append({
                'id': line['id'],
                'nom': line['nom'],
                'prix': line['prix'],
                'id_categories': line['id_categories'],
                'id_sous_categories': line['id_sous_categories'],
                'description': line['description'],
                'premiere_page': line['premiere_page'],
                'categorie': line['categorie'],
                'sous_categorie': line['sous_categorie'],
                'fichier2D': config.img_2D_Path(line['fichier2D'])
            })

        return list