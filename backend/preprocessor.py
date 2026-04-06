import re
from urllib.parse import urlparse, urlsplit
import tldextract
import pandas as pd
from typing import *

# Given a url get these feature data
# Then return a np.array of those features


# def preprocess_data(self, self, url: str):
class preprocess_data:
    url_len = 0
    num_digit = 0
    func_pointer: List[callable] = {}


    def __init__(self, url: str):
        self.url_len = len(url)
    
    def get_data(self, url:str):
        func_pointer = [
            [self.URLLength, "URLLength"],
            [self.DomainLength, "DomainLength"]
            # TODO: Add other function here
        ]
        for x in func_pointer:
            print(x[0](url))
        pass
    
    def URLLength(self, url: str):
        return len(url)

    def DomainLength(self, url: str):
        domain = urlparse(url).netloc
        return len(domain)

    def IsDomainIP(self, url: str):
        parsed_url = urlsplit(url)
        regexIPV4 = r"\d+\.\d+\.\d+\.\d+"
        regexIPV6 = r"/^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/"

        ipv4 = re.match(regexIPV4, str(parsed_url.hostname))
        ipv6 = re.match(regexIPV6, str(parsed_url.hostname))
        return (ipv6 is None) or (ipv4 is None)

    def TLDLength(self, url: str):
        extracted = tldextract.extract(url)
        tld = extracted.suffix()
        return len(tld)

    def NoOfSubDomain(self, url: str):
        extracted = tldextract.extract(url)
        if extracted.subdomain == "":
            return 0
        return len(extracted.subdomain.split("."))

    def HasObfuscation(self, url: str):
        # URL obfuscation according to this article
        # https://pushsecurity.com/blog/detecting-phishing-pages-using-obfuscated-url-destinations
        # is any character after the @ symbol
        regex = r"@[@\w.-]+"
        return re.match(regex, url) is None

    def NoOfObfuscatedChar(self, url: str):
        return len(url.split("@", 1)[1]) if "@" in url else 0

    def ObfuscationRatio(self, url: str):
        return self.NoOfObfuscatedChar(url) / len(url) if len(url) > 0 else 0

    def NoOfLettersInURL(self, url: str):
        return sum(c.isalpha() for c in url)

    def LetterRatioInURL(self, url: str):
        return self.NoOfLettersInURL(url) / len(url) if len(url) > 0 else 0

    def NoOfDegitsInURL(self, url: str):
        return sum(c.isdigit() for c in url)

    def DegitRatioInURL(self, url: str):
        return self.NoOfDegitsInURL(url) / len(url) if len(url) > 0 else 0

    def NoOfEqualsInURL(self, url: str):
        return sum(c in "=" for c in url)

    def NoOfQMarkInURL(self, url: str):
        return sum(c in "?" for c in url)

    def NoOfAmpersandInURL(self, url: str):
        return sum(c in "&" for c in url)

    def NoOfOtherSpecialCharsInURL(self, url: str):
        special = "!@#$%^*()_+-[]{}|;:'\",<>/~`"
        return sum(c in special for c in url)

    def SpacialCharRatioInURL(self, url: str):
        total_special = (
            self.NoOfEqualsInURL(url)
            + self.NoOfQMarkInURL(url)
            + self.NoOfAmpersandInURL(url)
            + self.NoOfOtherSpecialCharsInURL(url)
        )

        return total_special / len(url) if len(url) > 0 else 0

    def IsHTTPS(self, url: str):
        return url.strip().lower().startswith("https://")

    def LineOfCode(self, url: str):
        return url.count("\n") + 1 if url else 0

    def LargestLineLength(self, url: str):
        return max((len(line) for line in url.splitlines()), default=0)


# TODO: Gotta run the class
tmp_example = "wtf.com"
preprocess_data(tmp_example)