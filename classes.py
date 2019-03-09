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
            return words

    def make_hist(self, words):
        """
        Makes a hist (in the form of a dictionary) of word frequency usage
        for the book. Pickles and writes the data to a text file.
        """
        hist_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___hist.txt"
        if not os.path.exists(hist_file_path):
            hist = {}
            for word in words:
                hist[word] = hist.get(word,0) + 1

            hist_text = pickle.dumps(hist)
            hist_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___hist.txt"
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
            return hist

    def make_atf(self, hist):
        """
        Makes a hist (in the form of a dictionary) of the augmented term
        frequency for each word in the book. Pickles and writes the data to a
        text file. Returns the atf (as a dictionary).

        Augmented term frequency = (raw freq. of word)/(2*raw freq. of most
        occuring word) + 0.5
        """
        atf_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___atf.txt"
        if not os.path.exists(atf_file_path):
            max_word_ct = 0
            for word in hist:
                if hist[word] > max_word_ct:
                    max_word_ct =  hist[word]

            atf = {}
            for word in hist:
                atf[word] = hist[word]/(2*max_word_ct)+0.5

            hist_text = pickle.dumps(atf)
            atf_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___atf.txt"
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
            return atf

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
