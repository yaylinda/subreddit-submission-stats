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
@app.route('/generate/<subreddit>/<days>', methods = ['GET'])
def generate(subreddit, days):

    print('Generating data and plot... [subreddit = %s] [days = %s]' % (subreddit, days))

    # Make sure Subreddit is valid
    if not validate_subreddit(subreddit):
        return jsonify(
            status = 'ERROR',
            message = 'Incorrect value for [subreddit].',
            subreddit = subreddit, 
            days = days
        )

    # Obtain raw data using pushshift.io
    data = generate_data(str(subreddit), int(days))

    # Transform data for plotting
    score_means = transform_data(subreddit, data, column_names[3])
    score_means.reverse() # reverse data for day of the week

    num_comments_means = transform_data(subreddit, data, column_names[1])
    num_comments_means.reverse() # reverse data for day of the week

    return jsonify(
        status = 'SUCCESS',
        scores = score_means,
        comments = num_comments_means,
        subreddit = subreddit,
        days = days)

    # return jsonify(
    #     status = 'ERROR',
    #     message = 'Incorrect value for [stat]. Must be one of [SCORE, COMMENT].',
    #     subreddit = subreddit, 
    #     days = days
    # )

"""
Start server
"""
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')