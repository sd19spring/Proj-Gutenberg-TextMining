"""
This contains the functions that classes.py and automatic_text_mining.py reference
"""

import random
import requests
import os
import classes as cl
import pickle
import math
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import doctest

book_list = [
    ('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
    ('Watersprings, by Arthur Christopher Benson'),
]

def get_num_texts_plot():
    while True:
        num_texts_plot = input("Would you like to perform calculations with one or two texts? 1 or 2 --> ")
        if num_texts_plot == "1":
            num = int(num_texts_plot)
            break
        elif num_texts_plot == "2":
            num = int(num_texts_plot)
            break
        else:
            print("Invalid input, please try again")
            continue
    return num


def list_to_string(list):
    """
    Takes a list of strings and returns a string that is the combination of the
    strings in the list.

    >>> list_to_string(['this','is','a','test'])
    this is a test
    """
    return_string = ""
    for word in list:
        return_string = return_string + word + " "
    return return_string


def build_gutenberg_index():
    """
    Generates a python-readable index of project gutenberg's master index -
    GUTINDEX.txt - called gutenberg_index.txt. Returns a dictionary of the
    index. If gutenberg_index.txt exists, it is deleted and re-downloaded.
    :return gutenberg_index: a dictionary that is built from GUTINDEX
    """
    if os.path.exists("gutenberg_index.txt"):
        print("Deleting old gutenberg_index.txt file.")
        os.system("rm -rf gutenberg_index.txt")

    gut_index_file = open("GUTINDEX.txt", 'r+')
    gut_index_text = gut_index_file.read()
    gut_index_file.close()

    # Hard coding conditions that the text parser will use:
    skip_line_if = [" ", "~", "TITLE"]
    end_title_if = ["  ", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
    gutenberg_index = {}

    print("Generating gutenberg_index dictionary and writing as gutenberg_index.txt")
    # The following code is what parses the text file into a dictionary
    gut_lines = gut_index_text.split("\n")
    for line in gut_lines[260:]:
        if line == "<==End of GUTINDEX.ALL==>":
            break
        else:
            # Skip empty lines
            if len(line) != 0:
                if line[0] not in skip_line_if or line[0:5] not in skip_line_if:
                    # At this point, the line in consideration will have a book title/author name and index number
                    for i in range(len(line) - 1):
                        if line[i:i + 2] in end_title_if:
                            # Find where the book title ends in the line
                            book_name_author = line[0:i]
                            for j in range(0, len(line)):
                                if line[len(line) - j - 1] == " ":
                                    # Pull out the index number of the book
                                    book_number = line[len(line) - j:len(line)]
                                    break
                            gutenberg_index[book_name_author] = book_number
                            break
    gut_index_file = open("gutenberg_index.txt", 'wb')
    to_write = pickle.dumps(gutenberg_index)
    gut_index_file.write(to_write)
    gut_index_file.close()
    print("Index successfully generated and written to disk as gutenberg_index.txt")
    return gutenberg_index


def check_GUTINDEX():
    """
    Handles the GUTINDEX.txt file - either download it for the first time or
    redownloads the file.
    """
    if os.path.exists("GUTINDEX.txt"):
        while True:
            yn = input(
                "Redownload the index of project gutenberg - GUTINDEX.txt - and delete the old one? New books may have been added. y/n --> ")
            if yn == "y" or yn == "Y":
                print("Deleting old GUTINDEX.txt file")
                os.system("rm -rf GUTINDEX.txt")
                print("Downloading the GUTINDEX file...")
                try:
                    GUTINDEX = requests.get("https://www.gutenberg.org/dirs/GUTINDEX.ALL").text
                except requests.exceptions.MissingSchema:
                    print("Invalid url / could not download from this link")
                    break
                GUTINDEX_file = open("GUTINDEX.txt", "w")
                GUTINDEX_file.write(GUTINDEX)
                GUTINDEX_file.close()

                build_gutenberg_index()

                break
            elif yn == "n" or yn == "N":
                break
            else:
                print("Invalid input; try again")
                continue
    else:
        try:
            print("Downloading the GUTINDEX file...")
            GUTINDEX = requests.get("https://www.gutenberg.org/dirs/GUTINDEX.ALL").text
        except requests.exceptions.MissingSchema:
            print("Invalid url / could not download from this link")
        GUTINDEX_file = open("GUTINDEX.txt", "w")
        GUTINDEX_file.write(GUTINDEX)
        GUTINDEX_file.close()
        print("Download of the GUTINDEX file successful")

        build_gutenberg_index()


def check_books_folder():
    """
    If existing books/ folder exists, the user is prompted to either delete it
    and make a new folder or keep it. If it doesn't exist, a books/ folder is
    made. The /books folder will store all of the books' files.
    """
    if os.path.exists("books/"):
        while True:
            yn = input("Delete the existing books/ folder? y/n --> ")
            if yn == "y" or yn == "Y":
                os.system("rm -rf books")
                os.system("mkdir books")
                break
            elif yn == "n" or yn == "N":
                break
            else:
                print("Invalid input; try again")
                continue
    else:
        os.system("mkdir books")


def handle_books(gutenberg_index, num_texts_plot):
    """
    This function will prompt the user to either download books from the hard-coded list or to type in the desired
    books by hand. The program will then acquire the books if they haven't already, or if they have, loading them into
    book objects in the library dictionary.
    :param gutenberg_index:
    :param num_texts_plot: either take input of one or two texts
    :return library: a dictionary of the book objects
    """
    library = {}
    while True:
        yn = input("Compare books from hardcoded list? If no, then you will type in your own. y/n --> ")
        if yn == "y" or yn == "Y":
            for book_name_author in book_list:
                print("Loading {}".format(book_name_author))
                library[book_name_author] = cl.Book(book_name_author, gutenberg_index)
                book = library[book_name_author]
                book.make_book(gutenberg_index)
            break
        elif yn == "n" or yn == "N":
            n = 0
            while True:
                if n == 0:
                    book_name_author = input(
                        "\nType in what book you want to download using this format: Book Title, by Author Name: --> ")
                elif n == 1 and num_texts_plot == 2:
                    book_name_author = input(
                        "\nType in the second book you want to using this format: Book Title, by Author Name: --> ")
                else:
                    break

                try:
                    library[book_name_author] = cl.Book(book_name_author, gutenberg_index)
                    book = library[book_name_author]
                    book.make_book(gutenberg_index)
                    print("Successfully acquired {}".format(book_name_author))
                    n += 1
                    continue
                except cl.InvalidBookError:
                    print("Try re-entering the book name and author (be sure to use the author's full name)...")
                    continue
            break
        else:
            print("Invalid input; try again")
            continue
    return library


def random_markov_chain(book, len_chain=30):
    """
    Generates a markov chain using the random method described in the Book class.
    :param book: a book object
    :param len_chain: length of the desired markov chain
    :return: a list of words that is the markov chain
    """
    output_list = [book.words[random.randint(0, book.length - 1)]]

    # Generate an output of a 30 word length
    for i in range(len_chain - 1):
        possible_words = book.random_markov[output_list[-1]]
        output_list.append(possible_words[random.randint(0, len(possible_words) - 1)])
    return output_list


def assisted_markov_chain(book, len_chain=30):
    """
    Generates a markov chain using the assisted method described in the Book class.
    :param book: book object
    :param len_chain: length of the desired chain
    :return: a list of words that is the markov chain
    """
    output_list = [book.words[random.randint(0, book.length - 1)]]

    # Generate an output of a 30 word length
    for i in range(len_chain - 1):
        possible_words = book.assisted_markov[output_list[-1]]
        output_list.append(possible_words[random.randint(0, len(possible_words) - 1)])
    return output_list


def control_markov_chain(book, len_chain=30):
    """
    Generates a markov chain using the controlled method described in the Book class.
    Takes a book object as a parameter and the length of the desired chain and
    returns a list of words that is the markov chain.
    :param book:
    :param len_chain:
    :return: markov chain list
    """
    rand_int = random.randint(0, book.length - len_chain)
    return book.words[rand_int:rand_int + len_chain]


def atf_helper(text):
    """
    Creates a histogram and dictionary of augmented term frequencies for a given text.

    :param text: a list of words
    :return: the histogram for raw word count and augmented term frequency

    >>> text = ['word', 'word', 'hello']; hist, atf = atf_helper(text); [atf[word] for word in text]
    [1.0, 1.0, 0.75]
    """
    # make histogram for the text
    hist = {}
    for word in text:
        hist[word] = hist.get(word, 0) + 1
        # calculate the most commonly occuring word in the text
    max_word_ct = 0
    for word in hist:
        if hist[word] > max_word_ct:
            max_word_ct = hist[word]

    # calculate the (augmented) term frequency for each word in text
    atf = {}
    for word in hist:
        atf[word] = hist[word] / (2 * max_word_ct) + 0.5

    return hist, atf


def inv_doc_freq(word, hist_list):
    """
    :param word - a string
    :param hist_list - the list of histograms for all texts in consideration for the similarity matrix
    :return: the inverse document frequency based on the weighting: log(1+N/(n)).

    >>> inv_doc_freq('test', [{'this':1,'is':1,'a':1,'test':1},{'this':1,'should':1,'work':1}])
    0.3010299956639812

    >>> inv_doc_freq('this', [{'this':1,'is':1,'a':1,'test':1},{'this':1,'should':1,'work':1}])
    0.0
    """
    n = 0
    for hist in hist_list:
        n += hist.get(word, 0)
    return math.log10(1 + len(hist_list) / n)


def cosine_sim(vec1, vec2):
    """
    Returns the centered cosine similarity between two vectors. The cosine similarity is calculated as the dot product
    of two vectors divided by the product of their magnitudes.

    >>> cosine_sim([1,2], [1,2])
    0.9999999999999998
    >>> cosine_sim([0,1], [1,0])
    0.0
    """

    vec_len = len(vec1)
    dot = sum(vec1[i] * vec2[i] for i in range(vec_len))
    mag_vec1 = math.sqrt(sum(vec1[i] ** 2 for i in range(vec_len)))
    mag_vec2 = math.sqrt(sum(vec2[i] ** 2 for i in range(vec_len)))
    return dot / (mag_vec1 * mag_vec2)


def make_similarity_matrix(texts):
    """
    Takes as an input a list of lists, where the inner lists are lists of words
    in a text. Returns the similarity matrix of the texts, using the cosine
    similarity of the vectors, where the vectors are populated with the augmented
    term frequency of each word. The augmented term frequency uses the weighting:
    tf = 0.5 + frequency_of_word_in_document/(2*frequency_of_most_common_word)

    Note: have to account for print statements in the output for doctests
    >>> make_similarity_matrix([['this','is','a','test'],['this','is','a','test']])
    array([[1., 1.],0 %0 %
           [1., 1.]])

    >>> make_similarity_matrix([['there','should','be'],['no','similarity','between','these']])
    array([[1., 0.],0 %0 %
           [0., 1.]])

    There are inconsistencies with expectations of indenting which cause the
    doctests to fail, but otherwise they work.
    """

    num_texts = len(texts)

    # These lists will be populated with dictionaries of word histograms and augmented term frequencies. To access the
    # desired dictionary of a text, simply access atf_list or hist_list with the same index of the text in the list
    # texts.
    atf_list = []
    hist_list = []
    for text in texts:
        hist, atf = atf_helper(text)
        hist_list.append(hist)
        atf_list.append(atf)

    # Create a vocabulary for the combined texts
    v = []
    for text in texts:
        for word in text:
            v.append(word)
    vocabulary = set(v)

    matrix = np.ndarray((num_texts, num_texts))
    # Calculate the cosine distance between each pair of texts using the tf-idf
    for i in range(num_texts):
        for j in range(num_texts):
            # Track computation progress:
            try:
                n += 1
            except:
                n = 0
            print("Analyzing...", round(100 * n / num_texts ** 2, 2), "%", end="\r")

            # Populate vectors with their respective tfidf values
            texti_vec = []
            textj_vec = []
            for word in vocabulary:
                texti_vec.append(atf_list[i].get(word, 0) * inv_doc_freq(word, hist_list))
            for word in vocabulary:
                textj_vec.append(atf_list[j].get(word, 0) * inv_doc_freq(word, hist_list))

            # Populate the similarity matrix with the cosine similarity of each vector
            matrix[i][j] = cosine_sim(texti_vec, textj_vec)
    return matrix


def display_similarity_matrix(matrix, num_sets_markov_chains, num_texts_plot):
    """
    :param matrix: similarity matrix
    :param num_sets_markov_chains: number of markov chains that will be compared
    :param num_texts: number of texts being compared; either a 1 or a 2
    :return: none
    Displays the scatterplot of text similarities
    """
    # dissimilarity is 1 minus similarity
    dissimilarities = 1 - matrix

    # compute the embedding
    coord = MDS(dissimilarity='precomputed').fit_transform(dissimilarities)

    # Creates the arrays of colors to distinguish between the different points in the scatter plot
    colors = np.ndarray(0)
    if num_texts_plot == 1:
        for i in range(3):
            colors = np.concatenate((colors, (i/5) * np.ones(int(num_sets_markov_chains/3))))
        labels = ["Control Markov", "Random Markov", "Assisted Markov"]
    else:
        for i in range(3):
            colors = np.concatenate((colors, (i/5) * np.ones(int(num_sets_markov_chains/3))))
        for i in range(3):
            colors = np.concatenate((colors, 1+(i/5) * np.ones(int(num_sets_markov_chains/3))))

    plt.scatter(coord[:, 0], coord[:, 1], c=colors, label=labels)
    plt.title()

    # Label the points
    for i in range(coord.shape[0]):
        plt.annotate(str(i), (coord[i, :]))

    plt.show()


if __name__ == "__main__":
    print("Not all doctests run successfully, but that doesn't necessarily mean that their respective functions aren't "
          "working correctly; please refer to the function's documentation for more information.")
    cont = input("Press enter to continue")

    doctest.run_docstring_examples(cosine_sim, globals(), verbose=False)
    doctest.run_docstring_examples(inv_doc_freq, globals(), verbose=False)
    doctest.run_docstring_examples(make_similarity_matrix, globals(), verbose=False)
    doctest.run_docstring_examples(atf_helper, globals(), verbose=False)
    doctest.run_docstring_examples(inv_doc_freq, globals(), verbose=False)
    doctest.run_docstring_examples(list_to_string(), globals(), verbose=False)
