from selenium import webdriver
import requests
from manual_text_mining import collect_book
import os

################################################################################
driver = webdriver.Firefox()

book_list = [
('Frankenstein; Or, The Modern Prometheus', 'Mary Wollstonecraft Shelley'),
('Pride and Prejudice', 'Jane Austin'),
('A Modest Proposal', 'Jonathan Swift'),
('Heart of Darkness','Joseph Conrad'),
('A Tale of Two Cities', 'Charles Dickens'),
('Moby Dick; Or, The Whale', 'Oscar Wilde'),
('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle'),
('Adventures of Huckleberry Finn', 'Mark Twain'),
('The Yellow Wallpaper', 'Charlotte Perkins Gilman'),
('Metamorphosis', 'Franz Kafka')
]
################################################################################

def find_book(book_name, author_name):
    """
    Searches project gutenberg for book_name, and returns the url of the txt
    file of that book. If it can't find the file, it returns False.
    """
    flag = False
    search_page = "https://www.gutenberg.org/ebooks/search/?query={}".format(book_name)
    try:
        driver.get(search_page)
    except:
        print('Could not search for the book name')
        return False

    try:
        links = driver.find_elements_by_class_name("link")
        header_string = '{} by {}'.format(book_name, author)
        print('Number of links to check for {}: {}'.format(book_name, len(links)))
        for i in range(len(links)): # book link is always preceded by 4 other links
            links = driver.find_elements_by_class_name("link")
            link = links[i]
            link.click()
            if "gutenberg.org" not in driver.current_url:
                driver.back()
                continue
            web_code = requests.get(driver.current_url).text
            if header_string in web_code:
                print('Found site!')
                break
            else:
                print('trying new site')
                driver.back()
                continue
    except:
        return False
        print('No matches found for the book {}'.format(book_name))

    try:
        links = driver.find_elements_by_class_name('link')
        link = links[len(links)-2] # .txt file is always the second to last link
        link.click()
        return driver.current_url
    except:
        print('Something went awry...')
        return False

def book_looper(book_list):
    for book in book_list:
        book_name = book[0]
        author = book[1]
        link_to_book = find_book(book_name, author)
        if link_to_book != False:
            if collect_book(link_to_book, book_name, author):
                "{} all ready to go!"
            else:
                "Oops, something happened trying to download {}, moving on to the next book"
                continue
        else:
            "Moving on to the next book."
    print("Finished downloading!")

# def file_rearranger():
#     if os.path.exists("/books"):
#         print('/books folder already exists.')
#         path_exists = True
#     else:
#         print('/books folder does not already exist')
#         path_exists = False
#     mkdir = input("Make new directory called books? If yes and one already exists, the existing one will be delted. y/n")
#     if mkdir == 'y' or mkdir == 'Y':
#         if path_exists:
#             os.system('rm -rf books; mkdir books')
#         else:
#             os.system('mkdir books')
#     else:
#         if not path_exists:
#             print('Because you did not make a directory, there is no directory called /books for the files to be moved to.')
#             return None
#
#     mv = input("Move files to the directory /books ? y/n")
#     if mv == 'y' or mv == 'Y':
#         for book in book_list:
#             file_name = book[0]+'___'+book[1]
#             for i in range(len(file_name)):
#                 file_name = file_name[0:i] + '\ ' + file_name[i:len(file_name)]
#             try:
#                 os.system('mv {} /books'.format(file_name))


if __name__=="__main__":
    # book_looper()
    file_rearranger()
