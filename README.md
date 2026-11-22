# PenguinPedia article-to-text API

A small Flask service that fetches full Wikipedia article HTML, strips markup and non-article elements, and returns simple JSON:

```json
{"title":"Hebrew","extract":"Full article text..."}
```

## Local use

```sh
pip install -r requirements.txt
python app.py
```

Try `http://localhost:8000/article?title=Hebrew`.

## HTTPS hosting

Deploy this directory as a Python web service on Render, Railway, or a similar host. On Render, use build command `pip install -r requirements.txt` and start command `gunicorn app:app --bind 0.0.0.0:$PORT`. Once deployed, use `https://YOUR-SERVICE.example/article?title=Hebrew` in PenguinMod. The URL only becomes publicly accessible after deployment.

## Notes

- CORS is enabled for browser-based projects.
- Wikipedia may change its HTML structure; text conversion is best-effort.
- This removes infoboxes, references, and navigation elements, but preserves the main article's headings and prose.
- For a public deployment, consider caching and rate limiting to reduce Wikipedia requests.
