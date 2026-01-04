#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Lancement de l'application Glapi sur le port 5000 pour le debug sur le PC de développement
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)