# -*- coding: utf-8 -*-
"""
Serveur web – Sushis Waza
Auteur : Syuma LOUETTE 
Date : 13/03/2026

"""

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import os
import datetime as dt
import matplotlib.pyplot as plt

# numéro du port TCP utilisé par le serveur
port_serveur = 8081


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """"Classe dérivée pour traiter les requêtes entrantes du serveur"""

    # sous-répertoire racine des documents statiques
    static_dir = 'client'

    def __init__(self, *args, **kwargs):
        """Surcharge du constructeur pour imposer 'client' comme sous répertoire racine"""
        super().__init__(*args, directory=self.static_dir, **kwargs)

    # Remplace le séparateur pour lier avec la base de données
    def safe_filename(self, s):
        if s is None:
            return "none"
        return s.replace(":", "-").replace("T", "_")


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
    httpd = socketserver.TCPServer(("", port_serveur), RequestHandler)
    print("Serveur lancé sur le port", port_serveur)
    httpd.serve_forever()
