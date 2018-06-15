from queue import Queue
from threading import Thread

class DownloadWorker(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
       while True:
           directory, link = self.queue.get()
           download_link(directory, link)
           self.queue.task_done()