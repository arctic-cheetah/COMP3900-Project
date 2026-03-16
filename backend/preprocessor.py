import re
from urllib.parse import urlparse, urlsplit
import tldextract
import pandas as pd
from typing import *
import requests
import logging
import json, datetime
from pathlib import Path as path
from ipaddress import ip_address


# create logger for preprocessor
logger = logging.getLogger(__name__)

# Given a url get these feature data
# Then return a np.array of those features


# def preprocess_data(self, self, url: str):
class preprocess_data:
    url_len = 0
    num_digit = 0
    func_pointer: List[Callable]
    url: str = ""
    numObfuscatedChar = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }
    # Page data should be list of lines for ease of processing
    page_data: List[str]


    def __init__(self, url: str):
        self.url_len = len(url)
        self.url = url


    def get_data(self) -> pd.DataFrame:
        func_pointer = [
            [self.URLLength, "URLLength"],
            [self.DomainLength, "DomainLength"],
            [self.IsDomainIP, "IsDomainIP"],
            [self.TLDLength, "TLDLength"],
            [self.NoOfSubDomain, "NoOfSubDomain"],
            [self.HasObfuscation, "HasObfuscation"],
            [self.NoOfObfuscatedChar, "NoOfObfuscatedChar"],
            [self.ObfuscationRatio, "ObfuscationRatio"],
            [self.NoOfLettersInURL, "NoOfLettersInURL"],
            [self.LetterRatioInURL, "LetterRatioInURL"],
            [self.NoOfDigitsInURL, "NoOfDigitsInURL"],
            [self.DigitRatioInURL, "DigitRatioInURL"],
            [self.NoOfEqualsInURL, "NoOfEqualsInURL"],
            [self.NoOfQMarkInURL, "NoOfQMarkInURL"],
            [self.NoOfAmpersandInURL, "NoOfAmpersandInURL"],
            [self.NoOfOtherSpecialCharsInURL, "NoOfOtherSpecialCharsInURL"],
            [self.SpacialCharRatioInURL, "SpacialCharRatioInURL"],
            [self.IsHTTPS, "IsHTTPS"],
        ]
        # TODO: Add other function here

        dat = {}
        # better variable names cuz it took me way too long to figure out what x was doing
        for func, name in func_pointer:
            try:
                result = func(self.url)
                dat[name] = [result]
            except Exception as e:
                print(f"PREPROCESSOR ERROR: Feature '{name}' failed on url '{self.url}' with error {e}")
                
                LOG_DIR = path("logs")
                LOG_DIR.mkdir(exist_ok=True)

                timestamp = datetime.datetime.utcnow().isoformat()
                entry = {
                    "timestamp": timestamp,
                    "log_type": "PREPROCESSOR_ERROR",
                    "message": f"PREPROCESSOR ERROR: Feature '{name}' failed on url '{self.url}' with error {e}"
                }

                with open(LOG_DIR / "preprocessor_errors.txt", "a") as f:
                    f.write(json.dumps(entry) + "\n")
                
                dat[name] = [None]

        return pd.DataFrame(dat)


        # THIS IS WHERE DF FROM URL IS MADE
        # TODO: POTENTIAL OPTIMISATION FOR SPEED POSSIBLE HERE!
        # for x in func_pointer:
        #     # print((x[1], x[0](self.url)))
        #     dat[x[1]] = [x[0](self.url)]
        # return pd.DataFrame(dat)
    def URLLength(self, url: str):
        return len(url)

    def DomainLength(self, url: str):
        domain = urlparse(url).netloc
        return len(domain)

    def IsDomainIP(self, url: str):
        """
            Checks if domain is an IP address.
            
            Args:
                url (str): The URL to be checked.
            
            Returns:
                int: Returns 1 if domain is IP, otherwise 0.
        """
        parsed_url = urlsplit(url)
        hostname = str(parsed_url.hostname)
       
        try:
            ip_address("hostname")
            return 1
        except ValueError:
            return 0
        except Exception as e:
            print(f'is_domain_ip error: "{e}"')


    def TLDLength(self, url: str):
        extracted = tldextract.extract(url)
        tld = extracted.suffix
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
        # WRONG => DATA SET USES HTML ENCODING FOR DETECTION
        regex = r"%[0-9a-fA-F]{2}"
        return 1 if re.match(regex, url) is None else 0


    def NoOfObfuscatedChar(self, url: str):
        regex = r"%[0-9a-fA-F]{2}"
        found = re.findall(regex, url)
        # HTML encoding always comes in triplets
        # eg: %01 or %0A or %10
        self.numObfuscatedChar = len(found) * 3
        return self.numObfuscatedChar


    def ObfuscationRatio(self, url: str):
        return self.NoOfObfuscatedChar(url) / len(url) if len(url) > 0 else 0


    def NoOfLettersInURL(self, url: str):
        # Count number of unique letters!
        ht = set()
        for c in url:
            if c.isalpha():
                ht.add(c)

        return len(ht)


    def LetterRatioInURL(self, url: str):
        return self.NoOfLettersInURL(url) / len(url) if len(url) > 0 else 0


    def NoOfDigitsInURL(self, url: str):
        return sum(c.isdigit() for c in url)


    def DigitRatioInURL(self, url: str):
        return self.NoOfDigitsInURL(url) / len(url) if len(url) > 0 else 0


    def NoOfEqualsInURL(self, url: str):
        return sum(c in "=" for c in url)


    def NoOfQMarkInURL(self, url: str):
        return sum(c in "?" for c in url)


    def NoOfAmpersandInURL(self, url: str):
        return sum(c in "&" for c in url)


    def NoOfOtherSpecialCharsInURL(self, url: str):
        special = "!@#$%^*()_+-[]{}|;:'\",<>~`"
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
        return 1 if url.strip().lower().startswith("https://") else 0


# TODO: Gotta run the class
# tmp_example = "wtf.com"
# obfuscation = "https://s3.amazonaws.com/appforest_uf/f1678949673383x832048620362898600/index%20%284%29.html"
# safe = "https://www.saffronart.com"
# example = preprocess_data(obfuscation)
# safeURL = preprocess_data(safe)
# obfuscated = example.get_data()
# s = safeURL.get_data()

# print(s)
# print(obfuscated)
