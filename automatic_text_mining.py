################################################################################

"""
This software will take a list of books (book_list) and automatically find and
download the text files for the books. It will also prompt the user if the
data training sets
"""

################################################################################

# from selenium import webdriver
import requests
from text_processing import build_dataset
# from manual_text_mining import collect_book
import os
import time
from classes import Book
import pickle

# PATH_TO_GECKO_DRIVER = "/home/duncan/softdes/mp3"

################################################################################

book_list = [
('Frankenstein, by Mary Wollstonecraft (Godwin) Shelley'),
('A Tale of Two Cities, by Charles Dickens'),
('The Adventures of Sherlock Holmes, by Arthur Conan Doyle'),
('Adventures of Huckleberry Finn, by Mark Twain'),
('The Yellow Wallpaper, by Charlotte Perkins Gilman'),
('Metamorphosis, by Franz Kafka')
]

successful_downloads = []

# book_list = [('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle')]

def build_gutenberg_index():
    gut_index_file = open("GUTINDEX.txt", 'r+')
    gut_index_text = gut_index_file.read()
    gut_index_file.close()

    skip_line_if = [" ", "~", "TITLE"]
    end_title_if = ["  ", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
    gutenberg_index = {}
    gut_lines = gut_index_text.split("\n")

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
    return gutenberg_index

if __name__=="__main__":
    if os.path.exists("gutenberg_index.txt"):
        print("\nProj. Gutenberg index already exists.")

        yn = input("Redownload the gutenberg index file? New books may have been added.")
        while True:
            if yn == "y" or yn == "Y":
                gutenberg_index = build_gutenberg_index()
                break
            elif yn == "n" or yn == "N":
                gutenberg_index_binary = open("gutenberg_index.txt", 'rb')
                gutenberg_index_text = gutenberg_index_binary.read()
                gutenberg_index = pickle.loads(gutenberg_index_text)
                gutenberg_index_binary.close()
                break
            else:
                print("Invalid input; try again")
    else:
        print("Generating Python-readable index for proj. Gutenberg books...")
        gutenberg_index = build_gutenberg_index()
        print("Index built.\n")

    if os.path.exists("books/"):
        yn = input("Delete books/ folder? Problems may arise if there will be duplicate files. y/n --> ")
        # TODO: handle invalid characters
        if yn == "y" or yn == "Y":
            yn_2 = input("Are you sure you want to delete the folder /books? y/n --> ")
            if yn_2 == "y" or yn == "Y":
                os.system("rm -rf books")
                os.system("mkdir books")
            else:
                print("Okay, will not delete /books")
        else:
            print("Okay, will not delete /books")
    else:
        os.system("mkdir books")

    dict_books = {}
    yn = input("Download books from list? y/n --> ")
    if yn == "y" or yn == "Y":
        for book_name_author in book_list:
            print("Downloading: {}".format(book_name_author))
            dict_books[book_name_author] = Book(book_name_author)
            book = dict_books[book_name_author]
            book.make_book(gutenberg_index)
