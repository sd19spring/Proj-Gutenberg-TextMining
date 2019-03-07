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

class Book:
    def __init__(self, path_to_book):
        self.path_to_book = path_to_book
        self.book_name_author = path_to_book[6:]

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

        with open("books/"+self.book_name_author) as text:
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
