################################################################################

"""
This software will take a list of books (book_list) and automatically find and
download the text files for the books. It will also prompt the user if the
data training sets
"""

################################################################################


from selenium import webdriver
import requests
from text_processing import build_dataset
import os
import time
from classes import Book
import pickle

PATH_TO_GECKO_DRIVER = "/home/duncan/softdes/mp3"

################################################################################

book_list = [
('Frankenstein; Or, The Modern Prometheus', 'Mary Wollstonecraft Shelley'),
('A Tale of Two Cities', 'Charles Dickens'),
('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle'),
('Adventures of Huckleberry Finn', 'Mark Twain'),
('The Yellow Wallpaper', 'Charlotte Perkins Gilman'),
('Metamorphosis', 'Franz Kafka')
]

successful_downloads = []

# book_list = [('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle')]

################################################################################

def collect_book(link_to_book, book_name, author):
    book_download = False
    print('Trying to download book with `requests`...')
    try:
        book_text = requests.get(link_to_book).text
        book_download = True
    except:
        print('Trying to download book with `urllib.request`...')
        try:
            time.sleep(1)
            book_text = urllib.request.urlretrieve(link_to_book)
            book_download = True
        except:
            print('Neither downlaod method was successful.')

    # remove project gutenberg header in document, which is concluded by:
    #
    # ***START OF PROJECT .... ***
    # book text...
    star_counter = 0
    for i in range(len(book_text)):
        if book_text[i:i+3] == "***":
            star_counter += 1
            if star_counter == 2:
                book_text = book_text[i+3:len(book_text)]
                break

def find_book(book_name, author_name):
    """
    Searches project gutenberg for book_name, and returns the url of the txt
    file of that book. If it can't find the file, it returns False.
    """
    flag = False
    search_page = "https://www.gutenberg.org/ebooks/search/?query={}".format(book_name+"___"+author_name)
    try:
        text = driver.get(search_page) # enter the search query
        time.sleep(sleep_time)
    except:
        print('Could not search for the book name')
        return False

    try:
        links = driver.find_elements_by_class_name("link")
        header_string = '{} by {}'.format(book_name, author_name)
        # Now we are on the results page of the search query where we will
        # test each link for a match with the book name
        print('Number of links to check for {}: {}'.format(book_name, len(links)))

        for i in range(len(links)):
            links = driver.find_elements_by_class_name("link")
            link = links[i]
            link.click() # enter each element of the results page
            time.sleep(sleep_time)
            url = driver.current_url
            while "gutenberg.org" not in url: # make sure we are in the right website
            # because some links lead to facebook or twitter
                driver.back()
                time.sleep(1)
            else:
                web_code = requests.get(url).text
                if header_string in web_code:
                    try:
                        links = driver.find_elements_by_class_name('link')
                        link = links[len(links)-2] # .txt file is always the second to last link
                        link.click()
                        if driver.current_url[len(driver.current_url)-3:] != 'txt': # making sure it's not an audio book
                            print('here')
                            driver.back()
                            if driver.current_url[len(driver.current_url)-3:] != 'txt':
                                driver.back()
                            continue
                        else:
                            print("Found site!")
                            return driver.current_url
                    except:
                        print('Something went awry...')
                        return False
                else:
                    print('trying new site')
                    driver.back()
                    continue
    except:
        return False
        print('No matches found for the book {}'.format(book_name))

def book_looper():
    for book in book_list:
        book_name = book[0]
        author_name = book[1]
        link_to_book = find_book(book_name, author_name)
        if link_to_book != False:
            if collect_book(link_to_book, book_name, author_name):
                print("{} all ready to go!".format(book_name))
                if os.path.exists("successful_downloads.txt"):
                    file = open("successful_downloads.txt", "rb+")
                    file_text = file.read()
                    file_list = pickle.loads(file_text)
                    file_list.append("{}___{}.txt".format(book_name, author_name))
                    file_text = pickle.dumps(file_list)
                    file.seek(0,0)
                    file.write(file_text)
                    file.close()
                else:
                    file = open("successful_downloads.txt", "wb")
                    file_list = ["{}___{}.txt".format(book_name, author_name)]
                    file_text = pickle.dumps(file_list)
                    print(file_text)
                    file.write(file_text)
                    file.close()
            else:
                "Oops, something happened trying to download {}, moving on to the next book"
                continue
        else:
            "Unable to get {} link, moving on to the next book.".format(book)
    print("Finished downloading!")

if __name__=="__main__":
    ############################################### Configuring program

    yn = input("Download books from list? y/n --> ")
    if yn == "y" or yn == "Y":

        os.system("export PATH=$PATH:{}".format(PATH_TO_GECKO_DRIVER))

        sleep_time_bool = input("Would you like the code to browse the web slower to avoid being labeled as a spammer? y/n --> ")
        if sleep_time_bool == 'y' or sleep_time_bool == 'Y':
            sleep_time = input("How long (in seconds) would you like the program to wait between web pages? float--> ")
            sleep_time = float(sleep_time)
            time.sleep(1)
        else:
            sleep_time = 0.0
            print("Loading web driver...")
            time.sleep(1)

        print("Loading web driver...")
        driver = webdriver.Firefox()
        book_looper()

        print("Moving books to /books folder")
        os.system("mkdir books; mv *___* books") # put books in a separate folder

    yn = input("Delete /books if existing? Problems may arise if there will be duplicate files. y/n --> ")
    if yn == "y" or yn == "Y":
        yn_2 = input("Are you sure you want to delete the folder /books? y/n --> ")
        if yn_2 == "y" or yn == "Y":
            os.system("rm -rf books")
        else:
            print("Okay, will not delete /books")
    else:
        print("Okay, will not delete /books")

    ################################### Text processing for the downloaded books

    # Generate a book object for each downloaded book
    dict_book_objs = {}
    try:
        successful_downloads_file = open("successful_downloads.txt", 'rb')
        successful_downloads_text = successful_downloads_file.read()
        successful_downloads = pickle.loads(successful_downloads_text)
    except:
        print("There is no record of successfully download bookds.")
        exit()

    for book_file_name in successful_downloads:
        print(book_file_name)
        dict_book_objs[book_file_name] = Book("books/{}".format(book_file_name))

    for book_file_name in dict_book_objs:
        book = dict_book_objs[book_file_name]
        book.tokenize_book()
        book.make_hist()

    test = open("books/The Yellow Wallpaper___Charlotte Perkins Gilman___tokenized.txt", 'rb')
    test_text = test.read()
    test_data = pickle.loads(test_text)
    print(len(test_data))
    test.close()
