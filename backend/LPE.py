from flask import Flask, jsonify, redirect, request
import secrets
import json
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

class Tokenize:
    def __init__(self, url):
        self.raw = url.strip()
        self.base_url = None          # ← new: without params
        self.params = {}              # ← new: query params dict
        self.host = None
        self.token = secrets.token_urlsafe(8)
        self.protected_url = "http://127.0.0.1:5000/"  # change to your real domain later

        self._parse_url()
        self.tokenize()

    def _parse_url(self):
        """Extract host, base URL (without query), and params"""
        parsed = urlparse(self.raw)
        self.host = parsed.hostname or ""

        # Base URL = scheme + netloc + path (no query/fragment)
        self.base_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            "",          # remove query
            ""           # remove fragment
        ))

        # Params as dict (list values for multi-value keys)
        self.params = parse_qs(parsed.query)

    def tokenize(self):
        """Build the protected short link"""
        self.protected_url += f"affiliate/{self.host}/{self.token}"

    def getTokenizedLink(self):
        return self.protected_url

    def getHost(self):
        return self.host

    # New getters for later use (encryption, redirect, etc.)
    def getBaseUrl(self):
        return self.base_url

    def getParams(self):
        return self.params  # dict like {'tag': ['yourtag123'], 'ref': ['abc']}

    def getFullOriginalUrl(self):
        """Reconstruct original URL with params"""
        if not self.base_url:
            return self.raw
        query_string = urlencode(self.params, doseq=True)
        return urlunparse(urlparse(self.base_url)._replace(query=query_string))