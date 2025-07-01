import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Tag
import socket
import requests
from googlesearch import search
import whois
from datetime import date
from urllib.parse import urlparse

class URLFeature:
    def __init__(self, url):
        self.url = url
        self.features = []
        self.domain = ""
        self.whois_response = None
        self.parsed = None
        self.response = None
        self.soup = None

        # Fetch and parse
        try:
            self.response = requests.get(url, timeout=5)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except Exception:
            self.response = None
            self.soup = None

        # Parse URL
        try:
            self.parsed = urlparse(url)
            self.domain = self.parsed.netloc
        except Exception:
            self.parsed = None
            self.domain = ""

        # WHOIS lookup
        try:
            self.whois_response = whois.whois(self.domain)
        except Exception:
            self.whois_response = None

        # Compute features
        self.features.append(self.UsingIp())
        self.features.append(self.longUrl())
        self.features.append(self.shortUrl())
        self.features.append(self.symbol())
        self.features.append(self.redirecting())
        self.features.append(self.prefixSuffix())
        self.features.append(self.SubDomains())
        self.features.append(self.Https())
        self.features.append(self.DomainRegLen())
        self.features.append(self.NonStdPort())
        self.features.append(self.HTTPSDomainURL())
        self.features.append(self.AbnormalURL())
        self.features.append(self.WebsiteForwarding())
        self.features.append(self.StatusBarCust())
        self.features.append(self.DisableRightClick())
        self.features.append(self.UsingPopupWindow())
        self.features.append(self.IframeRedirection())
        self.features.append(self.AgeofDomain())
        self.features.append(self.DNSRecording())
        self.features.append(self.WebsiteTraffic())
        self.features.append(self.PageRank())
        self.features.append(self.GoogleIndex())
        self.features.append(self.LinksPointingToPage())
        self.features.append(self.StatsReport())

    def UsingIp(self):
        try:
            ipaddress.ip_address(self.url)
            return 1
        except Exception:
            return 0

    def longUrl(self):
        length = len(self.url)
        if length < 54:
            return 0
        if 54 <= length <= 75:
            return 0
        return 1

    def shortUrl(self):
        try:
            pattern = r'(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd)'
            return 1 if re.search(pattern, self.url) else 0
        except Exception:
            return 0

    def symbol(self):
        return 1 if '@' in self.url else 0

    def redirecting(self):
        return 1 if self.url.rfind('//') > 6 else 0

    def prefixSuffix(self):
        try:
            return 1 if '-' in self.domain else 0
        except Exception:
            return 1

    def SubDomains(self):
        dots = self.url.count('.')
        if dots <= 2:
            return 0
        return 1

    def Https(self):
        scheme = self.parsed.scheme if self.parsed else ''
        return 1 if scheme == 'https' else 0

    def DomainRegLen(self):
        who = self.whois_response
        if who and hasattr(who, 'expiration_date') and hasattr(who, 'creation_date'):
            exp = who.expiration_date
            cri = who.creation_date
            if isinstance(exp, list): exp = exp[0]
            if isinstance(cri, list): cri = cri[0]
            if exp and cri:
                months = (exp.year - cri.year) * 12 + (exp.month - cri.month)
                return 1 if months >= 12 else 0
        return 0

    def NonStdPort(self):
        parts = self.domain.split(':')
        return 0 if len(parts) > 1 else 1

    def HTTPSDomainURL(self):
        return 0 if 'https' in self.domain else 1

    def AbnormalURL(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        who = str(self.whois_response) if self.whois_response else ''
        return 1 if text == who else 0

    def WebsiteForwarding(self):
        if isinstance(self.response, requests.Response):
            hist = self.response.history
            return 1 if len(hist) <= 1 else 0
        return 0

    def StatusBarCust(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        return 1 if re.search(r"<script>.+onmouseover.+</script>", text) else 0

    def DisableRightClick(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        return 1 if re.search(r"event.button ?== ?2", text) else 0

    def UsingPopupWindow(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        return 1 if re.search(r"alert\(", text) else 0

    def IframeRedirection(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        return 1 if re.search(r"<iframe|<frameBorder>", text) else 0

    def AgeofDomain(self):
        who = self.whois_response
        if who and hasattr(who, 'creation_date'):
            cri = who.creation_date
            if isinstance(cri, list): cri = cri[0]
            if cri:
                months = (date.today().year - cri.year) * 12 + (date.today().month - cri.month)
                return 1 if months >= 6 else 0
        return 0

    def DNSRecording(self):
        return self.AgeofDomain()

    def WebsiteTraffic(self):
        try:
            xml = urllib.request.urlopen(f"http://data.alexa.com/data?cli=10&dat=s&url={self.url}").read()
            soup = BeautifulSoup(xml, 'xml')
            reach = soup.find('REACH')
            if isinstance(reach, Tag):
                rank = reach.attrs.get('RANK')
                rank_str = str(rank) if rank is not None else ''
                if rank_str.isdigit() and int(rank_str) < 100000:
                    return 1
            return 0
        except Exception:
            return 0

    def PageRank(self):
        try:
            resp = requests.post('https://www.checkpagerank.net/index.php', {'name': self.domain})
            match = re.search(r'Global Rank: ([0-9]+)', resp.text)
            if match:
                val = int(match.group(1))
                return 1 if 0 < val < 100000 else 0
            return 0
        except Exception:
            return 0

    def GoogleIndex(self):
        try:
            return 1 if list(search(self.url, num_results=5)) else 0
        except Exception:
            return 1

    def LinksPointingToPage(self):
        text = self.response.text if isinstance(self.response, requests.Response) else ''
        count = len(re.findall(r"<a href=", text))
        return 1 if count == 0 else 0

    def StatsReport(self):
        try:
            url_match = re.search(r'at\.ua|usa\.cc|hol\.es|ow\.ly', self.url)
            ip = socket.gethostbyname(self.domain) if self.domain else ''
            ip_match = re.search(r'146\.112\.61\.108|192\.185\.217\.116|216\.58\.192\.225|10\.10\.10\.10', ip)
            return 0 if url_match or ip_match else 1
        except Exception:
            return 1

    def getFeaturesList(self):
        return self.features

# Test harness
if __name__ == '__main__':
    sample = "https://youtube.com"
    feat = URLFeature(sample)
    print([f for f in feat.getFeaturesList()])
