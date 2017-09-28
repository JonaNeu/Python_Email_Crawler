import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

from openpyxl import load_workbook

excel_sheet = load_workbook('data.xlsx')
excel_sheet = excel_sheet.get_sheet_by_name('Tabelle1')


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


# TODO restrict the number of websites that gets crawled to a certain number
# seiten wie facebook, linkedin restricten

PROJECT_NAME = ''
HOMEPAGE = ''

for i in range(4, 310):

    homepage = excel_sheet['C{}'.format(i)].value

    # check if url starts with http or https
    if not homepage.startswith('http'):
        HOMEPAGE = "http://" + homepage
    else:
        HOMEPAGE = homepage
    print("\n\n\n" + HOMEPAGE)

    DOMAIN_NAME = get_domain_name(HOMEPAGE)

    PROJECT_NAME = DOMAIN_NAME
    print(PROJECT_NAME + "\n\n\n")


    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    EMAIL_FILE = 'emails.csv'
    NUMBER_OF_THREADS = 8

    queue = Queue()
    Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

    create_workers()
    crawl()

