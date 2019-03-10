import random
import requests
import os
import classes as cl
import pickle
import math
import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

book_list = [
('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
('A Tale of Two Cities, by Charles Dickens'),
]

def build_gutenberg_index():
    """
    Generates a python-readable index of project gutenberg's master index -
    GUTINDEX.txt - called gutenberg_index.txt. Returns a dictionary of the
    index. If gutenberg_index.txt exists, it is deleted and redownloaded.
    """
    if os.path.exists("gutenberg_index.txt"):
        print("Deleting old gutenberg_index.txt file.")
        os.system("rm -rf gutenberg_index.txt")

    gut_index_file = open("GUTINDEX.txt", 'r+')
    gut_index_text = gut_index_file.read()
    gut_index_file.close()

    skip_line_if = [" ", "~", "TITLE"]
    end_title_if = ["  ", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
    gutenberg_index = {}
    gut_lines = gut_index_text.split("\n")

    print("Generating gutenberg_index dictionary and writing as gutenberg_index.txt")
    for line in gut_lines[260:]:
        if line == "<==End of GUTINDEX.ALL==>":
            break
        else:
            if len(line) != 0:
                if line[0] not in skip_line_if or line[0:5] not in skip_line_if:
                    for i in range(len(line)-1):
                        if line[i:i+2] in end_title_if:
                            book_name_author = line[0:i]
                            for j in range(0, len(line)):
                                if line[len(line)-j-1] == " ":
                                    book_number = line[len(line)-j:len(line)]
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
            yn = input("Redownload the index of project gutenberg - GUTINDEX.txt - and delete the old one? New books may have been added. y/n --> ")
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
    If existing books/ folder exists, the user is prompted to either delte it
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
            elif yn == "n" or y == "N":
                break
            else:
                print("Invalid input; try again")
                continue
    else:
        os.system("mkdir books")

def handle_books(gutenberg_index):
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
                if n == 2:
                    break
                elif n == 0:
                    book_name_author = input("\nType in what book you want to download using this format: Book Title, by Author Name: --> ")
                else:
                    book_name_author = input("\nType in the second book you want to download using this format: Book Title, by Author Name: --> ")

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
    output_list = [book.words[random.randint(0, book.length-1)]]

    # Generate an output of a 30 word length
    for i in range(len_chain-1):
        possible_words = book.random_markov[output_list[-1]]
        output_list.append(possible_words[random.randint(0,len(possible_words)-1)])
    return output_list

def assisted_markov_chain(book, len_chain=30):
    output_list = [book.words[random.randint(0, book.length-1)]]

    # Generate an output of a 30 word length
    for i in range(len_chain-1):
        possible_words = book.assisted_markov[output_list[-1]]
        output_list.append(possible_words[random.randint(0,len(possible_words)-1)])
    return output_list

def control_markov_chain(book, len_chain=30):
    rand_int = random.randint(0, book.length-len_chain)
    return book.words[rand_int:rand_int+len_chain]

def inv_doc_freq(word, text1, text2):
    num_docs_contain_word = 0
    if word in text1:
        num_docs_contain_word += 1
    if word in text2:
        num_docs_contain_word += 1
    return math.log(2/(num_docs_contain_word+1))

def cosine_sim(vec1, vec2):
    """
    Returns the centered cosine similarity between two vectors
    """
    vec_len = len(vec1)

    dot = sum(vec1[i]*vec2[i] for i in range(vec_len))
    mag_vec1 = math.sqrt(sum(vec1[i]**2 for i in range(vec_len)))
    mag_vec2 = math.sqrt(sum(vec2[i]**2 for i in range(vec_len)))
    return dot/(mag_vec1*mag_vec2)

def make_similarity_matrix(texts):
    """
    Takes as an input a list of lists, where the inner lists are lists of words
    in a text. Returns the similarity matrix of the texts.


    """
    num_texts = len(texts)
    print(num_texts)
    hist_list = []
    atf_list = []
    tfidf = {}

    for text in texts:
        # make histogram for the text
        hist = {}
        for word in text:

            hist[word] = hist.get(word,0) + 1
        hist_list.append(hist)
        # calculate the most commonly occuring word in the text
        max_word_ct = 0
        for word in hist:
            if hist[word] > max_word_ct:
                max_word_ct =  hist[word]

        atf = {} # calculate the augmented term frequency for each word in text
        for word in hist:
            atf[word] = hist[word]/(2*max_word_ct)+0.5
        atf_list.append(atf)

    matrix = np.ndarray((num_texts,num_texts))
    # Calculate the cosine distance between each pair of texts using the tf-idf
    for i in range(num_texts):
        for j in range(num_texts):
            # Create a vocabulary for the combined texts; initialize tfidf
            # values to 0
            s = set(texts[i]+texts[j])
            texti_vec = []
            textj_vec = []
            for word in s:
                texti_vec.append(atf_list[i].get(word,0)*inv_doc_freq(word, texts[i], texts[j]))
                textj_vec.append(atf_list[j].get(word,0)*inv_doc_freq(word, texts[i], texts[j]))
            matrix[i][j] = cosine_sim(texti_vec, textj_vec)
    return matrix

def display_similarity_matrix(matrix):
    # dissimilarity is 1 minus similarity
    dissimilarities = 1 - matrix

    # compute the embedding
    coord = MDS(dissimilarity='precomputed').fit_transform(dissimilarities)

    plt.scatter(coord[:,0], coord[:,1])

    # Label the points
    for i in range(coord.shape[0]):
        plt.annotate(str(i), (coord[i,:]))

    plt.show()


if __name__=="__main__":
    """
    Test functionality of the functions in this document
    """
    # check_GUTINDEX()
    # check_books_folder()
    #
    # # Load the gutenberg_index dictionary
    # gutenberg_index_file = open("gutenberg_index.txt", "rb")
    # gutenberg_index_text = gutenberg_index_file.read()
    # gutenberg_index = pickle.loads(gutenberg_index_text)
    # gutenberg_index_file.close()
    #
    # library = handle_books(gutenberg_index)

    print(cosine_sim([1,2],[1,2]))
