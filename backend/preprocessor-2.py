# Given a url get these feature data
# Then return a np.array of those features


# def preprocess_data(self, url: str):
class preprocess_data:
    url_len = 0
    num_digit = 0

    def __init__(self, url: str):
        self.url_len = len(url)

    def domain_len(self, url: str):
        return

    def isDomainIP(self, url: str):
        pass

    def URLLength(self, url: str):
        return len(url)

    def DomainLength(self, url: str):
        pass

    def IsDomainIP(self, url: str):
        pass

    def URLSimilarityIndex(self, url: str):
        pass

    def CharContinuationRate(self, url: str):
        pass

    def TLDLegitimateProb(self, url: str):
        pass

    def URLCharProb(self, url: str):

        pass

    def TLDLength(self, url: str):
        pass

    def NoOfSubDomain(self, url: str):
        pass

    def HasObfuscation(self, url: str):
        pass

    def NoOfObfuscatedChar(self, url: str):
        pass

    def ObfuscationRatio(self, url: str):
        pass

    def NoOfLettersInURL(self, url: str):
        return sum(c.isalpha() for c in url)

    def LetterRatioInURL(self, url: str):
        pass

    def NoOfDigitsInURL(self, url: str):
        return sum(c.isdigit() for c in url)

    def DigitRatioInURL(self, url: str):
        pass

    def NoOfEqualsInURL(self, url: str):
        return sum(c == "=" for c in url)

    def NoOfQMarkInURL(self, url: str):
        pass

    def NoOfAmpersandInURL(self, url: str):
        pass

    def NoOfOtherSpecialCharsInURL(self, url: str):
        pass

    def SpacialCharRatioInURL(self, url: str):
        pass

    def IsHTTPS(self, url: str):
        pass

    def LineOfCode(self, url: str):
        pass

    def LargestLineLength(self, url: str):
        pass

    def HasTitle(self, url: str):
        pass

    def DomainTitleMatchScore(self, url: str):
        pass

    def URLTitleMatchScore(self, url: str):
        pass

    def HasFavicon(self, url: str):
        pass

    def Robots(self, url: str):
        pass

    def IsResponsive(self, url: str):
        pass

    # BELOW IS HTML ANALYSIS
    def NoOfURLRedirect(self, url: str):
        pass

    def NoOfSelfRedirect(self, url: str):
        pass

    def HasDescription(self, url: str):
        pass

    def NoOfPopup(self, url: str):
        pass

    def NoOfiFrame(self, url: str):
        pass

    def HasExternalFormSubmit(self, url: str):
        pass

    def HasSocialNet(self, url: str):
        pass

    def HasSubmitButton(self, url: str):
        pass

    def HasHiddenFields(self, url: str):
        pass

    def HasPasswordField(self, url: str):
        pass

    def Bank(self, url: str):
        pass

    def Pay(self, url: str):
        pass

    def Crypto(self, url: str):
        pass

    def HasCopyrightInfo(self, url: str):
        pass

    def NoOfImage(self, url: str):
        pass

    def NoOfCSS(self, url: str):
        pass

    def NoOfJS(self, url: str):
        pass

    def NoOfSelfRef(self, url: str):
        pass

    def NoOfEmptyRef(self, url: str):
        pass

    def NoOfExternalRef(self, url: str):
        pass

    def IsLegit(self, url: str):
        pass
