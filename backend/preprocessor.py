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
    num_obfuscated_char = 0
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
            [self.url_length, "URLLength"],
            [self.domain_length, "DomainLength"],
            [self.is_domain_ip, "IsDomainIP"],
            [self.tld_length, "TLDLength"],
            [self.no_of_sub_domain, "NoOfSubDomain"],
            [self.has_obfuscation, "HasObfuscation"],
            [self.no_of_obfuscated_char, "NoOfObfuscatedChar"],
            [self.obfuscation_ratio, "ObfuscationRatio"],
            [self.no_of_letters_in_url, "NoOfLettersInURL"],
            [self.letter_ratio_in_url, "LetterRatioInURL"],
            [self.no_of_digits_in_url, "NoOfDigitsInURL"],
            [self.digit_ratio_in_url, "DigitRatioInURL"],
            [self.no_of_equals_in_url, "NoOfEqualsInURL"],
            [self.no_of_q_mark_in_url, "NoOfQMarkInURL"],
            [self.no_of_ampersand_in_url, "NoOfAmpersandInURL"],
            [self.no_of_other_special_chars_in_url, "NoOfOtherSpecialCharsInURL"],
            [self.special_char_ratio_in_url, "SpecialCharRatioInURL"],
            [self.is_https, "IsHTTPS"],
        ]
        # TODO: Add other function here

        # THIS IS WHERE DF FROM URL IS MADE
        # TODO: POTENTIAL OPTIMISATION FOR SPEED POSSIBLE HERE!
        data = {}
        for func, name in func_pointer:
            try:
                result = func(self.url)
                data[name] = [result]
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
                
                data[name] = [None]

        return pd.DataFrame(data)

    def _avoid_div_zero(self, url: str) -> int:
        return max(len(str), 1)

    def url_length(self, url: str):
        return len(url)

    def domain_length(self, url: str):
        domain = urlparse(url).netloc
        return len(domain)

    def is_domain_ip(self, url: str):
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


    def tld_length(self, url: str):
        extracted = tldextract.extract(url)
        tld = extracted.suffix
        return len(tld)


    def no_of_sub_domain(self, url: str):
        extracted = tldextract.extract(url)
        if extracted.subdomain == "":
            return 0
        return len(extracted.subdomain.split("."))


    def has_obfuscation(self, url: str):
        # URL obfuscation according to this article
        # https://pushsecurity.com/blog/detecting-phishing-pages-using-obfuscated-url-destinations
        # is any character after the @ symbol
        # WRONG => DATA SET USES HTML ENCODING FOR DETECTION
        regex = r"%[0-9a-fA-F]{2}"
        return 1 if re.match(regex, url) else 0


    def no_of_obfuscated_char(self, url: str):
        regex = r"%[0-9a-fA-F]{2}"
        found = re.findall(regex, url)
        # HTML encoding always comes in triplets
        # eg: %01 or %0A or %10
        self.num_obfuscated_char = len(found) * 3
        return self.num_obfuscated_char


    def obfuscation_ratio(self, url: str):
        return self.no_of_obfuscated_char(url) / len(url) if len(url) > 0 else 0


    def no_of_letters_in_url(self, url: str):
        """
        Dataset behaviour
        - Count all letters in the hostname, not full url
        - drop leading www if present
        - dataset seems to drop last char wtf
        """
        
        host = (urlparse(url).netloc or "").lower()
        
        if host.startswith("www."):
            host = host[4:]
        
        if host:
            host = host[:-1]
        
        return sum(c.isalpha() for c in host)


    def letter_ratio_in_url(self, url: str):
        return self.no_of_letters_in_url(url) / self._avoid_div_zero(url)


    def no_of_digits_in_url(self, url: str):
        return sum(c.isdigit() for c in url)


    def digit_ratio_in_url(self, url: str):
        return self.no_of_digits_in_url(url) / self._avoid_div_zero(url)


    def no_of_equals_in_url(self, url: str):
        return sum(c in "=" for c in url)


    def no_of_q_mark_in_url(self, url: str):
        return sum(c in "?" for c in url)


    def no_of_ampersand_in_url(self, url: str):
        return sum(c in "&" for c in url)


    def no_of_other_special_chars_in_url(self, url: str):
        special = "!@#$%^*()_+-[]{}|;:'\",<>~`"
        return sum(c in special for c in url)


    def special_char_ratio_in_url(self, url: str):
        total_special = (
            self.no_of_equals_in_url(url)
            + self.no_of_q_mark_in_url(url)
            + self.no_of_ampersand_in_url(url)
            + self.no_of_other_special_chars_in_url(url)
        )

        return total_special / len(url) if len(url) > 0 else 0


    def is_https(self, url: str):
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
