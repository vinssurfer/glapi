import os, sys
import logging
from logging.handlers import RotatingFileHandler
import config

class logFileAndConsole:
    
    def __init__(self, logpath: str, logFileName:str, minimumLogLevel:int=logging.DEBUG, maxLogFileSizeBytes:int=100000, maxFileLogHistory:int=10):
        """
            Class permettant d'afficher un message dans la console de docker 
            et d'enregistrer un fichier log dans le dossier log de l'application

            logpath : Dossier où seront stocker les fichiers log
            logFileName : Nom du fichier log qui sera dans le dossier log de l'application
            minimumLogLevel : Niveau minimum du log pour l'enregistrement de type logFileAndConsole.logging.DEBUG
            maxLogFileSizeBytes : Taille maximal en bytes d'un fichier log (par défaut 0.1Mo)
            maxFileLogHistory : Nombre de fichier log à historiser (par défaut 10)
        """
        if logpath[-1:] == '\\' or logpath[-1:] == '/':
            self.logpath = logpath[:-1]
        else:
            self.logpath = logpath

        self.logFileName = logFileName
        self.minimumLogLevel = minimumLogLevel
        self.maxLogFileSizeBytes = maxLogFileSizeBytes
        self.maxFileLogHistory = maxFileLogHistory
        self.rotating_file_handler = None
        self.console_stream_handler = None
        
        # ---- Création du gestionnaire de log ----
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.minimumLogLevel) # Niveau minimum pour enregistrer le log

    def __addConsoleStreamHandler(self):
        """
            Ajoute au gestionnaire de log la gestion de la console
        """
        # ---- Création du console log ----
        self.console_stream_handler = logging.StreamHandler()
        self.console_stream_handler.setFormatter(ConsoleColorFormatter()) # Application du format d'une ligne de log
        self.logger.addHandler(self.console_stream_handler) # Ajout au gestionnaire de log

    def __addRotatingFileHandler(self):
        """
            Ajoute au gestionnaire de log la gestion de fichiers log avec rotation
        """
        # ---- Création du fichier log ----
        if not self.__log_path_exist():
            self.__create_log_folder()

        # Rotation du fichier log tous les 0.1Mo et sauvegarde de 20 log (paramètres par défaut)
        self.rotating_file_handler = RotatingFileHandler(self.__log_path(), maxBytes=self.maxLogFileSizeBytes, backupCount=self.maxFileLogHistory, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # Format d'une ligne de log
        self.rotating_file_handler.setFormatter(formatter) # Application du format d'une ligne de log
        self.logger.addHandler(self.rotating_file_handler) # Ajout au gestionnaire de log

    def __create_log_folder(self):
        """
            Création du dossier des logs
        """
        os.mkdir(self.logpath)
           
    def __log_path_exist(self):
        """
            Retourne True si dossier existe, sinon False
        """
        return os.path.isdir(self.logpath)

    def __log_path(self):
        # Chemin vers le fichier log
        if sys.platform == "linux" or sys.platform == "linux2":
            # linux
            return self.logpath + '/' + self.logFileName
        elif sys.platform == "win32":
            # Windows
            return self.logpath + '\\' + self.logFileName

    def __handler_exists(self, handler):
        """
            Retourne True si le handler existe sinon False
        """
        try:
            for h in self.logger.handlers:
                if h == handler:
                    return True
            return False
        except:
            return False

    def addLog(self, message:str, loglevel:int=logging.DEBUG, onlyConsole:bool=False):
        """
            Ajout d'un message au log

            message : Message à écrire
            loglevel : Niveau du log du type log_console.logging.DEBUG
            onlyConsole : Affichage uniquement dans la console
        """
        if not onlyConsole :
            if not self.__handler_exists(self.rotating_file_handler): # si le handler fichier log n'éxiste pas
                self.__addRotatingFileHandler() # Ajout de la gestion de fichier log

            if not self.__handler_exists(self.console_stream_handler): # si le handler console n'éxiste pas
                self.__addConsoleStreamHandler() # Ajout de la gestion de la console
        else:
            if not self.__handler_exists(self.console_stream_handler): # si le handler console n'éxiste pas
                self.__addConsoleStreamHandler() # Ajout de la gestion de la console
        
            if self.__handler_exists(self.rotating_file_handler): # si le handler fichier log éxiste
                self.logger.removeHandler(self.rotating_file_handler) # Suppression de la gestion de fichier log

        # Ajout du message au  log
        if loglevel == logging.CRITICAL:
            self.logger.critical(message)
        elif loglevel == logging.ERROR:
            self.logger.error(message)
        elif loglevel == logging.WARNING:
            self.logger.warning(message)
        elif loglevel == logging.INFO:
            self.logger.info(message)
        else:
            self.logger.debug(message)

class ConsoleColorFormatter(logging.Formatter):
    """
        Class permetant d'ajouter de la couleur au log de la console suivant le niveau du log
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    cyan = "\x1b[36;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Objet logger unique à importer dans tous les modules
logger = logFileAndConsole( logpath= config.log_path(),
                            logFileName= 'app.log',
                            minimumLogLevel= logging.DEBUG,
                            maxLogFileSizeBytes =100000, 
                            maxFileLogHistory =10
                        )
