"""
This software will take a list of books (book_list) and automatically find,
download, and generate all associated files for the books.
"""

import utility_functions as uf
import pickle

book_list = [
    ('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
    ('Watersprings, by Arthur Christopher Benson'),
]

# Parameters for program
len_markov_chain = 5000  # desired length in words of a markov chain
num_sets_markov_chains = 12  # number of markov chains generated per text; must be a multiple of 3
num_texts_plot = uf.get_num_texts_plot()  # plot the similarity matrix of either 1 text or two texts. If only one text is considered either
# user will choose to input only one text, or opt to use the hard coded list, in which only the first text will be
# considered

uf.check_GUTINDEX()
uf.check_books_folder()

# Load the gutenberg_index dictionary
gutenberg_index_file = open("gutenberg_index.txt", "rb")
gutenberg_index_text = gutenberg_index_file.read()
gutenberg_index = pickle.loads(gutenberg_index_text)
gutenberg_index_file.close()

library = uf.handle_books(gutenberg_index, num_texts_plot)

print("\nExample markov chains:\n")

for book_name_author in library:
    control_markov = uf.control_markov_chain(library[book_name_author])
    print("\nControl markov chain for {}:\n{}".format(book_name_author,uf.list_to_string(control_markov)))
    random_markov = uf.random_markov_chain(library[book_name_author])
    print("\nRandom markov chain for {}:\n{}\n".format(book_name_author,uf.list_to_string(random_markov)))
    assisted_markov = uf.assisted_markov_chain(library[book_name_author])
    print("\nAssisted markov chain for {}:\n{}\n".format(book_name_author,uf.list_to_string(assisted_markov)))
    if num_texts_plot == 1:
        break

text_lists = []
for book in library:
    for i in range(num_sets_markov_chains):
        if num_sets_markov_chains/3 < i:
            text_lists.append(
                uf.control_markov_chain(library[book], len_markov_chain))
        elif num_sets_markov_chains/3 <= i < 2*num_sets_markov_chains/3:
            text_lists.append(
                uf.random_markov_chain(library[book], len_markov_chain))
        else:
            text_lists.append(
                uf.assisted_markov_chain(library[book], len_markov_chain))
    if num_texts_plot == 1:
        break

"""For testing the similarity matrix calculation, uncomment the following line of
code. There should be two points plotted on top of each other and one separated
a small distance from them."""
# text_lists = [['this','is','a','test'],['this','is','a','test'],['this','is','not','a','test']]

matrix = uf.make_similarity_matrix(text_lists)
uf.display_similarity_matrix(matrix, num_sets_markov_chains, num_texts_plot)
