# -*- coding: utf-8 -*-
"""
Serveur web – Pluviométrie Grand Lyon

- Contient une version améliorée du cache
- Pluviométrie simple
- Moyenne de 2 stations
- Comparaison de 2 courbes sur le même graphique
- Heatmap

Auteur: ECL 2025
"""

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import os
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt

# numéro du port TCP utilisé par le serveur
port_serveur = 8080
# nom de la base de données
BD_name = "pluvio.sqlite"


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """"Classe dérivée pour traiter les requêtes entrantes du serveur"""

    # sous-répertoire racine des documents statiques
    static_dir = 'client'

    def __init__(self, *args, **kwargs):
        """Surcharge du constructeur pour imposer 'client' comme sous répertoire racine"""
        super().__init__(*args, directory=self.static_dir, **kwargs)
        

    def do_GET(self):
        self.init_params()

        if self.path_info[0] == 'stations':
            self.send_stations_pluvio()

        elif self.path_info[0] == 'pluviometrie':
            if len(self.path_info) > 1 and self.path_info[1] == 'moyenne':
                self.send_pluviometrie_moyenne()
            elif len(self.path_info) > 1 and self.path_info[1] == 'comparer':
                self.send_pluviometrie_comparer()
            else:
                self.send_pluviometrie()
        # le chemin d'accès commence par /cartedechaleur
        elif self.path_info[0] == 'cartedechaleur':
            self.send_cartedechaleur()
            
        else:
            super().do_GET()

    # Remplace le séparateur pour lier avec la base de données
    def safe_filename(self, s):
        if s is None:
            return "none"
        return s.replace(":", "-").replace("T", "_")

    # Cache
    def chercher_cache(self, type_g, s1, s2, start, end):
        c = conn.cursor()
        c.execute("""
            SELECT donnees_json, image_path
            FROM cache_graphiques
            WHERE type=? AND station1=? AND station2 IS ?
            AND date_start IS ? AND date_end IS ?
        """, (type_g, s1, s2, start, end))
        return c.fetchone()

    def sauvegarder_cache(self, type_g, s1, s2, start, end, data, img):
        c = conn.cursor()
        c.execute("""
            INSERT INTO cache_graphiques
            (type, station1, station2, date_start, date_end,
             donnees_json, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            type_g, s1, s2, start, end,
            json.dumps(data),
            img,
        ))
        conn.commit()


    def send(self, body, headers=[]):
        encoded = body.encode('utf-8')
        self.send_response(200)
        for h in headers:
            self.send_header(*h)
        self.send_header('Content-Length', len(encoded))
        self.end_headers()
        self.wfile.write(encoded)

    def init_params(self):
        info = urlparse(self.path)
        self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
        self.params = parse_qs(info.query)

# Programme principal
if __name__ == '__main__':
    conn = sqlite3.connect(BD_name)
    # Crée le cache si ce dernier est supprimé
    conn.execute("""
    CREATE TABLE IF NOT EXISTS cache_graphiques (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        station1 TEXT,
        station2 TEXT,
        date_start TEXT,
        date_end TEXT,
        donnees_json TEXT,
        image_path TEXT
    )
    """)
    conn.commit()
    httpd = socketserver.TCPServer(("", port_serveur), RequestHandler)
    print("Serveur lancé sur le port", port_serveur)
    httpd.serve_forever()
