import datetime
import requests

from queue import Queue
from threading import Thread
from constants import *

class DownloadWorker(Thread):

    def __init__(self, queue, subreddit, worker_num):
        Thread.__init__(self)
        self.queue = queue
        self.subreddit = subreddit
        self.worker_num = worker_num
        self.data = []

    def run(self):
        while True:
            day = self.queue.get()
            self.get_data_for_day(day)
            self.queue.task_done()

    def get_data_for_day(self, day):

        print('\t[worker_num-%d] Getting data for [before=%sd] [after=%sd]' % (self.worker_num, str(day), str(day+1)))

        url = URL_TEMPLATE % (self.subreddit, str(day), str(day+1))

        r = requests.get(url)

        if r.status_code == 200:

            data_per_day = 0
            for submission in r.json()['data']:
                datum = {}
                for col_name in COLUMN_NAMES:
                    if col_name == COLUMN_NAMES[4]:
                        datum[COLUMN_NAMES[4]] = int(datetime.datetime.fromtimestamp(datum['created_utc']).strftime('%H'))
                    elif col_name == COLUMN_NAMES[5]:
                        datum[COLUMN_NAMES[5]] = datetime.datetime.fromtimestamp(datum['created_utc']).strftime('%a')
                    else:
                        datum[col_name] = submission[col_name]

                self.data.append(datum)
                data_per_day = data_per_day + 1
                print('\t[worker_num-%d] Obtained %s data points [before=%sd] [after=%sd]' % (self.worker_num, str(data_per_day), str(day), str(day+1)))
        else:
            print('\t[worker_num-%d] Status code was %s for request: [before=%sd] [after=%sd]' % (self.worker_num, r.status_code, str(day), str(day+1)))



    def get_all_data(self):
        return self.data
