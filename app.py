from flask import (Flask, send_file, request, render_template)
from serpapi import GoogleSearch
from datetime import datetime
import csv
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
# konstrukce dotazu do SerpApi s frazi z html form, gl je kod pro location, 10 vysledku = 1. strana
def getresults():
    query = request.form['query']
    params = {
        "api_key": "9fdfdbd4120faef3d195b4d2530640d4ff1d087734e60a56de58a04d1e04f39c",
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
        "gl": "cz",
        "num": "10"}

    search = GoogleSearch(params)
    results = search.get_dict()

    # generator radku do csv souboru, k ziskanym informacim pridava timestamp
    def parse(data):
        for d in data['organic_results']:
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pos = d['position']
            title = d['title']
            snippet = d['snippet']
            link = d['link']
            item = [dt, pos, title, link, snippet]
            yield item

    # csv soubor se bude ukladat docasne
    os.chdir('/tmp')
    filename = 'results.csv'

    # nazvy sloupcu = prvni radka csv souboru
    fields = ['datum_cas', 'pozice', 'nadpis', 'link', 'snippet']
    f = open(filename, 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)

    #zapis prvni radky a smycka pro zapis vysledku vyhledavani do csv
    writer.writerow(fields)
    for i in parse(results):
        writer.writerow(i)
    return render_template('index.html')


@app.route('/download')
def download():
    path = '/tmp/results.csv'
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
