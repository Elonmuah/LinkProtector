from flask import Flask, jsonify, redirect, request
import secrets
import json
from urllib.parse import urlparse



class Tokenize:
    def __init__(self, url):
        # =
        self.raw = url
        self.url = "http://127.0.0.1:5000/" # Testing link, current startpage
        self.host = urlparse(self.raw).hostname
        
        self.token = secrets.token_urlsafe(8)
        # ()
        self.tokenize()

    def tokenize(self):
        # Implement go.mySide.com
        self.url += "/affiliate"
        self.url += "/" + self.host # affiliate side
        self.url += "/" + self.token

    def getTokenizedLink(self):
        return self.url
    
    def getHost(self):
        return self.host