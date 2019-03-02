# Code to grab text from the interwebs

import requests
import os
import sys

def collect_book(link_to_book, book_name, author):
    try:
        book_text = requests.get(link_to_book).text
        file_name = book_name + "___" + author + '.txt'
        if os.path.exists(file_name):
            counter_file = open(file_name, 'rb+')
            counter_txt = counter_file.read()
            counter_file.seek(0, 0) # allows the old data to be written over
            counter_file.write(book_text) # write the string data containing the num
            counter_file.close()
            print('Existing book file overwritten.')
        else: ### this part works now!
            counter_file = open(file_name, 'wb')
            counter_file.write(book_text)
            counter_file.close()
        return True
        print('Successfully acquired book and wrote to file.')
    except:
        print('Not able to acquire and write book to file; may have exceeded request limit for project guttenberg')

if __name__=="__main__":
    welcome_text = "Welcome to the book gatherer! Type in the link to the book, the book's name, and the author to download and save the book. To exit the program, press Ctrl+C. \n \n"
    n = 0
    while True:
        print('Collecting book number {}'.format(n))
        link_to_book = input("What is the link to the book?")
        book_name = input("What is the book's name?")
        author = input("Who is the book's author?")
        collect_book(link_to_book, book_name, author)
