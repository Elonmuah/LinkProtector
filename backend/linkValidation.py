from urllib.parse import urlparse, unquote
from posixpath import normpath
import ipaddress
import errorLog
from datetime import datetime, timezone
import traceback
import time

class CheckURL:
    def __init__(self, data):
        self.raw = data
        self.parsed = urlparse(self.raw)
        self.allowedSchemes = ["https"]
        self.specialSchemes = ["http"]
        self.blockedHosts = ["localhost", "127.0.0.1", "::1", "0.0.0.0", "::"]
        self.blockedSuffixes = [".local", ".lan", ".internal", ".home", ".corp", ".example"]

    def parseCheckURL(self):
        if not self.parsed.netloc or not self.parsed.scheme:
            return "INVALID_URL_ERROR"
        
        return "OK"
    
    def schemeCheckURL(self):
        scheme = self.parsed.scheme.lower()

        if scheme in self.specialSchemes:
            return "HTTP_NOT_ALLOWED_ERROR"
        elif scheme in self.allowedSchemes:
            return "OK"
        
        return "UNSUPPORTED_SCHEME"
    
    def normalizeURL(self):
        try:
            query = unquote(self.parsed.query)
            path = unquote(self.parsed.path)
            path = normpath(path)
            host = self.parsed.hostname.lower()
            port =self.parsed.port
            scheme = self.parsed.scheme.lower()

            if (scheme == "https" and port in (None, 443)) or \
            (scheme == "http" and port in (None, 80)):
                netloc = host
            elif port:
                netloc = f"{host}:{port}"
            else:
                netloc = host

            self.parsed = self.parsed._replace(
                scheme=scheme,
                netloc=netloc,
                path=path,
                query=query,
                fragment=""
            )
        except Exception as e:
            error_id = f"{int(time.time()*1000)}"
            date = datetime.now(timezone.utc)
            errorLog.logError({
                "error": "NORMALIZATION_ERROR",
                "errorCode": error_id,
                "URL": self.raw,
                "time": date.isoformat(),
                "errorType": ["NORMALIZATION_ERROR with type:", type(e).__name__],
                "message": ["URL was not normalized due to error:", str(e)],
                "trace": traceback.format_exc()
            })
            return ["NORMALIZATION_ERROR", error_id]

    def validateHost(self):
        host = self.parsed.hostname
        port = self.parsed.port

        if host in self.blockedHosts:
            return "HOSTNAME_NOT_ALLOWED_ERROR" # Block hostname
        
        if self.isNotPrivateIP(host):
            return "IP_NOT_ALLOWED_ERROR" # Block IP
        
        for blockedSuffix in self.blockedSuffixes:
            if host.lower().endswith(blockedSuffix):
                return "DNS_NAME_NOT_ALLOWED_ERROR" # Block DNS name
            
        return "OK"

    def isNotPrivateIP(self, host):
        try:
            #parse IP
            ip = ipaddress.ip_address(host)
        except ValueError:
            return False # not an IP, treat as hostname
        
        if ip.is_private:       # 10/8, 172.16/12, 192.168/16 (IPv4), fc00::/7 (IPv6)
            return True
        
        if ip.is_loopback:      # 127.0.0.1, ::1
            return True
        
        if ip.is_link_local:    # 169.254/16, fe80::/10
            return True
        
        if ip.is_multicast:     # 224.0.0.0/4, ff00::/8
            return True
        
        if ip.is_reserved:      # 240.0.0.0/4, some IPv6 reserved ranges
            return True
        
        if ip.is_unspecified:   # 0.0.0.0, ::
            return True
        
        return False # IP fine
    
    def runTests(self):
        if self.parseCheckURL() != "OK":
            error_id = f"{int(time.time()*1000)}"
            errorLog.logError({
                "error": self.parseCheckURL(),
                "errorCode": error_id,
                "URL": self.raw,
                "time": datetime.now(timezone.utc).isoformat(),
                "errorType": self.parseCheckURL,
                "message": "URL did not check the parsing",
                "trace": "No trace provided"
            })
            return {
                "error": 1,
                "errorCode": error_id,
                "message": self.parseCheckURL()
                }
        
        elif self.schemeCheckURL() != "OK":
            error_id = f"{int(time.time()*1000)}"
            errorLog.logError({
                "error": self.schemeCheckURL(),
                "errorCode": error_id,
                "URL": self.raw,
                "time": datetime.now(timezone.utc).isoformat(),
                "errorType": self.schemeCheckURL,
                "message": "URL did not check the schemata",
                "trace": "No trace provided"
            })
            return {
                "error": 1,
                "errorCode": error_id,
                "message": self.schemeCheckURL()
                }
        
        elif self.normalizeURL()[0] == "NORMALIZATION_ERROR":
            return {
                "error": 1,
                "errorCode": self.normalizeURL[1],
                "message": self.normalizeURL()[0]
                }
        
        elif self.validateHost != "OK":
            error_id = f"{int(time.time()*1000)}"
            errorLog.logError({
                "error": self.validateHost(),
                "errorCode": error_id,
                "URL": self.raw,
                "time": datetime.now(timezone.utc).isoformat(),
                "errorType": self.validateHost,
                "message": "The provided host, IP or DNS did not check out",
                "trace": "No trace provided"
            })
            return {
                "error": 1,
                "errorCode": error_id,
                "message": self.validateHost()
                }
        
        return {"error": 0}