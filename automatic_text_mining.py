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

for book_name_author in library:
    control_markov = uf.control_markov_chain(library[book_name_author])
    print("\nControl markov chain for {}:\n{}".format(book_name_author,control_markov))
    random_markov = uf.random_markov_chain(library[book_name_author])
    print("\nRandom markov chain for {}:\n{}\n".format(book_name_author,random_markov))
    assisted_markov = uf.assisted_markov_chain(library[book_name_author])
    print("\nAssisted markov chain for {}:\n{}\n".format(book_name_author,assisted_markov))
