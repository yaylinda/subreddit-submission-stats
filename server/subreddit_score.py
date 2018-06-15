import csv
import sys
import statistics
import plotly
import plotly.graph_objs as go
import time
from download_worker import DownloadWorker
from queue import Queue

from constants import *


"""
"""
def generate_data(subreddit, days=10):

    print('[use_pushshift] Obtaining submissions from [/r/%s]' % subreddit)

    start = time.time()

    workers = []

    queue = Queue()
    
    for x in range(16):
       worker = DownloadWorker(queue, subreddit, x)
       worker.daemon = True
       worker.start()
       workers.append(worker)

    for i in range(0, int(days)):
        queue.put(i)

    queue.join()

    data = []
    for w in workers:
        for worker_data in w.get_all_data():
            data.append(worker_data)

    print('Took %d seconds.' % (time.time() - start))
    return data


"""
"""
def transform_data(subreddit, data, column):

    print('Aggregating data for [subreddit=%s] [column=%s]' % (subreddit, column))

    transformed = {}
    for weekday in WEEKDAYS:
        transformed[weekday] = {}
        for hour in HOURS:
            transformed[weekday][hour] = []

    for datum in data:
        weekday = datum[COLUMN_NAMES[5]]
        hour = int(datum[COLUMN_NAMES[4]])
        value = datum[column]
        transformed[weekday][hour].append(value)

    means = []
    for weekday in WEEKDAYS:
        means_for_day = []

        for hour in HOURS:
            values = transformed[weekday][hour]
            stats = calculate_stats(values)
            means_for_day.append(stats)

        means.append(means_for_day)

    # print(means)

    return means

"""
"""
def calculate_stats(values_list):

    if len(values_list) == 0:
        return 0

    return statistics.mean(values_list)

"""
"""
def write_data_to_csv(subreddit, data):
    filename = 'data/' + subreddit + '.csv'
    print('Writing data to [%s]' % filename)

    csv_file = open(filename, 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(COLUMN_NAMES)
    
    for datum in data:
        csv_writer.writerow([
            datum[COLUMN_NAMES[0]], 
            datum[COLUMN_NAMES[1]], 
            datum[COLUMN_NAMES[2]], 
            datum[COLUMN_NAMES[3]],
            datum[COLUMN_NAMES[4]],
            datum[COLUMN_NAMES[5]],
        ])

    csv_file.close()
    print('Done!')

"""
"""
def plot_data(data_to_plot, subreddit, column, stat):

    print('Plotting data for [subreddit=%s] [column=%s] [stat=%s]' % (subreddit, column, stat))

    title = '%s Submission %s for /r/%s' % (stat, column, subreddit)
    html_filename = 'plots/%s_%s_%s.html' % (subreddit, column, stat)
    image_filename = 'plots/%s_%s_%s' % (subreddit, column, stat)

    data_to_plot.reverse()
    WEEKDAYS.reverse()

    plotly.offline.plot(
        {
            "data" : [go.Heatmap(
                z = data_to_plot,
                x = [str(h) for h in HOURS],
                y = WEEKDAYS,
                colorscale = 'Viridis')],
            "layout" : go.Layout(
                title = title,
                xaxis = dict(title='Hour of Submission', ticks=' ', nticks=24),
                yaxis = dict(title='Day of Week', ticks=' '))
        },
        image_filename=image_filename,
        image='png',
        filename=html_filename)

"""
"""
if __name__ == '__main__':

    # Generate data from Reddit
    subreddit = sys.argv[1]
    if len(sys.argv) > 2:
        days = sys.argv[2]
    else:
        days = 10
    data = generate_data(subreddit, days)

    # print(data)

    # Write data to CSV
    # write_data_to_csv(subreddit, data)

    # Get data for plotting
    # score_means = transform_data(subreddit, data, COLUMN_NAMES[3])
    # num_comments_means = transform_data(subreddit, data, COLUMN_NAMES[1])

    # Plot data
    # plot_data(score_means, subreddit, 'Score', 'Mean')
    # plot_data(num_comments_means, subreddit, 'Num Comments', 'Mean')
