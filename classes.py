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
    def __init__(self, book_name_author):
        self.book_name_author = book_name_author

    def collect_book(self, gutenberg_index):
        try:
            book_number = gutenberg_index[self.book_name_author]
        except KeyError:
            print("Book name/author not in the index.")
            return False
        book_link_number = ''
        book_file_path = "books/{}.txt".format(self.book_name_author)

        for i in range(len(book_number)):
            book_link_number = book_link_number + book_number[0:i] + "/"
        book_link_number = book_link_number + book_file_path
        try:
            book_text = requests.get("http://mirrors.xmission.com/gutenberg/{}".format(book_link_number)).text
        except requests.exceptions.MissingSchema:
            print("Invalid url / could not download from this link.")
            return False
        if os.path.exists(book_file_path):
            print("Book already exists.")
            return False
        else:
            book_file = open(book_file_path, 'w')
            book_file.write(book_text)
            book_file.close()
            self.path_to_book = book_file_path
            return True

    def tokenize_book(self):
        """
        Tokenizes a book into a list of words and writes the data as text file
        (data is pickled).
        """
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
        try:
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
                print('Successfully built and wrote dataset for {}'.format(self.book_name_author))
        except:
            print("An error occured trying to tokenize the book: {}".format(self.book_name_author))
        self.tokenized_book_file_path = data_file_name

    def make_hist(self):

        if os.path.exists(self.tokenized_book_file_path):
            file = open(self.tokenized_book_file_path, 'rb+')
            file_text = file.read()
            tokens = pickle.loads(file_text)

            hist = {}
            for word in tokens:
                hist[word] = hist.get(word,0) + 1

            hist_text = pickle.dumps(hist)
            hist_file_path = self.tokenized_book_file_path[:len(self.tokenized_book_file_path)-16]+"___hist.txt"
            hist_file = open(hist_file_path, 'wb')
            hist_file.write(hist_text)
            hist_file.close()
        else:
            print("Book has not yet been tokenized; this needs to be done before a hist can be made.")

    def make_book(self, gutenberg_index):
        if self.collect_book(gutenberg_index):
            self.tokenize_book()
            self.make_hist()
