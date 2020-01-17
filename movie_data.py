import json

import data_handler
import os

import utilities
from utilities import Printer


class MovieCollection:

    def __init__(self, year):
        self.year = year
        self.films = {}
        self.file = ''.join(['resources//', str(self.year), '_data.json'])
        if os.path.isfile(self.file):
            Printer.print_equal('FILE EXISTS: Parsing Data...')
            self.parse_existing_data()
        else:
            Printer.print_equal('FILE DOES NOT EXIST: Creating File...')
            self.get_new_data()
        Printer.print_equal('SAVING FILE')
        self.save_data()

    # TO-DO
    def parse_existing_data(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
            i = 1
            for film in data['films']:
                name = film['Name']
                link = film["Link"]
                Printer.print_minus(''.join(['PARSING: ', str(i), ". ", name, "(", self.year, ")"]))
                self.films[name] = Movie(name, link)
                self.films[name].movie_data = data_handler.DataContainer(self.year, film=film)

    def save_data(self):
        data = {'films': []}
        with open(self.file, 'w') as json_file:
            for film_name in self.films:
                film = self.films[film_name]
                data['films'].append({
                    'Name': film.title,
                    "Link": film.wikipedia_link,
                    "IMDB": film.save_imdb_data(),
                    "Metacritic": film.save_metacritic_data(),
                    "Rotten Tomatoes": film.save_rotten_tomatoes_data(),
                    "Boxofficemojo": film.save_boxofficemojo_data()
                })
            json.dump(data, json_file)

    def get_new_data(self):
        Printer.print_equal('RETRIEVING NEW DATA')
        import wikipedia_handler
        self.films = wikipedia_handler.parse(self.year)
        self.create_data_containers()

    def create_data_containers(self):
        for title, film in self.films.items():
            utilities.count = utilities.count + 1
            Printer.print_equal('')
            Printer.print_minus(''.join(["RETRIEVING DATA: ", str(utilities.count), ". ", title, " - ", self.year]))
            film.movie_data = data_handler.DataContainer(self.year, wikipedia_link=film.wikipedia_link)
            film.movie_data.predict_missing_values(title).find_incorrect_urls(title)


class Movie:
    def __init__(self, title, wikipedia_link):
        self.title = title
        self.wikipedia_link = wikipedia_link
        self.movie_data = None

    def save_imdb_data(self):
        if self.movie_data.imdb is not None:
            return {
                'ID': self.movie_data.imdb.id,
                "Link": self.movie_data.imdb.link
            }
        return None

    def save_metacritic_data(self):
        if self.movie_data.metacritic is not None:
            return {
                'Link': self.movie_data.metacritic.link
            }
        return None

    def save_rotten_tomatoes_data(self):
        if self.movie_data.rotten_tomatoes is not None:
            return {
                'Link': self.movie_data.rotten_tomatoes.link
            }
        return None

    def save_boxofficemojo_data(self):
        if self.movie_data.boxofficemojo is not None:
            return {
                'Link': self.movie_data.boxofficemojo.link
            }
        return None
