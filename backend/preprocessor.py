import re
from urllib.parse import urlparse, urlsplit, urljoin
import tldextract
import pandas as pd
from typing import *
from bs4 import BeautifulSoup
import requests
import logging
import json, datetime
from pathlib import Path as path
from ipaddress import ip_address
import traceback
import unicodedata
import re


# create logger for preprocessor
logger = logging.getLogger(__name__)

# Given a url get these feature data
# Then return a np.array of those features
TIMEOUT = 10


# def preprocess_data(self, self, url: str):
class preprocess_data:
    url_len = 0
    num_digit = 0
    url: str = ""
    num_obfuscated_char = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }
    # Page data should be list of lines for ease of processing
    page_data: List[str]
    html_data: BeautifulSoup

    # Number of ref tags type
    num_self_ref = 0
    num_empty_ref = 0
    num_external_ref = 0
    has_title: bool = False

    def __init__(self, url: str):
        # We should ensure ending slashes are stripped
        url.strip("/")
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

    # def get_url_similarity_score(self, url: str):

    # TODO: ASK+CHECK WITH KELLY ABOUT THESE TWO FIELDS
    # IF U CANNOT FETCH FROM WEBSITE THEN IT SHOULD RETURN FALSE
    def LineOfCode(self, url: str):
        """
        Count lines in the html code
        Returns 0 if the page can't be fetched.
        """
        # TODO: REDIRECTS ARE BAD HERE
        # TODO: FIX TIMEOUT
        # TODO: NEED TO SWITCH FROM REQUESTS TO SELENIUM BROWSER API
        # Check if request failed!
        try:
            r = requests.get(
                url, allow_redirects=True, timeout=TIMEOUT, headers=self.headers
            )
            # This is the first function that is run for html feature
            # analysis so get the html data for use later
            self.html_data = BeautifulSoup(r.text, "html.parser")
            self.page_data = r.text.splitlines()
            # Count the refs
            self.ref_counts(url)
            return len(r.text.splitlines())
        except Exception as err:
            traceback.print_exc()
            print(err)
            self.page_data = []
            return 0

    def LargestLineLength(self, url: str):
        """
        Find the line with the largest length
        otherwise, return 0
        """
        return max((len(line) for line in self.page_data), default=0)

    def NoOfJS(self, url: str) -> int:
        """
        Count the number of JavaScript "code occurrences" in the fetched HTML.
        This can be defeated if the page is behind some kind of WAF

        Heuristic (fast, no HTML parser dependency):
        - Counts <script> blocks (inline or external via src=)
        - Also counts inline event handlers (onclick=, onload=, etc.)
        - Also counts javascript: URLs

        Returns 0 if the page can't be fetched.
        """
        # TODO: My JS CHECKER MAY OVERCOUNT!
        # Ensure page_data is populated (LineOfCode fetches and sets self.page_data)
        if not hasattr(self, "page_data") or self.page_data is None:
            _ = self.LineOfCode(url)

        if not self.page_data:
            return 0

        html = "\n".join(self.page_data)
        # html = requests.get(
        #     url,
        #     allow_redirects=True,
        #     timeout=10,
        #     headers=self.headers,
        # ).text

        # 1) <script ...> occurrences
        script_tags = len(re.findall(r"<\s*script\b", html, flags=re.IGNORECASE))

        # 2) Inline JS event handlers like onclick=, onsubmit=, onload=, etc.
        # (This is a heuristic: counts any attribute that starts with "on" followed by letters, then '=')
        inline_handlers = len(re.findall(r"\bon[a-z]+\s*=", html, flags=re.IGNORECASE))

        # 3) javascript: pseudo-protocol usage
        js_protocol = len(re.findall(r"\bjavascript\s*:", html, flags=re.IGNORECASE))

        return script_tags + inline_handlers + js_protocol

    def hasFavicon(self, url) -> int:
        """
        Check if the site has a favicon image
        Args:
            url (_type_): url
        """
        # TODO: Check if we should do redirects!
        try:
            r = requests.get(
                url + "/favicon.ico",
                allow_redirects=True,
                timeout=TIMEOUT,
                headers=self.headers,
            )
            if r.status_code >= 200 and r.status_code < 400:
                return 1

        except Exception:
            return 0
        return 0

    def robots(self, url) -> int:
        """
        Check if the site has a robots.txt
        Args:
            url (_type_): url
        """

        try:
            r = requests.get(
                url + "/robots.txt",
                allow_redirects=True,
                timeout=TIMEOUT,
                headers=self.headers,
            )
            if r.status_code >= 200 and r.status_code < 400:
                return 1
        except Exception:
            return 0
        return 0

    def ref_counts(self, url):
        """
        Use this function with the initial html feature analysis at line of code
        as a hook

        Find the number of href tags that either:
        1)point to the main website
        2)Point to another site
        3)empty
        @PreConditions => url is not empty! and HTTPS is present
        Args:
            url (_type_): url
        """
        url_info = urlparse(url)
        base_url: str = url_info.hostname.lower()
        # Check if ending url has slash or not
        # if not base_url.endswith("/"):
        #     base_url += "/"

        self.num_empty_ref = 0
        self.num_external_ref = 0
        self.num_self_ref = 0
        # Usually a tags but also link, script, img, iframe or form
        tags = [
            ("a", "href"),
            ("link", "href"),
            ("script", "src"),
            ("img", "src"),
            ("iframe", "src"),
            ("form", "action"),
        ]
        for nameTag, attri in tags:
            for tag in self.html_data.find_all(nameTag):
                # TODO: remove later because my pylance is fked
                val = tag.get(attri)
                # empty tags should be empty
                if (
                    val == ""
                    or val == None
                    or val == "#"
                    or val.lower().startswith("javascript:")
                ):
                    self.num_empty_ref += 1
                    continue

                # Now check for internal or external
                # urljoin will intelligently join two url if different
                # otherwise www.southbankmosaics.com + https://southbanksmosaics.com will be
                # www.southbankmosaics.com
                absolute_url: str = urljoin(base_url, val)
                external = (urlparse(absolute_url).hostname or "").lower()
                if external == "" or external == base_url:
                    self.num_self_ref += 1
                else:
                    self.num_external_ref += 1

    def NoOfSelfRef(self, url):
        return self.num_self_ref

    def NoOfEmptyRef(self, url):
        return self.num_empty_ref

    def NoOfExternalRef(self, url):
        return self.num_external_ref

    def HasSubmitButton(self, url):
        pass

    def HasTitle(self, url) -> int:
        self.has_title = self.html_data.find("title") is not None
        return 1 if self.has_title is not None else 0

    def pay(self, url):
        pass

    def HasHiddenFields(self, url):
        pass

    def IsResponsive(self, url):
        pass

    def HasDescription(self, url):
        pass

    def HasCopyRightInfo(self, url):
        pass

    def HasSocialNet(self, url):
        pass

    def CharContinuationRate(self, url: str):
        # Return the length of the longest congitguous sequence of:
        # alphabet
        # numbers
        # Special chars
        # https://www.saffronart.com
        # FFS it uses hostname
        # Precondition assume valid url
        hostname = urlsplit(url).hostname.lower()
        if hostname.startswith("www."):
            hostname = hostname[4:]

        # Remove final TLD label to match dataset behaviour
        # saffronart.com => saffronart
        if "." in hostname:
            hostname = hostname.rsplit(".", 1)[0]

        longest_alphabet = [0, ""]
        longest_number = [0, ""]
        longest_special_char = [0, ""]
        for c in hostname:
            if c.isalpha():
                longest_alphabet[1] += c
                longest_alphabet[0] = (
                    len(longest_alphabet[1])
                    if len(longest_alphabet[1]) > longest_alphabet[0]
                    else longest_alphabet[0]
                )
                # Reset the longest sequence of char for other variables
                longest_number[1] = ""
                longest_special_char[1] = ""

            elif c.isdigit():
                longest_number[1] += c
                longest_number[0] = (
                    len(longest_number[1])
                    if len(longest_number[1]) > longest_number[0]
                    else longest_number[0]
                )
                # Reset the longest sequence of char for other variables
                longest_number[1] = ""
                longest_special_char[1] = ""
            # THis is the special chars now
            else:
                longest_special_char[1] += c
                longest_special_char[0] = (
                    len(longest_special_char[1])
                    if len(longest_special_char[1]) > longest_special_char[0]
                    else longest_special_char[0]
                )
                # Reset the longest sequence of char for other variables
                longest_alphabet[1] = ""
                longest_number[1] = ""

        return (
            longest_alphabet[0] + longest_number[0] + longest_special_char[0]
        ) / len(hostname)

    def URLTitleMatchScore(self, url: str):
        """
        This function returns how much the root domain is explained by words
        from the page title
        """
        # If it does not have title then BAD!
        if not self.has_title:
            return 0

        hostname = urlsplit(url).hostname.lower()
        if hostname.startswith("www."):
            hostname = hostname[4:]

        # Remove only the *final* dot-label (dataset behavior).
        # Examples:
        # - saffronart.com      -> saffronart
        # - voicefmradio.co.uk  -> voicefmradio.co
        if "." in hostname:
            hostname = hostname.rsplit(".", 1)[0]

        # Tokenise the title into a set (but normalize first so casing/accents don't break matching)
        title_tag = self.html_data.find("title")
        # Need this to stop linter from complaing
        if title_tag is None:
            return 0

        title_text = title_tag.get_text(" ", strip=True)

        # Normalize to ASCII + lowercase, then extract alnum tokens
        title_norm = unicodedata.normalize("NFKD", title_text)
        title_norm = title_norm.encode("ascii", "ignore").decode("ascii").lower()
        raw_tokens = re.findall(r"[a-z0-9]+", title_norm)

        tokens_title = set(raw_tokens)

        # actual score is here
        score = float(0)
        baseScore = 100 / len(hostname)

        for word in tokens_title:
            if hostname.find(word) >= 0:
                n = len(word)
                score = score + baseScore * n
                hostname.replace(word, "")
                if score > 99.9:
                    return 100.0
        return score

    # TODO: Add other function here AND ALSO DON'T use FEATURE VARS FROM HERE
    # TODO: fix function convention later
    FeatureFn = Callable[["preprocess_data", str], Any]
    func_pointer: ClassVar[list[tuple[FeatureFn, str]]] = [
        (url_length, "URLLength"),
        (domain_length, "DomainLength"),
        (is_domain_ip, "IsDomainIP"),
        (CharContinuationRate, "CharContinuationRate"),
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
        (HasTitle, "HasTitle"),
        (URLTitleMatchScore, "URLTitleMatchScore"),
        (hasFavicon, "HasFavicon"),
        (NoOfJS, "NoOfJS"),
        (robots, "Robots"),
        (NoOfSelfRef, "NoOfSelfRef"),
        (NoOfEmptyRef, "NoOfEmptyRef"),
        (NoOfExternalRef, "NoOfExternalRef"),
        # (HasSubmitButton, "HasSubmitButton")
    ]

    def get_data(self) -> pd.DataFrame:

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
                print(
                    f"PREPROCESSOR ERROR: Feature '{name}' failed on url '{self.url}' with error {e}"
                )

                LOG_DIR = path("logs")
                LOG_DIR.mkdir(exist_ok=True)

                timestamp = datetime.datetime.utcnow().isoformat()
                entry = {
                    "timestamp": timestamp,
                    "log_type": "PREPROCESSOR_ERROR",
                    "message": f"PREPROCESSOR ERROR: Feature '{name}' failed on url '{self.url}' with error {e}",
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
