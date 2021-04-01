from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    # """ 
    file = open(filename)
    text = file.read()
    file.close() 
    soup = BeautifulSoup(text, 'html.parser')
    
    titleAuthorPairs = []
    allBooks = soup.find_all("tr")
    for book in allBooks: 

        title = book.find_all("a", class_="bookTitle")[0]
        title = title.findChildren("span" , recursive=False)[0].text

        author = book.find_all("a", class_="authorName")[0]
        author = author.findChildren("span", recursive=False)[0].text

        titleAuthorPairs.append((title, author))

    return titleAuthorPairs 

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")

    allResults = soup.find_all("a", class_="bookTitle", href=True)
    search_results = []
    count = 0 
    for result in allResults: 
        if count == 10: 
            break
        href = result['href']
        if "/book/show/" in href: 
            search_results.append("https://www.goodreads.com" + href)
            count += 1
    
    return search_results




def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    
    text = requests.get(book_url).text
    soup = BeautifulSoup(text, "html.parser")

    bookTitle = soup.find(id="bookTitle").text.strip()
    authorName = soup.find("a", class_="authorName").findChildren("span" , recursive=False)[0].text.strip()
    numPages = soup.find("span", itemprop="numberOfPages").text.split()[0]

    return (bookTitle, authorName, int(numPages))



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    file = open(filepath)
    text = file.read()
    file.close() 
    soup = BeautifulSoup(text, 'html.parser')

    bestBookSummaries = [] 
    allBooks = soup.find_all("div", class_="category clearFix")
    for book in allBooks: 
        category = book.find("h4", class_="category__copy").text.strip() 
        title = book.find("img", class_="category__winnerImage")["alt"].strip()
        href = book.findChildren("a", recursive=False)[0]['href']
        bestBookSummaries.append((category, title, href))
    return bestBookSummaries

        

def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    outputFile = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
    f = open(outputFile, 'w')
    f.write("Book title,Author Name")
    for title in data:
        f.write('\n')
        line = ""
        f.write("{},{}".format(title[0], title[1]))
    f.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    file = open(filepath)
    text = file.read()
    file.close() 
    soup = BeautifulSoup(text, 'html.parser')

    description = soup.findAll(id="description")[0].findAll('span')[1]
    allText = description.findAll(text=True)
    text = ''
    for i in allText:
        text = text + str(i.string)
        # [A-Z][a-z][a-z]+ [A-Z][a-z.\d]+( [A-Z][a-z.\d]+)*
        # [A-Z][a-z][a-z]+ [A-Z][a-z.\d]+\s*([A-Z][a-z.\d]+)*
    pattern = r"[A-Z][a-z][a-z]+ [A-Z][a-z.\d]+(?: [A-Z][a-z.\d]+)*"
    namedEntities = re.findall(pattern, text)

    return namedEntities
    


class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    def setUp(self):
        self.search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(titles), list)
        # check that each item in the list is a tuple
        for pair in titles: 
            self.assertEqual(type(pair), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1], ("Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"))
        
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for url in self.search_urls: 
            self.assertEqual(type(url), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in self.search_urls: 
            self.assertTrue(url.startswith("https://www.goodreads.com/book/show/"))
        
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        first = True
        count = 0 
        for url in self.search_urls:
            count += 1
            print(count, "finished")

            summary = get_book_summary(url)    
            # check that each item in the list is a tuple
            self.assertEqual(type(summary), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(summary), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]), str)
            self.assertEqual(type(summary[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(summary[2]), int)
            # check that the first book in the search has 337 pages
            if first == True: 
                self.assertEqual(summary[2], 337)
                first = False
            summaries.append(summary)
            
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books_summarized = summarize_best_books("best_books_2020.htm") 
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books_summarized), 20)

        for book in best_books_summarized:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(book), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(book), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        first_tuple = ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        self.assertEqual(best_books_summarized[0], first_tuple)
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        last_tuple = ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020')
        self.assertEqual(best_books_summarized[-1], last_tuple)

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        data = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(data, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open(os.path.dirname(os.path.abspath(__file__)) + '/test.csv', 'r')
        lines = f.readlines() 
        f.close()

    #     # check that there are 21 lines in the csv
        self.assertEqual(len(lines), 21)
    #     # check that the header row is correct
        self.assertEqual(lines[0].rstrip(), "Book title,Author Name")
    #     # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(lines[1].rstrip(), 'Harry Potter and the Deathly Hallows (Harry Potter, #7),J.K. Rowling')
    #     # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(lines[-1].rstrip(), 'Harry Potter: The Prequel (Harry Potter, #0.5),J.K. Rowling')


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



