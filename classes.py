################################################################################

"""
This software will calculate the tf-idf scores for words in each book for a set
of books (text files).
"""

################################################################################

import math
import numpy as np
import pickle
import os
import string
import requests

class Book:
    """
    A book object stores all relevant information about the book (identified by
    book_name_author) and provides methods for processing each book's data.

    All attributes:
    self.book_name_author - "Book Title, by Author Name"
    self.path_to_book - "books/path_to_book_text_file"
    self.tokenized_book_file_path - "books/path_to_the_book_token_file.txt"
    self.book_hist_file_path - "books/path_to_the_book_hist_file.txt"
    """
    def __init__(self, book_name_author):
        self.book_name_author = book_name_author

    def collect_book(self, gutenberg_index, override_existing_download=False):
        """
        Downloads the book from project gutenberg if the book is in
        gutenberg_index. The link to the book is generated from the book's
        associated number in the gutenberg_index, and is downloaded as a text
        file. Returns False if the book couldn't be downloaded or already was
        downloaded (and override_existing_download == False), returns true if
        the book was successfully downloaded.
        """
        book_file_path = "books/{}.txt".format(self.book_name_author)

        # Check if the book already exists and override it if indicated.
        if os.path.exists(book_file_path):
            if override_existing_download == False:
                print("Book file already exists")
                return False
            else:
                print("Overriding existing download: deleting {}".format(self.book_file_path))
                os.system("rm -rf {}".format(self.book_file_path))

        try:
            book_number = gutenberg_index[self.book_name_author]
        except KeyError:
            print("Book name/author not in the index.")
            return False

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
            return False

        book_file = open(book_file_path, 'w')
        book_file.write(book_text)
        book_file.close()
        self.path_to_book = book_file_path
        print("Successfully downloaded {} and wrote to file".format(self.book_name_author))
        return True

    def tokenize_book(self):
        """
        Tokenizes a book into a list of words and writes the data as text file
        (data is pickled).
        """
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

        data_file_name = self.path_to_book[:len(self.path_to_book)-4] + "___tokenized.txt"

        if os.path.exists(data_file_name):
            os.system("rm -rf {}".format(data_file_name))
            file = open(data_file_name, 'wb')
            data_text = pickle.dumps(words)
            file.write(data_text)
            file.close()
            print('Replaced original file; successfully built and wrote token file for {}.'.format(self.book_name_author))
        else:
            file = open(data_file_name, 'wb')
            data_text = pickle.dumps(words)
            file.write(data_text)
            file.close()
            print('Successfully tokenized and wrote file for {}'.format(self.book_name_author))

        self.tokenized_book_file_path = data_file_name

    def make_hist(self):
        """
        Makes a hist (in the form of a dictionary) of word frequency usage
        for the book. Pickles and writes the data to a text file.
        """
        if os.path.exists(self.tokenized_book_file_path):
            file = open(self.tokenized_book_file_path, 'rb+')
            file_text = file.read()
            tokens = pickle.loads(file_text)

            hist = {}
            for word in tokens:
                hist[word] = hist.get(word,0) + 1

            hist_text = pickle.dumps(hist)
            hist_file_path = self.path_to_book[:len(self.path_to_book)-4]+"___hist.txt"
            hist_file = open(hist_file_path, 'wb')
            hist_file.write(hist_text)
            hist_file.close()
        else:
            print("Book has not yet been tokenized; this needs to be done \
before a histogram can be made.")
        self.book_hist_file_path = hist_file_path

    def make_book(self, gutenberg_index):
        """
        Runs all Book methods in one go.
        """
        if self.collect_book(gutenberg_index):
            self.tokenize_book()
            self.make_hist()

    def __str__(self):
        return "Book: {}\nBook file: {}\nBook token file: {}\nBook hist\
        file: {}".format(self.book_name_author, self.book_file_path,
        self.tokenized_book_file_path, self.book_hist_file_path)
