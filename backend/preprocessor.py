import re
from urllib.parse import urlparse, urlsplit
import tldextract
import pandas as pd
from typing import *
from types import MethodType
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



    def _avoid_div_zero(self, url: str) -> int:
        return max(len(url) - 1, 1)

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
        return self.no_of_obfuscated_char(url) / self._avoid_div_zero(url)


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

        return total_special / self._avoid_div_zero(url)


    def is_https(self, url: str):
        return 1 if url.strip().lower().startswith("https://") else 0
    
    
    # TODO: ASK+CHECK WITH KELLY ABOUT THESE TWO FIELDS
    # IF U CANNOT FETCH FROM WEBSITE THEN IT SHOULD RETURN FALSE
    def LineOfCode(self, url: str):
        """
        Count lines in the html code
        Returns 0 if the page can't be fetched.
        """
        # TODO: REDIRECTS ARE BAD HERE
        # Check if request failed!
        try:
            r = requests.get(
                url, allow_redirects=True, timeout=10, headers=self.headers
            )
            self.page_data = r.text.splitlines()
            return len(r.text.splitlines())
        except Exception as err:
            print(err)
            self.page_data = []
            return 0

    def LargestLineLength(self, url: str):
        """
        Find the line with the largest length
        otherwise, return 0
        """
        return max((len(line) for line in self.page_data), default=0)

    
    def NoOfJSCode(self, url: str) -> int:
        """
        Count the number of JavaScript "code occurrences" in the fetched HTML.

        Heuristic (fast, no HTML parser dependency):
        - Counts <script> blocks (inline or external via src=)
        - Also counts inline event handlers (onclick=, onload=, etc.)
        - Also counts javascript: URLs

        Returns 0 if the page can't be fetched.
        """
        # Ensure page_data is populated (LineOfCode fetches and sets self.page_data)
        if not hasattr(self, "page_data") or self.page_data is None:
            _ = self.LineOfCode(url)

        if not self.page_data:
            return 0

        html = "\n".join(self.page_data)

        # 1) <script ...> occurrences
        script_tags = len(re.findall(r"<\s*script\b", html, flags=re.IGNORECASE))

        # 2) Inline JS event handlers like onclick=, onsubmit=, onload=, etc.
        # (This is a heuristic: counts any attribute that starts with "on" followed by letters, then '=')
        inline_handlers = len(re.findall(r"\bon[a-z]+\s*=", html, flags=re.IGNORECASE))

        # 3) javascript: pseudo-protocol usage
        js_protocol = len(re.findall(r"\bjavascript\s*:", html, flags=re.IGNORECASE))

        return script_tags + inline_handlers + js_protocol
    
    
    FeatureFn = Callable[["preprocess_data", str], Any]
    func_pointer: ClassVar[list[tuple[FeatureFn, str]]] = [
        (url_length, "URLLength"),
        (domain_length, "DomainLength"),
        (is_domain_ip, "IsDomainIP"),
        (tld_length, "TLDLength"),
        (no_of_sub_domain, "NoOfSubDomain"),
        (has_obfuscation, "HasObfuscation"),
        (no_of_obfuscated_char, "NoOfObfuscatedChar"),
        (obfuscation_ratio, "ObfuscationRatio"),
        (no_of_letters_in_url, "NoOfLettersInURL"),
        (letter_ratio_in_url, "LetterRatioInURL"),
        (no_of_digits_in_url, "NoOfDigitsInURL"),
        (digit_ratio_in_url, "DigitRatioInURL"),
        (no_of_equals_in_url, "NoOfEqualsInURL"),
        (no_of_q_mark_in_url, "NoOfQMarkInURL"),
        (no_of_ampersand_in_url, "NoOfAmpersandInURL"),
        (no_of_other_special_chars_in_url, "NoOfOtherSpecialCharsInURL"),
        (special_char_ratio_in_url, "SpecialCharRatioInURL"),
        (is_https, "IsHTTPS"),
        (LineOfCode, "LineOfCode"),
        (LargestLineLength, "LargestLineLength"),
        (NoOfJSCode, "NoOfJSCode"),
    ]
    
    def get_data(self) -> pd.DataFrame:
        # TODO: Add other function here

        # THIS IS WHERE DF FROM URL IS MADE
        # TODO: POTENTIAL OPTIMISATION FOR SPEED POSSIBLE HERE!
        data = {}
        for func, name in self.func_pointer:
            try:
                # result = func(self, self.url)
                # The methods stored in func pointer belong to class => need to bind it to the object
                bounded_func: Callable = getattr(self, func.__name__)
                data[name] = [bounded_func(self.url)]
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
