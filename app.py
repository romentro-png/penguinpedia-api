import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WIKIPEDIA = 'https://en.wikipedia.org/w/rest.php/v1/page/{title}/html'

@app.get('/article')
def article():
    title = request.args.get('title', '').strip()
    if not title:
        return jsonify(error='Missing title parameter'), 400
    try:
        response = requests.get(WIKIPEDIA.format(title=requests.utils.quote(title.replace(' ', '_'), safe='')),
                                headers={'User-Agent': 'PenguinPedia/1.0 (educational encyclopedia project)', 'Accept': 'text/html'}, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.select('style, script, noscript, table, figure, .mw-editsection, .reference, .reflist, .navbox, .metadata, .hatnote, .shortdescription, .toc, .mw-empty-elt, sup.reference'):
            tag.decompose()
        root = soup.select_one('section') or soup.body or soup
        for heading in root.select('h1, h2, h3, h4, h5, h6'):
            heading.insert_before('\n\n')
            heading.insert_after('\n')
        for paragraph in root.select('p, li'):
            paragraph.insert_after('\n\n' if paragraph.name == 'p' else '\n')
        text = root.get_text(separator=' ', strip=False)
        import re
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' *\n *', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        page_title = (soup.find('h1').get_text(' ', strip=True) if soup.find('h1') else title.replace('_', ' '))
        return jsonify(title=page_title, extract=text)
    except requests.HTTPError as exc:
        return jsonify(error='Wikipedia could not return this article', status=exc.response.status_code), 502
    except requests.RequestException:
        return jsonify(error='Wikipedia request failed'), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')))
