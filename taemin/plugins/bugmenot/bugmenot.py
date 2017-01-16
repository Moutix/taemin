""" Module to fetch shared login from bugmenot.com"""

from urlparse import urlparse
import re
from bs4 import BeautifulSoup
import requests

class BugMeNot(object):
    """ Class to fetch login from bugmenot.com """

    URL = "http://bugmenot.com/view/{domain}"

    def __init__(self):
        pass

    @classmethod
    def logins(cls, url, _succes_rate_regex=re.compile("^(\d{1,3})%")):
        """ Return the list with all the logins found for this url """
        try:
            res = requests.get(
                url=cls.URL.format(domain=cls.extract_domain(url)),
                timeout=2
            )
        except requests.RequestException:
            return []

        logins = []

        for html_login in BeautifulSoup(res.text, 'html.parser').select("article > dl"):
            login = {}
            elements = ('username', 'password')
            for i, element in enumerate(html_login.select("dd > kbd")):
                if i > len(element):
                    break

                login[elements[i]] = element.getText()

            success_rate = html_login.select("li.success_rate")
            if success_rate:
                match = re.search(_succes_rate_regex, success_rate[0].getText())
                if match:
                    login["confidence"] = 1/float(match.group(1))

            logins.append(login)

        return logins

    @classmethod
    def login(cls, url):
        """ Return the first login found in bugmenot """

        logins = cls.logins(url)
        if not logins:
            return None

        return logins[0]

    @staticmethod
    def extract_domain(url):
        """ Return the domain from a given url """

        if not url.startswith("http://"):
            url = "http://%s" % url

        return urlparse(url).hostname

def main():
    print(BugMeNot.logins("pottermore.com"))

if __name__ == "__main__":
    main()
