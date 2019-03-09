################################################################################

"""
This stores the class(es) used for the text mining project.
"""

################################################################################

import math
import numpy as np
import pickle
import os
import string
import requests

class Error(Exception):
    """Base class for other exceptions"""
    pass
class InvalidBookError(Error):
    """Raised when the book could not be successfully acquired"""
    pass

class Book:
    """
    A book object stores all relevant information about the book (identified by
    name_author) and provides methods for processing each book's data.

    All attributes:
    self.name_author - "Book Title, by Author Name"
    self.path_to_book - "books/path_to_book_text_file"
    self.words_file_path - "books/path_to_the_book_token_file.txt"
    self.words - book parsed into a list of words
    self.hist_file_path - "books/path_to_the_hist_file.txt"
    self.hist - histogram of book's word usage
    """

    def __init__(self, name_author, gutenberg_index, override_existing_download=False):
        """
        Downloads the book from project gutenberg if the book is in
        gutenberg_index. The link to the book is generated from the book's
        associated number in the gutenberg_index, and is downloaded as a text
        file. Returns False if the book couldn't be downloaded or already was
        downloaded (and override_existing_download == False), returns true if
        the book was successfully downloaded.
        """
        self.name_author = name_author

        book_file_path = "books/{}.txt".format(self.name_author)
        try:
            self.path_to_book
        except AttributeError:
            self.path_to_book = book_file_path

        # Check if the book already exists and override it if indicated.
        if os.path.exists(book_file_path):
            if override_existing_download == False:
                print("Book file already exists")
                return None
            else:
                print("Overriding existing download: deleting {}".format(self.book_file_path))
                os.system("rm -rf {}".format(self.book_file_path))

        try:
            book_number = gutenberg_index[self.name_author]
        except KeyError:
            print("Book name/author not in the index.")
            raise InvalidBookError

        book_link_number = ''
        for i in range(1,len(book_number))  :
            # generating the unique part of the download link for the book
            book_link_number = book_link_number + book_number[0:i] + "/"
        book_link_number = book_link_number + book_number + "/" + book_number + ".txt"
        try:
            print("Downloading {}".format(self.name_author))
            book_text = requests.get("http://mirrors.xmission.com/gutenberg/{}".format(book_link_number)).text
            if book_text[0:6] == "<html>": # some links require a different format which is handled below
                book_link_number = book_link_number[0:len(book_link_number)-4]+"-0.txt"
                book_text = requests.get("http://mirrors.xmission.com/gutenberg/{}".format(book_link_number)).text
        except requests.exceptions.MissingSchema:
            print("Invalid url / could not download from this link")
            raise InvalidBookError

        book_text = book_text[2000:len(book_text)-2000]

        book_file = open(book_file_path, 'w')
        book_file.write(book_text)
        book_file.close()
        print("Successfully downloaded {} and wrote to file".format(self.name_author))

    def tokenize_book(self):
        """
        Tokenizes a book into a list of words and writes the data as text file
        (data is pickled).
        """
        data_file_name = self.path_to_book[:len(self.path_to_book)-4] + "___tokenized.txt"
        if os.path.exists(data_file_name):
            file = open(data_file_name, 'rb')
            file_text = file.read()
            words = pickle.loads(file_text)
            file.close()
            try:
                self.words
            except AttributeError:
                self.words = words
            self.length = len(words)
            return words
        else:
            # Information for parsing the book
            punc_list = list(string.punctuation)
            whitespace_list = list(string.whitespace)
            delete_list = punc_list + whitespace_list

            print("Tokenizing {}".format(self.name_author))
            lines = []
            words = []

            with open("books/"+self.name_author+".txt") as text:
                for line in text:
                    processed_line = line.strip()
                    lines.append(processed_line)

            for i in range(len(lines)):
                words.extend(lines[i].split())

            for i in range(len(words)):
                words[i] = words[i].strip("".join(delete_list))
                words[i] = words[i].lower()

            file = open(data_file_name, 'wb')
            data_text = pickle.dumps(words)
            file.write(data_text)
            file.close()
            print('Successfully tokenized and wrote file for {}'.format(self.name_author))

            self.words_file_path = data_file_name
            self.words = words
            self.length = len(words)
            return words

    def make_hist(self):
        """
        Makes a hist (in the form of a dictionary) of word frequency usage
        for the book. Pickles and writes the data to a text file.
        """
        hist_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___hist.txt"
        if not os.path.exists(hist_file_path):
            words = self.tokenize_book
            hist = {}
            for word in self.words:
                hist[word] = hist.get(word,0) + 1

            hist_text = pickle.dumps(hist)
            hist_file = open(hist_file_path, 'wb')
            hist_file.write(hist_text)
            hist_file.close()
            self.hist_file_path = hist_file_path
            self.hist = hist
            print("Histogram for {} successfully made and written to file".format(self.name_author))
            return hist
        else:
            file = open(hist_file_path, 'rb')
            file_text = file.read()
            hist = pickle.loads(file_text)
            try:
                self.hist
            except AttributeError:
                self.hist = hist
            return hist

    def make_atf(self):
        """
        Makes a hist (in the form of a dictionary) of the augmented term
        frequency for each word in the book. Pickles and writes the data to a
        text file. Returns the atf (as a dictionary).

        Augmented term frequency = (raw freq. of word)/(2*raw freq. of most
        occuring word) + 0.5
        """
        atf_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___atf.txt"
        if not os.path.exists(atf_file_path):
            hist = self.hist
            max_word_ct = 0
            for word in hist:
                if hist[word] > max_word_ct:
                    max_word_ct =  hist[word]

            atf = {}
            for word in hist:
                atf[word] = hist[word]/(2*max_word_ct)+0.5

            hist_text = pickle.dumps(atf)
            atf_file = open(atf_file_path, 'wb')
            atf_text = pickle.dumps(atf)
            atf_file.write(atf_text)
            atf_file.close()
            self.atf_file_path = atf_file_path
            self.atf = atf
            print("Histogram for {} successfully made and written to file".format(self.name_author))
            return atf
        else:
            file = open(atf_file_path, 'rb')
            file_text = file.read()
            atf = pickle.loads(file_text)
            file.close()
            try:
                self.atf
            except AttributeError:
                self.atf = atf
            return atf

    def make_random_markov_helper(self):
        random_markov_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___randommarkov.txt"
        if not os.path.exists(random_markov_file_path):
            print("Making helper dictionary for markov chain for {}".format(self.name_author))
            random_markov = {}
            for i in range(len(self.words)-1):
                try:
                    random_markov[self.words[i]].append(self.words[i+1])
                except KeyError:
                    random_markov[self.words[i]] = [self.words[i+1]]

            random_markov_text = pickle.dumps(random_markov)
            random_markov_file = open(random_markov_file_path, 'wb')
            random_markov_file.write(random_markov_text)
            random_markov_file.close()
            self.random_markov_file_path = random_markov_file_path
            self.random_markov = random_markov
            print("Helper dictionary for markov chain for {} successfully made and written to file".format(self.name_author))
            return random_markov
        else:
            file = open(random_markov_file_path, 'rb')
            file_text = file.read()
            random_markov = pickle.loads(file_text)
            file.close()
            try:
                self.random_markov
            except AttributeError:
                self.random_markov = random_markov
            return random_markov

    def make_assisted_markov_helper(self):
        assisted_markov_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___assistedmarkov.txt"
        if not os.path.exists(assisted_markov_file_path):
            print("Making helper dictionary for markov chain for {}".format(self.name_author))
            assisted_markov = {}
            for i in range(len(self.words)-1):
                try:
                    assisted_markov[self.words[i]]
                except KeyError:
                    assisted_markov[self.words[i]] = []
                if self.words[i+1] not in assisted_markov[self.words[i]]:
                    for j in range(int(100*self.atf[self.words[i+1]])):
                        assisted_markov[self.words[i]].append(self.words[i+1])
            assisted_markov_text = pickle.dumps(assisted_markov)
            assisted_markov_file = open(assisted_markov_file_path, 'wb')
            assisted_markov_file.write(assisted_markov_text)
            assisted_markov_file.close()
            self.assisted_markov_file_path = assisted_markov_file_path
            self.assisted_markov = assisted_markov
            print("Helper dictionary for markov chain for {} successfully made and written to file".format(self.name_author))
            return assisted_markov
        else:
            file = open(assisted_markov_file_path, 'rb')
            file_text = file.read()
            assisted_markov = pickle.loads(file_text)
            file.close()
            try:
                self.assisted_markov
            except AttributeError:
                self.assisted_markov = assisted_markov
            return assisted_markov

    def make_book(self, gutenberg_index):
        """
        Runs all Book methods in one go.
        """
        self.tokenize_book()
        self.make_hist()
        self.make_atf()
        self.make_random_markov_helper()
        self.make_assisted_markov_helper()

    def __str__(self):
        return "Book: {}\nBook file: {}\nBook token file: {}\nBook hist\
        file: {}".format(self.name_author, self.book_file_path,
        self.words_file_path, self.hist_file_path)

# class MarkovChainGenerator:
#     def __init__(self, book1_obj, book2_obj):
#         self.book_1 = book1_obj
#         self.book2 =  book2_obj
#
#     def random_markov_chain(self):
