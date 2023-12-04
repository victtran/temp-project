from flask import Flask, render_template, request   
import pandas as pd
from create_data import create_nested_dict_from_csv, convert_to_dict_structure, merge_dicts
from search_algorithm import search_nested_dict_top5_similarity


################################################################
csv_file_path = 'mindmaptest.csv'

df = pd.read_csv(csv_file_path, header =None, skiprows=1)

for i,col in enumerate(df.columns[1:], start=1):
    df[col] = df[col].shift(-1*col)
df = df.dropna(axis=0, how='all')
df = df.reset_index(drop=True)
df.to_csv('new_mindmap.csv')  
mindmap_data = create_nested_dict_from_csv(df)
convert_to_dict_structure(mindmap_data)
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
    search_results = search_nested_dict_top5_similarity(mindmap_data, query)

    # Render a search results page
    return render_template('search_results.html', query=query, results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
