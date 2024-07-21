from ContentProvider import ContentProvider
from threading import Condition, Thread, RLock, Lock
from collections import deque
import time 

class Crawler():
  def __init__(self, seedUrls, max_workers, filename):
    self.content_provider = ContentProvider()
    self.n_workers_condition = Condition()
    self.max_workers = max_workers
    self.n_workers = 0
    self.seen = set()
    self.condition = Condition()
    self.q = deque()
    self.q_lock = RLock()
    self.crawled_lock = Lock()
    self.crawled = 0
    self.crawling = 0
    self.add_to_queue(seedUrls)
    self.filename = filename
    self.file_lock = Lock()
    self.file = open(self.filename, 'w', encoding="utf-8")
    self.exception_count = 0

  def __del__(self):
    if self.file and not self.file.closed:
      self.file.close()

  def add_to_queue(self, links):
    with self.q_lock:
      links = [l for l in links if l not in self.seen]
      self.q.extend(links)
      self.seen.update(links)
      # if self.seen is more than max_urls exit

  def crawl_next_page(self, max_urls_to_crawl):
    # think about having a batch here instead of a single thread.
    next_url = ""
    with self.condition:
      self.condition.wait_for(lambda: (len(self.q) > 0)  or (len(self.q) == 0 and self.crawling == 0))

      with self.q_lock:
        if len(self.q) == 0 and self.crawling == 0:
          return
        next_url = self.q.popleft()
      # add comment here
      self.condition.notify_all() # not necessary but good practice
  
      with self.crawled_lock:
        if self.crawled + self.crawling == max_urls_to_crawl:
          return
        self.crawling += 1

    try:
      with self.file_lock:
        self.file.write(f'crawling "{next_url}"...')
      page = self.content_provider.fetch_webpage_content(next_url)
      with self.file_lock:
        self.file.write(f'{'-' * 100}\n"{page.title}" was crawled succesfully\ncontent:\n{page.content_peek}\n{'-' * 100}')
      with self.crawled_lock:
        self.crawling -= 1
        self.crawled += 1
      with self.condition:
        self.add_to_queue(page.links)
        self.condition.notify_all()
    except Exception as e:
      print(f'error: {e}')
      with self.crawled_lock:
        self.crawling -= 1

    with self.n_workers_condition:
      self.n_workers -= 1
      self.n_workers_condition.notify_all()

  def crawl_all(self, max_urls_to_crawl):
    while True:
      with self.crawled_lock:
        if self.crawled == max_urls_to_crawl:
          return
      # print("crawling")
      self.crawl_next_page(max_urls_to_crawl)

  def crawl_spin_thread_every_crawl(self, max_urls_to_crawl):
    # can we create only few threads at the beginnig and make them wait for the queue
    while self.exception_count < 10:
      with self.q_lock:
        with self.crawled_lock:
          if len(self.q) == 0 and self.crawling == 0:
            print("No more links to crawl")
            break
      with self.crawled_lock:
        if self.crawled == max_urls_to_crawl:
          break
      with self.n_workers_condition:
        self.n_workers_condition.wait_for(lambda: self.n_workers < self.max_workers)
        self.n_workers += 1
        t = Thread(target = self.crawl_next_page, args = (max_urls_to_crawl,))
        t.start()
        self.n_workers_condition.notify_all()

  def crawl_spin_workers_ahead(self, max_urls_to_crawl):
    # can we create only few threads at the beginnig and make them wait for the queue
    threads = [Thread(target = self.crawl_all, args = (max_urls_to_crawl,)) for _ in range(self.max_workers)]
    for t in threads:
      t.start()
    for t in threads:
      t.join()

  def sequential_crawl(self, max_urls_to_crawl):
    while self.crawled < max_urls_to_crawl:
      self.crawl_next_page(max_urls_to_crawl)


url = 'https://en.wikipedia.org/wiki/Algorithm'

t1 = time.time()
crawler = Crawler([url], 10, "crawler1.txt")
crawler.crawl_spin_thread_every_crawl(50)
dur1 = time.time() - t1
print(f"DONE crawl_spin_thread_every_crawl with 10 threads in {dur1}")

t4 = time.time()
crawler4 = Crawler([url], 10, "crawler4.txt")
crawler4.crawl_spin_workers_ahead(50)
dur4 = time.time() - t4
print(f"DONE crawl_spin_workers_ahead in {dur4}")

# t2 = time.time()
# crawler2 = Crawler([url], 1, "crawler2.txt")
# crawler2.crawl_spin_thread_every_crawl(20)
# dur2 = time.time() - t2
# print(f"DONE crawl_spin_thread_every_crawl with 1 thread in {dur2}")

# t3 = time.time()
# crawler3 = Crawler([url], 1, "crawler3.txt")
# crawler3.sequential_crawl(20)
# dur3 = time.time() - t3
# print(f"DONE sequential_crawl in {dur3}")
