import csv
import sys
import datetime
import requests
import statistics
import plotly
import plotly.graph_objs as go

column_names = [
    'created_utc',
    'num_comments',
    'domain',
    'score',
    'hour',
    'weekday'
]

weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

hours = range(0, 24)

"""
Helper function to ensure input subreddit string is a valid subreddit.

    Input:
        - subreddit: subreddit string

    Returns:
        - boolean of whether or not subreddit is valid
"""
def validate_subreddit(subreddit):

    # TODO - validate subreddit

    return True


"""
"""
def generate_data(subreddit, days=10):

    print('[use_pushshift] Obtaining submissions from [/r/%s]' % subreddit)

    url_template = 'https://api.pushshift.io/reddit/search/submission?subreddit=%s&before=%sd&after=%sd&size=1000&score=>1'
    data = []

    for i in range(0, int(days)):

        url = url_template % (subreddit, str(i), str(i+1))

        r = requests.get(url)
        
        data_per_day = 0
        for submission in r.json()['data']:
            datum = {}
            for col_name in column_names:
            
                if col_name == column_names[4]:
                    datum[column_names[4]] = int(datetime.datetime.fromtimestamp(datum['created_utc']).strftime('%H'))
                elif col_name == column_names[5]:
                    datum[column_names[5]] = datetime.datetime.fromtimestamp(datum['created_utc']).strftime('%a')
                else:
                    datum[col_name] = submission[col_name]

            data.append(datum)
            data_per_day = data_per_day + 1

        print('\tObtained %s data points [before=%sd] [after=%sd]' % (str(data_per_day), str(i), str(i+1)))

    return data

"""
"""
def transform_data(subreddit, data, column):

    print('Aggregating data for [subreddit=%s] [column=%s]' % (subreddit, column))

    transformed = {}
    for weekday in weekdays:
        transformed[weekday] = {}
        for hour in hours:
            transformed[weekday][hour] = []

    for datum in data:
        weekday = datum[column_names[5]]
        hour = int(datum[column_names[4]])
        value = datum[column]
        transformed[weekday][hour].append(value)

    means = []
    for weekday in weekdays:
        means_for_day = []

        for hour in hours:
            values = transformed[weekday][hour]
            stats = calculate_stats(values)
            means_for_day.append(stats)

        means.append(means_for_day)

    print(means)

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
    csv_writer.writerow(column_names)
    
    for datum in data:
        csv_writer.writerow([
            datum[column_names[0]], 
            datum[column_names[1]], 
            datum[column_names[2]], 
            datum[column_names[3]],
            datum[column_names[4]],
            datum[column_names[5]],
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
    weekdays.reverse()

    plotly.offline.plot(
        {
            "data" : [go.Heatmap(
                z = data_to_plot,
                x = [str(h) for h in hours],
                y = weekdays,
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

    # Write data to CSV
    write_data_to_csv(subreddit, data)

    # Get data for plotting
    score_means = transform_data(subreddit, data, column_names[3])
    num_comments_means = transform_data(subreddit, data, column_names[1])

    # Plot data
    # plot_data(score_means, subreddit, 'Score', 'Mean')
    # plot_data(num_comments_means, subreddit, 'Num Comments', 'Mean')
