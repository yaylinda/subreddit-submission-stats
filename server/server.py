from flask import Flask, request, jsonify
from flask_cors import CORS

from subreddit_score import *

app = Flask(__name__)
CORS(app)

"""
Obtain data and transform into valid format for Plotly.js.

    Input:
        - subreddit:
        - days:
        - stat:
    
    Output:
        - JSON
"""
@app.route('/generate/<subreddit>/<days>/<stat>', methods = ['GET'])
def generate(subreddit, days, stat):

    print('Generating data and plot... [subreddit = %s] [days = %s] [stat = %s]' % (subreddit, days, stat))

    # Make sure Subreddit is valid
    if not validate_subreddit(subreddit):
        return jsonify(
            status = 'ERROR',
            message = 'Incorrect value for [subreddit].',
            subreddit = subreddit, 
            days = days,
            stat = stat
        )

    # Obtain raw data using pushshift.io
    data = generate_data(str(subreddit), int(days))

    # Transform data for plotting
    if stat.upper() == 'SCORE':
        score_means = transform_data(subreddit, data, column_names[3])
        score_means.reverse() # reverse data for day of the week
        return jsonify(
            status = 'SUCCESS',
            means = score_means,
            subreddit = subreddit,
            days = days,
            stat = stat.upper())
    elif stat.upper() == 'COMMENT':
        num_comments_means = transform_data(subreddit, data, column_names[1])
        num_comments_means.reverse() # reverse data for day of the week
        return jsonify(
            status = 'SUCCESS',
            means = num_comments_means,
            subreddit = subreddit, 
            days = days,
            stat = stat.upper())
    else:
        return jsonify(
            status = 'ERROR',
            message = 'Incorrect value for [stat]. Must be one of [SCORE, COMMENT].',
            subreddit = subreddit, 
            days = days,
            stat = stat
        )


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
Start server
"""
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')