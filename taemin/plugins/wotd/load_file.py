""" Script to download all the word here:

http://golfes-dombre.nuxit.net/mots-rares/a.html
"""

import csv
import string
import sys
import re

import bs4
import requests

URL = "http://golfes-dombre.nuxit.net/mots-rares/{letter}.html"

def get_words():
    """ Get all the words """
    for letter in string.ascii_lowercase:
        try:
            page = requests.get(URL.format(letter=letter)).text
        except requests.RequestException as err:
            print("Error on URL '%s': %s" % (URL.format(letter=letter), err), file=sys.stderr)
            continue

        soup = bs4.BeautifulSoup(page, 'html.parser')
        for child in soup.select("p.MsoNormal"):
            names = child.find_all("b")

            text = child.text.replace("\n", " ")

            correctname = []
            for name in names:
                if not name.text.replace("\n", "").strip():
                    continue

                if not re.search(name.text.replace("\n", " ") + r"[\u00A0\s]*:\s*", text):
                    continue

                correctname.append(name)

            names = correctname

            for i, name in enumerate(names):
                regex = name.text.replace("\n", " ") + r"[\u00A0\s]*:\s*"

                if i == len(names) - 1:
                    match = re.search(regex + r"(.+)", text)
                else:
                    match = re.search(regex + r"(.+?)" + names[i + 1].text.replace("\n", " "), text)

                description = match.group(1).strip()

                yield name.text.replace("\n", "").strip(), description.strip()

def main():
    """ Main """

    writer = csv.DictWriter(sys.stdout, ["name", "description"])
    for word in get_words():
        writer.writerow({
            "name": word[0],
            "description": word[1],
        })

if __name__ == "__main__":
    main()
