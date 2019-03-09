################################################################################

"""
This software will take a list of books (book_list) and automatically find,
download, and generate all associated files for the books.
"""

################################################################################

import random
import requests
import os
import classes as cl
import utility_functions as uf
import pickle

################################################################################

# book_list = [
# ('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
# ('A Tale of Two Cities, by Charles Dickens'),
# ('The Adventures of Sherlock Holmes, by Arthur Conan Doyle'),
# ('Adventures of Huckleberry Finn, by Mark Twain'),
# ('The Yellow Wallpaper, by Charlotte Perkins Gilman'),
# ('Metamorphosis, by Franz Kafka')
# ]

book_list = [
('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
('A Tale of Two Cities, by Charles Dickens'),
]


uf.check_GUTINDEX()
uf.check_books_folder()

# Load the gutenberg_index dictionary
gutenberg_index_file = open("gutenberg_index.txt", "rb")
gutenberg_index_text = gutenberg_index_file.read()
gutenberg_index = pickle.loads(gutenberg_index_text)
gutenberg_index_file.close()

library = uf.handle_books(gutenberg_index)
