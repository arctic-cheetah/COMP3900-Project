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
    func_pointer: List[Callable]
    url: str = ""
    numObfuscatedChar = 0

    def __init__(self, url: str):
        self.url_len = len(url)
        self.url = url

    def get_data(self) -> pd.DataFrame:
        func_pointer = [
            [self.URLLength, "URLLength"],
            [self.DomainLength, "DomainLength"],
            [self.IsDomainIP, "isDomainIP"],
            [self.TLDLength, "TLDLength"],
            [self.NoOfSubDomain, "NoOfSubDomain"],
            [self.HasObfuscation, "HasObfuscation"],
            [self.NoOfObfuscatedChar, "NoOfObfuscatedChar"],
            [self.ObfuscationRatio, "ObfuscationRatio"],
            [self.NoOfLettersInURL, "NoOfLettersInURL"],
            [self.NoOfDegitsInURL, "NoOfDegitsInURL"],
            [self.DegitRatioInURL, "DegitRatioInURL"],
            [self.NoOfEqualsInURL, "NoOfEqualsInURL"],
            [self.NoOfQMarkInURL, "NoOfQMarkInURL"],
            [self.NoOfAmpersandInURL, "NoOfAmpersandInURL"],
            [self.NoOfOtherSpecialCharsInURL, "NoOfOtherSpecialCharsInURL"],
            [self.SpacialCharRatioInURL, "SpacialCharRatioInURL"],
            [self.IsHTTPS, "IsHTTPS"],
            [self.LineOfCode, "LineOfCode"],
            [self.LargestLineLength, "LargestLineLength"],
        ]
        # TODO: Add other function here

        dat = {}
        # THIS IS WHERE DF FROM URL IS MADE
        # TODO: POTENTIAL OPTIMISATION FOR SPEED POSSIBLE HERE!
        for x in func_pointer:
            # print((x[1], x[0](self.url)))
            dat[x[1]] = [x[0](self.url)]
        return pd.DataFrame(dat)

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
        return 1 if (ipv6 is None) or (ipv4 is None) else 0

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
        regex = r"%\d{2}"
        return 1 if re.match(regex, url) is None else 0

    def NoOfObfuscatedChar(self, url: str):
        regex = r"%\d{2}"
        found = re.findall(regex, url)
        # HTML encoding always comes in triplets
        # eg: %01 or %0A or %10
        self.numObfuscatedChar = len(found) * 3
        return self.numObfuscatedChar

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
        return 1 if url.strip().lower().startswith("https://") else 0

    # TODO: ASK+CHECK WITH KELLY ABOUT THESE TWO FIELDS
    # IF U CANNOT FETCH FROM WEBSITE THEN IT SHOULD RETURN FALSE
    def LineOfCode(self, url: str):
        return url.count("\n") + 1 if url else 0

    def LargestLineLength(self, url: str):
        return max((len(line) for line in url.splitlines()), default=0)


# TODO: Gotta run the class
tmp_example = "wtf.com"
obfuscation = "https://s3.amazonaws.com/appforest_uf/f1678949673383x832048620362898600/index%20%284%29.html"
example = preprocess_data(obfuscation)
df = example.get_data()
print(df)
