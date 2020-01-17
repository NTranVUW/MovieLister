import urllib

from unidecode import unidecode

from utilities import Printer


class Metacritic:
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse(film):
        if film["Metacritic"] is not None:
            meta = Metacritic(film["Metacritic"]['Link'])
            return meta


    @staticmethod
    def predict_link(title):
        link = ''
        title_split = title.split()
        for t in title_split:
            word = []
            word_as_list = list(t)
            # Only add word if alphanumeric
            for c in word_as_list:
                if c.isalnum():
                    c = unidecode(c)
                    c = c.lower()
                    word.append(c)
            # Covert byte to string
            word_as_string = ''.join(word)
            # Metacritic URLs are in the format: https://www.metacritic.com/movie/word1-word2-word3/
            # Each word in the title separated by a dash
            # No dash at the end of URL
            link = ''.join([link, word_as_string, '-']) if len(word) > 0 else ''.join([link, word_as_string])
        new_link = urllib.parse.urljoin('http://www.metacritic.com/movie/', link[:-1])
        # print(new_link)
        Printer.print_minus(''.join(["MISSING METACRITIC: ", title, ", Predicted Link: ", new_link]))
        return new_link