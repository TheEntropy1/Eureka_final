from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

TMDB_API_KEY = '483a8d6b53d5bb68c110d2c17aa6d725'  # <-- replace this with your own TMDB API key

# Fetch trending movies, series, anime
def get_latest(media_type):
    url = f"https://api.themoviedb.org/3/trending/{media_type}/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])[:6]
    else:
        return []

@app.route('/')
def home():
    latest_movies = get_latest('movie')
    latest_tv = get_latest('tv')
    latest_anime = get_latest('tv')  # Simplification for anime
    return render_template('home.html', movies=latest_movies, tv=latest_tv, anime=latest_anime)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

@app.route('/watch/<media_type>/<int:media_id>')
def watch(media_type, media_id):
    details_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}?api_key={TMDB_API_KEY}"
    response = requests.get(details_url)
    if response.status_code == 200:
        details = response.json()
        return render_template('watch.html', media=details, media_type=media_type)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
