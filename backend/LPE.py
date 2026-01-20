from flask import Flask, jsonify, redirect, request
import secrets
import json



class linkProtector:
    def __init__(self, url, title):
        # =
        self.realUrl = url
        self.url = "http://127.0.0.1:5000/" # Testing link, current startpage
        self.title = title
        self.token = secrets.token_urlsafe(8)
        # ()
        self.tokenize()

    def tokenize(self):
        self.url += self.title
        self.url += "/" + self.token

    def getTokenizedLink(self):
        return self.url