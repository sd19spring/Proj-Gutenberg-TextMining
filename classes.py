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
    book_name_author) and provides methods for processing each book's data.

    All attributes:
    self.book_name_author - "Book Title, by Author Name"
    self.path_to_book - "books/path_to_book_text_file"
    self.tokenized_book_file_path - "books/path_to_the_book_token_file.txt"
    self.tokenized_book - book parsed into a list of words
    self.book_hist_file_path - "books/path_to_the_book_hist_file.txt"
    self.book_hist - histogram of book's word usage
    """
    def __init__(self, book_name_author, gutenberg_index):
        """
        Downloads the book from project gutenberg if the book is in
        gutenberg_index. The link to the book is generated from the book's
        associated number in the gutenberg_index, and is downloaded as a text
        file. Returns False if the book couldn't be downloaded or already was
        downloaded (and override_existing_download == False), returns true if
        the book was successfully downloaded.
        """
        self.book_name_author = book_name_author

        book_file_path = "books/{}.txt".format(self.book_name_author)

        # Check if the book already exists and override it if indicated.
        if os.path.exists(book_file_path):
            if override_existing_download == False:
                print("Book file already exists")
                raise InvalidBookError
            else:
                print("Overriding existing download: deleting {}".format(self.book_file_path))
                os.system("rm -rf {}".format(self.book_file_path))

        try:
            book_number = gutenberg_index[self.book_name_author]
        except KeyError:
            print("Book name/author not in the index.")
            raise InvalidBookError

        book_link_number = ''
        for i in range(len(book_number)):
            # generating the unique part of the download link for the book
            book_link_number = book_link_number + book_number[0:i] + "/"
        book_link_number = book_link_number + book_file_path

        try:
            print("Downloading {}".format(self.book_name_author))
            book_text = requests.get("http://mirrors.xmission.com/gutenberg/{}".format(book_link_number)).text
        except requests.exceptions.MissingSchema:
            print("Invalid url / could not download from this link")
            raise InvalidBookError

        book_file = open(book_file_path, 'w')
        book_file.write(book_text)
        book_file.close()
        self.path_to_book = book_file_path
        print("Successfully downloaded {} and wrote to file".format(self.book_name_author))

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
                self.tokenized_book
            except AttributeError:
                self.tokenized_book = words
            return words
        else:
            # Information for parsing the book
            punc_list = list(string.punctuation)
            whitespace_list = list(string.whitespace)
            delete_list = punc_list + whitespace_list

            print("Tokenizing {}".format(self.book_name_author))
            lines = []
            words = []

            with open("books/"+self.book_name_author+".txt") as text:
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
            print('Successfully tokenized and wrote file for {}'.format(self.book_name_author))

            self.tokenized_book_file_path = data_file_name
            self.tokenized_book = words
            self.book_length = len(words)
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
            for word in words:
                hist[word] = hist.get(word,0) + 1

            hist_text = pickle.dumps(hist)
            hist_file = open(hist_file_path, 'wb')
            hist_file.write(hist_text)
            hist_file.close()
            self.book_hist_file_path = hist_file_path
            self.book_hist = hist
            print("Histogram for {} successfully made and written to file".format(self.book_name_author))
            return hist
        else:
            file = open(hist_file_path, 'rb')
            file_text = file.read()
            hist = pickle.loads(file_text)
            try:
                self.book_hist
            except AttributeError:
                self.book_hist = hist
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
            hist = self.book_hist
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
            self.book_atf_file_path = atf_file_path
            self.book_atf = atf
            print("Histogram for {} successfully made and written to file".format(self.book_name_author))
            return atf
        else:
            file = open(atf_file_path, 'rb')
            file_text = file.read()
            atf = pickle.loads(file_text)
            file.close()
            try:
                self.book_atf
            except AttributeError:
                self.book_atf = atf
            return atf

    def make_random_markov_helper(self):
        random_rmf_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___rmf.txt"
        if not os.path.exists(random_rmf_file_path):
            words = self.tokenize_book
            hist = self.book_hist

            print("Making helper dictionary for markov chain for {}".format(self.book_name_author))
            random_rmf = {}
            for i in range(len(words)-1):
                try:
                    random_rmf[words[i]].append(words[i+1])
                except KeyError:
                    random_rmf[words[i]] = [words[i+1]]

            random_rmf_text = pickle.dumps(random_rmf)
            random_rmf_file = open(random_rmf_file_path, 'wb')
            random_rmf_file.write(random_rmf_text)
            random_rmf_file.close()
            self.book_random_rmf_file_path = random_rmf_file_path
            self.book_random_rmf = random_rmf
            print("Helper dictionary for markov chain for {} successfully made and written to file".format(self.book_name_author))
            return random_rmf
        else:
            file = open(random_rmf_file_path, 'rb')
            file_text = file.read()
            random_rmf = pickle.loads(file_text)
            file.close()
            try:
                self.book_random_rmf
            except AttributeError:
                self.book_random_rmf = random_rmf
            return random_rmf

    def make_assisted_markov_helper(self):
        if not os.path.exists(assisted_rmf_file_path):
            words = self.tokenize_book
            hist = self.book_hist

            print("Making helper dictionary for markov chain for {}".format(self.book_name_author))
            assisted_rmf = {}
            for i in range(len(words)-1):
                try:
                    if words[i+1] not in assisted_rmf[words[i]]:
                        for i in range(self.book_atf[words[i+1]]):
                            assisted_rmf[words[i]].append(words[i+1])
                except KeyError:
                    assisted_rmf[words[i]] = []
                    if words[i+1] not in assisted_rmf[words[i]]:
                        for i in range(self.book_atf[words[i+1]]):
                            assisted_rmf[words[i]].append(words[i+1])

            assisted_rmf_text = pickle.dumps(assisted_rmf)
            assisted_rmf_file = open(assisted_rmf_file_path, 'wb')
            assisted_rmf_file.write(assisted_rmf_text)
            assisted_rmf_file.close()
            self.book_assisted_rmf_file_path = assisted_rmf_file_path
            self.book_assisted_rmf = assisted_rmf
            print("Helper dictionary for markov chain for {} successfully made and written to file".format(self.book_name_author))
            return assisted_rmf
        else:
            file = open(assisted_rmf_file_path, 'rb')
            file_text = file.read()
            assisted_rmf = pickle.loads(file_text)
            file.close()
            try:
                self.assisted_rmf
            except AttributeError:
                self.assisted_rmf = assisted_rmf
            return assisted_rmf

    def make_book(self, gutenberg_index):
        """
        Runs all Book methods in one go.
        """

        words = self.tokenize_book()
        hist = self.make_hist(words)
        atf = self.make_atf(hist)

    def __str__(self):
        return "Book: {}\nBook file: {}\nBook token file: {}\nBook hist\
        file: {}".format(self.book_name_author, self.book_file_path,
        self.tokenized_book_file_path, self.book_hist_file_path)

# class MarkovChainGenerator:
#     def __init__(self, book1_obj, book2_obj):
#         self.book_1 = book1_obj
#         self.book2 =  book2_obj
#
#     def random_markov_chain(self):
