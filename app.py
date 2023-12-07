from flask import Flask, render_template, request   
import pandas as pd
from create_data import parse_csv_to_dict
from search_algorithm import search_nested_dict_top5_similarity


################################################################
csv_file_path = 'mindmaptest2.csv'
nested_dict = parse_csv_to_dict(csv_file_path)
################################################################


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search')
def search():
# Get the search query from the URL parameters
    query = request.args.get('query', '')

    # Perform search using your search algorithm
    search_results = search_nested_dict_top5_similarity(nested_dict, query)

    # Render a search results page
    return render_template('search_results.html', query=query, results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
