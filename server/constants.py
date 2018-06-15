COLUMN_NAMES = [
    'created_utc',
    'num_comments',
    'domain',
    'score',
    'hour',
    'weekday'
]

WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

HOURS = range(0, 24)

URL_TEMPLATE = 'https://api.pushshift.io/reddit/search/submission?subreddit=%s&before=%sd&after=%sd&size=1000'
